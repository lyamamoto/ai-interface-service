class AuthException(Exception):
    def __init__(self, message="Customer not found for auth token"):
        self.message = message
        super().__init__(self.message)