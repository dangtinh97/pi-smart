import requests
from config import GEMINI_API_KEY
from services.text_to_speech import play_voice
class AIAgent:
    def __init__(self):
        pass
    async def question(self, question):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        body = {
            "contents": [
              {
                "parts": [
                  {
                    "text": question
                  }
                ],
              },
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "stopSequences": []
            },
          }
        response = requests.post(url, json=body,headers={'content-type': 'application/json','x-goog-api-key':GEMINI_API_KEY})
        print(response.json())
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        play_voice(answer.replace('**', ''))
        return response.json()
aiAgent = AIAgent()