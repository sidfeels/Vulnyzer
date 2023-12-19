import gradio as gr
import requests
import time
from gradio.themes.utils import sizes

# Function to get the token
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
            "temperature":0.4,
        }
    )

    if r.status_code != 200:
        return "Error 404"

    return r.json()["choices"][0]["message"]["content"]


# Gradio interface
def chat_interface(user_input, model,):
    global messages
    if user_input.lower() == 'reset':
        messages = []
        return "Conversation reset"
    messages.append({"role": "user", "content": user_input})
    output = openai_agent_test(messages, model)
    messages.append({"role": "assistant", "content": output})
    return output

messages = []
iface = gr.Interface(
    fn=chat_interface, 
    inputs=["text", gr.Radio(["gpt-4","gpt-3.5"])],
    outputs="text",
)
messages = []
demo = gr.ChatInterface(
    iface,
    chatbot=gr.Chatbot(
        show_copy_button=False,
        show_share_button=True,
        bubble_full_width=False,
        
    ),
    title='ChatBot',
    theme=gr.themes.Soft(),
    css="footer {visibility: hidden}",
    analytics_enabled=False
)

if __name__=='__main__':
    demo.launch()