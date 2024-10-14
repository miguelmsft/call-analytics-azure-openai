import os  
import json  
import numpy as np  
from dotenv import load_dotenv  
from openai import AzureOpenAI  
from pydantic import BaseModel  

# Load environment variables from .env file  
load_dotenv()  
aoai_endpoint = os.getenv("AOAI_ENDPOINT")  
aoai_api_key = os.getenv("AOAI_API_KEY")  
aoai_deployment_name = os.getenv("AOAI_DEPLOYMENT")  
  
# Initialize the AzureOpenAI client  
client = AzureOpenAI(  
    azure_endpoint=aoai_endpoint,  
    api_key=aoai_api_key,  
    api_version="2024-08-01-preview"  
)  
  
input_directory='call_transcripts'
output_directory='results'

# Ensure the output directory exists  
os.makedirs(output_directory, exist_ok=True)  

# Iterate over each file in the input directory  
for filename in os.listdir(input_directory):  
    if filename.endswith('.txt'):  
        print(f"Processing {filename}...")  # Processing status message  
        try:  
            # Read the content of the text file  
            file_path = os.path.join(input_directory, filename)  
            with open(file_path, 'r') as file:  
                content = file.read()  

            # Create a subfolder in the output directory named after the file (without extension)  
            subfolder_name = os.path.splitext(filename)[0]  
            subfolder_path = os.path.join(output_directory, subfolder_name)  
            os.makedirs(subfolder_path, exist_ok=True)  

            # Define output format  
            class ExtractedInformation(BaseModel):  
                summary: str  
                service: str  
                organizations: list[str]  
                sentimentStart: str  
                sentimentEnd: str  
                issues: str  
                resolution: str  
                feedback: str  

            # Generate completions using the Azure OpenAI API  
            system_message = "You are an expert assistant that helps people extract important information from call transcripts."  
            user_message = f"""  
            Extract the following from the call transcript:  
            1. A descriptive summary  
            2. The service or product they are calling about  
            3. Organizations that are mentioned  
            4. The sentiment at the start of the call  
            5. The sentiment at the end of the call  
            6. Issues that the caller mentions  
            7. Resolution (if any)  
            8. Feedback (if any)  

            Call transcription:  
            {content}  
            """  

            completion = client.beta.chat.completions.parse(  
                model=aoai_deployment_name,  
                messages=[  
                    {"role": "system", "content": system_message},  
                    {"role": "user", "content": user_message}  
                ],  
                response_format=ExtractedInformation,  
                max_tokens=8000  
            )  

            response = json.loads(completion.model_dump_json(indent=2))  
            call_analysis = response['choices'][0]['message']['parsed']  

            # Save the extracted information to a JSON file  
            json_file_path = os.path.join(subfolder_path, 'extracted_content.json')  
            with open(json_file_path, 'w') as json_file:  
                json.dump(call_analysis, json_file, indent=2)  

            print(f"Success: {filename} processed successfully.\nResult: {call_analysis}")  

        except Exception as e:  
            print(f"Error processing {filename}: {e}")  
  
