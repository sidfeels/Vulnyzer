import streamlit as st
import requests
import json
from gett import get_token 

def novaai_wow_vision(input_content, img_url):
    r=requests.post(
        "https://api.githubcopilot.com/chat/completions",
        headers={
            "Editor-Version":"vscode/1.83.0",
            "Editor-Plugin-Version":"copilot-chat/0.8.0",
            "Authorization":"Bearer "+get_token()
        },
        json={
            "messages":[
                {
                    "role":"user",
                    "content":json.dumps([input_content, {"image":img_url}]),
                },
            ],
            "model":"gpt-4",
            "temperature":0.7,
        }
    )
    return r.text

st.title('Image Analyzer')
img_url = st.text_input('Enter the image URL here:')
if st.button('Tell me about this image'):
    if img_url:
        result = novaai_wow_vision("Tell me about this.", img_url)
        if result:
            try:
                result_json = json.loads(result)
                content = result_json.get('choices', [{}])[0].get('message', {}).get('content', '')
                st.write(content)
            except json.JSONDecodeError:
                st.error('The API response is not a valid JSON string.')
    else:
        st.error('Please enter an image URL.')