from ._states import _missing, _notavalue, _unimplemented, _deleted


class BaseCachedPropertyException(Exception):
    """Common BaseException for landuo."""

    def __init__(self, descriptor_name, state) -> None:
        self.descriptor_name = descriptor_name
        self.state = state


class DeletedCachedProperty(BaseCachedPropertyException):

    def __str__(self):
        return f"The CachedProperty `{self.descriptor_name}` has been {self.state}."


class SetterUnimplemented(BaseCachedPropertyException):

    def __str__(self):
        return f"The CachedProperty `{self.descriptor_name}`'s setter is {self.state}."
