import typing


class NotFound(Exception):
    message: typing.Text

    def __init__(self, message: typing.Text):
        self.message = message


class AlreadyExists(Exception):
    message: typing.Text
    path: typing.List

    def __init__(self, message: typing.Text, path: typing.List = None):
        self.message = message
        self.path = path or []
