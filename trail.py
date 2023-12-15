import streamlit as st
import requests
import time

# Setting page title and header
st.set_page_config(page_title="GPT-4", page_icon=":robot_face:")


# Function to get token
def get_token():
    try:
        url = "https://api.github.com/copilot_internal/v2/token"
        headers = {
            "Authorization": "token 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",
            "Editor-Version": "vscode/1.83.0",
            "Editor-Plugin-Version": "copilot-chat/0.8.0"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json = response.json()
            if 'token' in json:
                return json['token']
        else:
            return {"error": f"Received {response.status_code} HTTP status code"}
    except Exception as e:
        return {"error": str(e)}

# Get the token once and store the time
token = get_token()
token_time = time.time()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

# Function to interact with the chatbot
def openai_agent_test(messages, model="gpt-4"):
    global token, token_time

    # Check if token is older than 10 minutes, if so, fetch a new one
    if time.time() - token_time > 600:  # 600 seconds = 10 minutes
        token = get_token()
        token_time = time.time()

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

with st.form("my_form"):
    user_input = st.text_area("GPT-4-32K:", key='input', height=100)
    submit_button = st.form_submit_button(label='Ask')
    clear_button = st.form_submit_button(label='Clear Conversation')

# Reset everything
if clear_button:
    st.session_state['messages'] = [{"role": "system", "content": st.session_state.system_prompt}]

if submit_button and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    output = openai_agent_test(st.session_state['messages'], "gpt-4")
    st.session_state['messages'].append({"role": "assistant", "content": output})
    st.markdown(f'**GPT-4**: {output}')

# Show History
history_expander = st.expander('Show History')
if history_expander: 
    for message in st.session_state.messages:
        if message["role"] == "user":
            history_expander.write(f"You: {message['content']}")
        else:
            history_expander.write(f"GPT-4: {message['content']}")