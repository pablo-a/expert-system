class ParsingError(Exception):
    def __init__(self, msg):
        self.msg = msg


def raise_parsing_error(msg):
    raise ParsingError(msg)
