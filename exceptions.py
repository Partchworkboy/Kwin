class CredentialsError(Exception):
    def __init__(self):
        super().__init__('Username/password is incorrect')


