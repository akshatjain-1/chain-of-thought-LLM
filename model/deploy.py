# model/deploy.py
import sagemaker
from sagemaker.huggingface import HuggingFaceModel
import boto3

# 1. Configuration
iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='AmazonSageMaker-ExecutionRole-2025-01-07')['Role']['Arn']
s3_model_path = "s3://geogpt-models-your-initials/GeoGPT-R1-Preview/model.tar.gz"
huggingface_image_uri = "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:2.1-transformers4.37-gpu-py310-cu121-ubuntu20.04"

# 2. Create a HuggingFaceModel object
huggingface_model = HuggingFaceModel(
   model_data=s3_model_path,      # path to your model and script
   role=role,                    # IAM role with permissions to create endpoint
   image_uri=huggingface_image_uri, # Hugging Face DLC
   env={
       'HF_MODEL_ID': "GeoGPT-Research-Project/GeoGPT-R1-Preview", # This is for reference, not used for loading from S3
       'SM_NUM_GPUS': '1' # Ensure it uses the GPU
   }
)

# 3. Deploy the model to an endpoint
# This is a GPU-intensive task, choose an appropriate instance type.
# 'ml.g5.2xlarge' is a good starting point.
predictor = huggingface_model.deploy(
   initial_instance_count=1,
   instance_type="ml.g5.2xlarge",
   endpoint_name="geogpt-r1-preview-endpoint"
)

print(f"Endpoint deployed successfully. Endpoint name: {predictor.endpoint_name}")