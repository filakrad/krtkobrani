

class BadState(Exception):
    def __init__(self, message, current_state):
        super().__init__(message)
        self.current_state = current_state


class TooSoon(Exception):
    def __init__(self, message, available_time):
        super().__init__(message)
        self.available_time = available_time
