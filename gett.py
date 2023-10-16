import requests

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
token = get_token()
print(token)