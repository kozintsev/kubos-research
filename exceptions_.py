

# TODO: Move (some of) these exceptions into 'lib'


class KubosException(Exception):
    pass


class InvalidInputException(KubosException):
    pass


class ConstructionError(KubosException):
    """This error is raised if a geometric construction could not be performed.
    """
    pass
