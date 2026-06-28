from groq import Groq

from config import Config

from prompts.rag_prompt import (
    SYSTEM_PROMPT
)


class GroqClient:

    def __init__(self):

        self.client = Groq(

            api_key=Config.GROQ_API_KEY

        )

    def generate(

        self,

        prompt

    ):

        response = self.client.chat.completions.create(

            model=Config.MODEL_NAME,

            temperature=0,

            messages=[

                {

                    "role": "system",

                    "content": SYSTEM_PROMPT

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )

        return (

            response

            .choices[0]

            .message

            .content

        )