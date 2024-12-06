class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def to_dict(self):
        return {
            "username": self.__username,
            "password": self.__password,
        }
