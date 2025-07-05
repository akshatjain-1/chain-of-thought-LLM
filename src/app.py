import gradio as gr
import time

# --- Custom CSS for advanced styling ---
css = """
#new_chat_button { background-color: #3B82F6; color: white; }
#chat_input_row { border-top: 1px solid #E5E7EB; padding-top: 10px; }
body { font-family: 'Inter', sans-serif; }
#chat_input_row { border-top: 1px solid #E5E7EB; padding-top: 10px; }
.gradio-container { border-radius: 15px !important; }

/* Add hover effects to buttons */
button { transition: all 0.2s ease-in-out; }
button:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }

/* Style the chat bubbles */
.message-bubble-user { background-color: #DBEAFE !important; color: #1E3A8A !important; border-radius: 15px 15px 0 15px !important; }
.message-bubble-bot { background-color: #F3F4F6 !important; color: #1F2937 !important; border-radius: 15px 15px 15px 0 !important; }
"""

# Function to process a new message
def process_chat_message(message, history):
    # This is where your agent will be called
    response = f"This is a mocked response to: '{message}'"
    history.append((message, response))
    return "", history # Clear input box and update history

# Function to start a new chat session
def start_new_chat(sessions):
    # Generate a unique ID for the new chat
    session_id = f"Chat - {int(time.time())}"
    # Initialize an empty history for this new session
    sessions[session_id] = []
    # Update the list of available chat sessions
    return sessions, session_id, [], gr.update(choices=list(sessions.keys()), value=session_id)

# Function to load a selected chat session
def load_chat_session(session_id, sessions):
    # Return the history for the selected session_id
    return sessions.get(session_id, [])

# Function to save the current chat history to its session
def save_chat_session(session_id, history, sessions):
    if session_id:
        sessions[session_id] = history
    return sessions

# --- Main UI Definition using Blocks ---
with gr.Blocks(theme=gr.themes.Soft(), title="GeoGPT", css=css) as demo:
    # State object to hold all chat histories
    chat_sessions = gr.State({})

    current_session_id = gr.State("")

    with gr.Row():
        # --- Left Sidebar ---
        with gr.Column(scale=1):
            gr.Markdown("## GeoGPT Controls")
            new_chat_button = gr.Button("New Chat", elem_id="new_chat_button")
            
            gr.Markdown("### Recent Chats")
            recent_chats_display = gr.Radio(
                label="Saved Chats",
                choices=[], # Will be updated dynamically
                interactive=True
            )

            gr.Markdown("### My Tools")
            tools_dropdown = gr.Dropdown(
                label="Available Tools",
                choices=["PythonREPL", "RAG Knowledge Base", "Web Search"],
                value="PythonREPL"
            )

        # --- Main Chat Area ---
        with gr.Column(scale=4):
            chatbot_display = gr.Chatbot(
                label="GeoGPT",
                bubble_full_width=False,
                height=600
            )
            # Row for the chat input box and buttons
            with gr.Row(elem_id="chat_input_row"):
                upload_button = gr.UploadButton("📁", file_types=["file"])
                # Placeholder for the other left-bottom button
                other_button = gr.Button("⚙️")
                message_input = gr.Textbox(
                    placeholder="Ask GeoGPT a question...",
                    show_label=False,
                    scale=5 # Makes the textbox take up most of the space
                )
                submit_button = gr.Button("Send", variant="primary", scale=1)

    # --- Event Handlers ---

    # When a message is sent, process it and then save the updated session
    submit_button.click(
        process_chat_message, [message_input, chatbot_display], [message_input, chatbot_display]
    ).then(
        save_chat_session, [current_session_id, chatbot_display, chat_sessions], [chat_sessions]
    )
    message_input.submit(
        process_chat_message, [message_input, chatbot_display], [message_input, chatbot_display]
    ).then(
        save_chat_session, [current_session_id, chatbot_display, chat_sessions], [chat_sessions]
    )

    # Start a new chat when the button is clicked
    new_chat_button.click(
        start_new_chat, [chat_sessions], [chat_sessions, current_session_id, chatbot_display, recent_chats_display]
    )

    # Load a chat when a recent chat is selected from the radio list
    recent_chats_display.change(
        load_chat_session, [recent_chats_display, chat_sessions], [chatbot_display]
    ).then(
        lambda x: x, [recent_chats_display], [current_session_id] # Update the current session ID
    )
    
    # Load the app and start the first chat session
    demo.load(
        start_new_chat, [chat_sessions], [chat_sessions, current_session_id, chatbot_display, recent_chats_display]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()