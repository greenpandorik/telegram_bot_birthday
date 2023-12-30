import requests

from main import api_key_yagpt


async def get_msg_yagpt(name):
    prompt = {
        "modelUri": "gpt://b1gv78p0hhrd2cn2j5ug/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "assistant",
                "text": f"Поздравление с днём рождения для {name}"
            }
        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key_yagpt}"
    }
    response = requests.post(url, headers=headers, json=prompt)
    if response.status_code == 200:
        result = response.json()
        return (result['result']['alternatives'][0]['message']['text'])
    else:
        return False
