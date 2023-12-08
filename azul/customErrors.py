class NotPlayersTurn(Exception):
    "Raised when wrong player tries to take tiles"
    pass

class EmptySourceOrWrongColour(Exception):
    "Source is either empty or does not have the requested colour"
    pass

class GameIsOver(Exception):
    "This game is already over"
    pass