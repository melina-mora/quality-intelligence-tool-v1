import requests

OLLAMA_API = 'http://localhost:11434/api/chat'

def chat(model, system_prompt, user_message):
    body = {
        "model":model,
        "messages":[
            {"role": "system", "content":system_prompt},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    r = requests.post(OLLAMA_API, json = body)

    return r.json()["message"]["content"]
