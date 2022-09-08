class NetBoxCLIException(Exception):
    """ Base class for exceptions """
    pass


class ConfigInstancesLastDeleted(NetBoxCLIException):
    """ Error when a instance gets deleted that is the last """
    pass
