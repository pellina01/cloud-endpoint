class status_validate:
    def __init__(self):
        self.counter = 0

    def isValid(self, recieved_list):
        status = recieved_list["status"]
        return getattr(status_validate, status)(self)

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
