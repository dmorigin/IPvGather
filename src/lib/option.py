
"""
"""
class Option:

    """
    """
    def __init__(self, value) -> None:
        self._value = value


    """
    """
    def __del__(self) -> None:
        self._value = None


    """
    """
    def some(self) -> bool:
        return self._value != None


    """
    """
    def none(self) -> bool:
        return self._value == None


    """
    """
    def get(self):
        return self._value

    """
    """
    def once(self):
        value = self._value
        self._value = None
        return value

# // class Option

"""
"""
def none() -> Option:
    return Option(None)


"""
"""
def some(value) -> Option:
    return Option(value)
