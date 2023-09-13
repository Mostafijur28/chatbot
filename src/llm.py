from abc import ABC, abstractmethod


class BaseLlm(ABC):
    @abstractmethod
    def chat(self, prompt):
        pass

    @abstractmethod
    def chat_completion(self, prompt):
        pass
