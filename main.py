import openai
import logging
from openai import InvalidRequestError
from openai.error import RateLimitError, AuthenticationError
from src.llm import BaseLlm
from src.domain import Role, Message, ChatLog

logging.basicConfig(filename="logs.log", level=logging.INFO)


class OpenAi(BaseLlm):
    def __init__(
        self,
        chatLog: ChatLog,
        model="gpt-3.5-turbo",
        temperature=0.6,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        number_of_results=1,
    ):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.number_of_results = number_of_results
        self.chatLog = chatLog

    def get_model(self):
        return self.model

    def get_chatLog(self):
        return self.chatLog.messages

    def chat(self, message: Message, max_tokens=256):
        "New message response"
        if message.id not in self.chatLog.id_map:
            self.chatLog.add_message(message)

        try:
            response = openai.ChatCompletion.create(
                n=self.number_of_results,
                model=self.model,
                messages=self.chatLog.messages,
                temperature=self.temperature,
                max_tokens=max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )

            content = response.choices[0].message["content"]

            if message.id not in self.chatLog.id_map:
                self.chatLog.add_message(Message(role=Role.SYSTEM, content=content))

            return {"role": Role.SYSTEM, "content": content}

        except AuthenticationError as auth_error:
            logging.error("Authentication error = %s", auth_error)
            return {"error": "ERROR_AUTHENTICATION", "message": "User Not Authorised"}

        except RateLimitError as rate_limit_error:
            logging.error("Rate Limit Error = %s", rate_limit_error)
            return {
                "error": "ERROR_RATE_LIMIT",
                "message": "Openai rate limit exceeded..",
            }

        except InvalidRequestError as invalid_request_error:
            logging.error("Invalid Request = %s", invalid_request_error)
            return {
                "error": "ERROR_INVALID_REQUEST",
                "message": "Openai invalid request error..",
            }

        except Exception as exception:
            logging.error("Exception = %s", exception)
            return {"error": "ERROR_OPENAI", "message": "Open ai exception"}

    def chat_completion(self, prompt: str, max_tokens=256):
        try:
            response = openai.ChatCompletion.create(
                n=self.number_of_results,
                model=self.model,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )

            content = response.choices[0]["text"]
            return {"role": Role.SYSTEM, "content": content}

        except AuthenticationError as auth_error:
            logging.error("Authentication error = %s", auth_error)
            return {"error": "ERROR_AUTHENTICATION", "message": "User Not Authorised"}

        except RateLimitError as rate_limit_error:
            logging.error("Rate Limit Error = %s", rate_limit_error)
            return {
                "error": "ERROR_RATE_LIMIT",
                "message": "Openai rate limit exceeded..",
            }

        except InvalidRequestError as invalid_request_error:
            logging.error("Invalid Request = %s", invalid_request_error)
            return {
                "error": "ERROR_INVALID_REQUEST",
                "message": "Openai invalid request error..",
            }

        except Exception as exception:
            logging.error("Exception = %s", exception)
            return {"error": "ERROR_OPENAI", "message": "Open ai exception"}

    def re_generate_response(self, message: Message, max_tokens=256):
        response = self.chat(message, max_tokens)
        response_idx = self.chatLog.id_map[message.id]
        self.chatLog[response_idx + 1].content = response["content"]

        return response

"""
CL = ChatLog(messages=[], id_map={})
opi = OpenAi(CL)

m1 = Message(Role.USER, "Hello")
print(opi.chat(m1))
"""
