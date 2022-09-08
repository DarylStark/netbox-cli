class NetboxCLIException(Exception):
    """ Base class for exceptions """
    pass


class ConfigInstancesLastDeleted(NetboxCLIException):
    """ Error when a instance gets deleted that is the last """
    pass
