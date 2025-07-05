# model/test_endpoint.py
import sagemaker
from sagemaker.huggingface import HuggingFacePredictor

# The name of the endpoint you just created
ENDPOINT_NAME = "geogpt-r1-preview-endpoint"

# Create a predictor object
predictor = HuggingFacePredictor(endpoint_name=ENDPOINT_NAME)

# Send a sample prompt
data = {
   "inputs": "What is the capital of India?",
   "parameters": {
      "max_new_tokens": 50,
      "do_sample": True
   }
}

# Get the prediction
response = predictor.predict(data)

print("Response from endpoint:")
print(response)

# IMPORTANT: Clean up the endpoint to avoid costs
# predictor.delete_endpoint()
# print("Endpoint deleted.")