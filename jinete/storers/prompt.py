from .abc import Storer


class PromptStorer(Storer):

    def store(self) -> None:
        text = self.formatted_planning()
        print(text)
