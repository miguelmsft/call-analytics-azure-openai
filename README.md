# call-analytics-azure-openai

## Call Transcript Analyzer
 
This repository contains a Python script for analyzing call transcripts using Azure OpenAI. It extracts key information from .txt files located in the call_transcripts directory and outputs the results in a structured JSON format.

### Features

Processes .txt files to extract information such as summaries, service details, sentiment analysis, issues, resolutions, and feedback.
Utilizes Azure OpenAI for natural language understanding.
Outputs results in organized JSON files within the results directory.

### Setup
 
1. Clone the repository:

```
git clone https://github.com/miguelmsft/call-analytics-azure-openai.git 
cd call-analytics-azure-openai  
 ```
2. If you haven't already, go to https://ai.azure.com/ and create a deployment for a `gpt-4o` model version `2024-08-06`

![gpt-4o deployment] (images/gpt4o-deployment.png)


Create a .env file in the root directory with your Azure OpenAI credentials. 

```
AOAI_ENDPOINT=your_azure_endpoint  
AOAI_API_KEY=your_api_key  
AOAI_DEPLOYMENT=your_deployment_name  
```
 
3. Prepare your transcript files:

Place your .txt files in the call_transcripts directory. The script will process each file in this directory.

4. Optional. Customize the fields to extract from call transcripts.

```
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

```

### Usage
 
Run the script using the following command:


`python analyze_calls.py  `
 
The script will process each .txt file, outputting a JSON file containing the extracted information in a subdirectory within results named after each processed file.

### Example

#### Input
 
Example input file: `call_transcripts/20241014-contoso-call-example.txt`

```
------------------------------------BEGIN TRANSCRIPT------------------------------------  
16:07:23.529 - AGENT: Thank you for calling Contoso Outdoors. My name is Sarah. How can I assist you today?  
...  
16:08:24.325 - AGENT: Have a great day, John!  
------------------------------------END TRANSCRIPT------------------------------------  
```

#### Output
 
Example output file: `results/20241014-contoso-call-example/extracted_content.json`

```
{  
  "summary": "John Doe called Contoso Outdoors because he received a jacket with a broken zipper. The agent, Sarah, apologized for the inconvenience and arranged for a new jacket to be shipped, along with a return label for the defective one. Sarah assured John that the replacement would arrive in 3-4 business days, ensuring it would be in time for his trip.",  
  "service": "Jacket purchase from Contoso Outdoors",  
  "organizations": ["Contoso Outdoors"],  
  "sentimentStart": "Frustrated",  
  "sentimentEnd": "Relieved and grateful",  
  "issues": "Received a jacket with a broken zipper",  
  "resolution": "Replacement jacket will be shipped with expedited shipping and a return label for the defective one.",  
  "feedback": "Caller expressed relief and gratitude for the efficient handling of the issue."  
}  
```

### License
 
This project is licensed under the MIT License. See the LICENSE file for details.