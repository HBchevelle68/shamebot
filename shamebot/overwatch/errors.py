
class InvalidHeroNameError(Exception):
    """Raise when hero name passed not found in dictionary"""
    type = "InvalidHeroNameError"
class EmptyAccountStringError(Exception):
    """Raise account string is empty"""
    type = "EmptyAccountStringError"
