import streamlit as st
import requests
import random
import time
from gett import get_token 

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def openai_agent_test(messages, model="gpt-4"):
    r = requests.post(
        "https://api.githubcopilot.com/chat/completions",
        headers={
            "Editor-Version":"vscode/1.83.0",
            "Authorization": f"Bearer {get_token()}",
        },
        json={
            "messages":messages,
            "model":model,
            "temperature":0.0,
        }
    )

    if r.status_code != 200:
        return "Sorry, Bot is under maintenance. *GPT-4 pr itna dependend mt rhe bhay* :)"

    return r.json()["choices"][0]["message"]["content"]
  
st.title('GPT-4-32k')

user_question = st.text_area('### Enter your question (ctrl+enter to send):', height=100)

ask_button = st.button("Ask")

last_question = st.session_state.get('last_user_question', '')

if (ask_button and user_question.strip()) or (user_question != last_question and user_question.strip()):
    st.session_state.last_user_question = user_question
    st.session_state.messages.append({"role": "user", "content": user_question})
    response = openai_agent_test([{"role":"user", "content": user_question}])
    st.session_state.messages.append({"role": "bot", "content": response})
   
chat_placeholder = st.empty()

if st.session_state.messages:
    last_msg = st.session_state.messages[-1:]
    chat_placeholder.markdown(f'**You**: {st.session_state.last_user_question}')
    chat_placeholder.markdown(f'**GPT-4**: {last_msg[0]["content"]}')

history_expander = st.sidebar.expander('Show History')
if history_expander: 
    for message in st.session_state.messages:
        if message["role"] == "user":
            history_expander.write(f"You: {message['content']}")
        else:
            history_expander.write(f"GPT-4: {message['content']}")  