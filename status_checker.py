class status_checker:
    def __init__(self):
        self.counter = 0

    def isValid(self, recieved_list):
        checker = recieved_list["status"]
        return getattr(status_checker, checker)

    def connected(self):
        self.counter += 1
        return True if self.counter == 1 else False

    def disconnected(self):
        if self.counter > 0:
            self.counter -= 1
            return True if self.counter == 0 else False

    def sending(self):
        return True
