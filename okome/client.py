class Client():
    def __init__(self):
        self.__init__(self, None, None)
    
    def __init__(self, csrf_token: str, session_hash: str):
        self.csrf_token = csrf_token
        self.session_hash = session_hash
       
    def login(self, id: str, password: str):
        # TODO: logging
        pass