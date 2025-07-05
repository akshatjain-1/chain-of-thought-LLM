import gradio as gr
import time
import random

# --- Custom CSS to Mimic Gemini's UI ---
gemini_css = """
/* Main background and fonts */
body, .gradio-container { background-color: #131314; color: #E3E3E3; font-family: 'Google Sans', 'sans-serif'; }
/* Remove header and footer borders */
.gradio-container > .main, .gradio-container > .footer { border-top: none !important; }
/* Input textbox style */
#chat_input_row textarea { background-color: #1F1F1F; border-color: #444746 !important; border-radius: 20px !important; }
/* Chat bubble styles */
.message-bubble { background-color: #1F1F1F !important; border-radius: 15px !important; }
/* User message bubble */
.message-bubble.user { background-color: #3B82F6 !important; color: white !important; }
/* Bot message bubble */
.message-bubble.bot { background-color: #1F1F1F !important; }
/* Blue "New Chat" button */
#new_chat_button { background-color: #3B82F6; color: white; }
/* General button styling */
.gr-button { border-radius: 8px !important; }
/* Sidebar styling */
#sidebar { background-color: #1E1F20; padding: 10px; border-radius: 12px; }
"""

# --- Backend Logic and State Management ---
def process_chat_message(message, history):
    # This is where your agent will be called
    bot_response = f"This is a mocked response to: '{message}'"
    history.append((message, bot_response))
    return "", history

def start_new_chat(sessions):
    session_id = f"Chat Session {len(sessions) + 1}"
    sessions[session_id] = []
    return sessions, session_id, [], gr.update(choices=list(sessions.keys()), value=session_id)

def load_chat_session(session_id, sessions):
    return sessions.get(session_id, [])

def save_chat_session(session_id, history, sessions):
    if session_id:
        sessions[session_id] = history
    return sessions

# --- UI Definition using Blocks ---
with gr.Blocks(theme=gr.themes.Default(), css=gemini_css, title="GeoGPT") as demo:
    chat_sessions = gr.State({})
    current_session_id = gr.State("")

    with gr.Row():
        # --- Left Sidebar ---
        with gr.Column(scale=1, elem_id="sidebar"):
            new_chat_button = gr.Button("New Chat", elem_id="new_chat_button")
            gr.Markdown("### Recent Chats")
            recent_chats_display = gr.Radio(label="Saved Chats", choices=[], interactive=True)
            gr.Markdown("### My Tools")
            tools_dropdown = gr.Dropdown(label="Available Tools", choices=["PythonREPL", "RAG Knowledge Base"], value="PythonREPL")

        # --- Main Chat Area ---
        with gr.Column(scale=4):
            chatbot_display = gr.Chatbot(
                label="GeoGPT",
                bubble_full_width=False,
                height=650,
                # URLs to user and bot avatar icons
                avatar_images=(
                    "https://www.gstatic.com/images/branding/product/2x/avatar_square_blue_120dp.png",
                    "https://www.gstatic.com/images/branding/product/1x/gemini_48dp.png"
                )
            )
            with gr.Row(elem_id="chat_input_row"):
                message_input = gr.Textbox(
                    placeholder="Ask GeoGPT a question...",
                    show_label=False,
                    scale=5
                )
                submit_button = gr.Button("➤", variant="primary", scale=1)

    # --- Event Handlers ---
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
    new_chat_button.click(
        start_new_chat, [chat_sessions], [chat_sessions, current_session_id, chatbot_display, recent_chats_display]
    )
    recent_chats_display.change(
        load_chat_session, [recent_chats_display, chat_sessions], [chatbot_display]
    ).then(
        lambda x: x, [recent_chats_display], [current_session_id]
    )
    demo.load(
        start_new_chat, [chat_sessions], [chat_sessions, current_session_id, chatbot_display, recent_chats_display]
    )

if __name__ == "__main__":
    demo.launch()