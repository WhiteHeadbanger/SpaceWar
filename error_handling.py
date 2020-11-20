# Error handling classes

class OutOfEnergy(Exception):
    """
    Defines error class for out of energy exception

    :param: message = message printed
    """

    def __init__(self, message="Your ship is out of energy resource!"):
        self.message = message
        super().__init__(self.message)

class OutOfFuel(Exception):
    """
    Defines error class for out of fuel exception

    :param: message = message printed
    """

    def __init__(self, message="Your ship is out of fuel!"):
        self.message = message
        super().__init__(self.message)

class OutOfLimitsScan(Exception):
    """
    Defines error class for out of scanner limits

    :param: message = message printed
    """

    def __init__(self, message="Your scan can't reach that far!"):
        self.message = message
        super().__init__(self.message)

class MovementRangeExceeded(Exception):
    """
    Defines error class for movement limits

    :param: message = message printed
    """

    def __init__(self, message="Your ship can't reach that far!"):
        self.message = message
        super().__init__(self.message)

class NoModuleActive(Exception):
    """
    Defines error class for modules

    :param: message = message printed
    """

    def __init__(self, message="Error: module is inactive or destroyed"):
        self.message = message
        super().__init__(self.message)
