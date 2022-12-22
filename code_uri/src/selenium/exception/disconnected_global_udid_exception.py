class DisconnectedGlobalUdidException(Exception):
    msg: str

    def __init__(self, msg: str = None, *args: object):
        self.msg = msg
        super().__init__(msg, *args)
