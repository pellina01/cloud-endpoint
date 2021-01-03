class status_validate:
    def __init__(self):
        self.counter = 0
        self.state = {
        "connected":self.__connected(),
        "disconnected":self.__disconnected(),
        "sending":self.__sending()
        }

    def isValid(self, recieved_list):
        return self.state.get(recieved_list["status"], False)

    def __connected(self):
        self.counter += 1
        return True if self.counter == 1 else False

    def __disconnected(self):
        if self.counter > 0:
            self.counter -= 1
            return True if self.counter == 0 else False
        else:
            return False

    def __sending(self):
        return True
