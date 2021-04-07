class AuthToken:

    tokens: list[str]
    current_token = 0

    def __init__(self, tokens: list) -> None:
        self.tokens = ['Bearer {}'.format(token)
                       for token in tokens]

    def next_token(self):
        if self.current_token < len(self.tokens) - 1:
            self.current_token += 1
        else:
            self.current_token = 0

    def get_token(self) -> str: return self.tokens[self.current_token]
