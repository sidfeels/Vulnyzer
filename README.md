# Interacte with gpt-4-32k model from github copilot via Streamlit interface

## Description
This Streamlit-based application allows users to interact with gpt-4-32k, gpt-3.5-turbo, including options for model selection, PDF text extraction, and YouTube transcript extraction. It is designed for educational purposes to help users understand and experiment with different AI capabilities. Due to a previous security issue with an exploited , this git no longer works unless you have a outh token for copilot which is working.

## Features
- **Model Selection**: Choose from predefined models or input a custom model name.
- **Document Handling**: Upload PDF documents to extract text.
- **Video Processing**: Input YouTube links to fetch and display video transcripts.
- **Dynamic Interaction**: Test interactions with AI models using custom prompts and settings.

## Installation
To get started with this project, follow these steps:
```bash
# Clone the repository
git clone https://yourgithubrepo.com/yourproject.git
cd yourproject

# Install dependencies
pip install -r requirements.txt

# Set up your API tokens in a .env file
echo "API_TOKEN=your_secure_token_here" > .env

# Run the Streamlit application
streamlit run your_script.py
