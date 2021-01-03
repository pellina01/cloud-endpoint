class status_validate:
    def __init__(self):
        self.counter = 0
        self.state = {
        "connected":self.connected(),
        "disconnected":self.disconnected(),
        "sending":self.sending()
        }

    def isValid(self, recieved_list):
        return self.state.get(recieved_list["status"], False)

    def connected(self):
        self.counter += 1
        return True if self.counter == 1 else False

    def disconnected(self):
        if self.counter > 0:
            self.counter -= 1
            return True if self.counter == 0 else False
        else:
            return False

    def sending(self):
        return True
