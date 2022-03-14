class TgFilter:
    def __init__(self, senders = [], texts = []):
        if isinstance(senders, list):
            self.senders = senders
        else:
            self.senders = [senders]
        self.texts = [] # text filter will be implemented later
