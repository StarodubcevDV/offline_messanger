class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserExistsException(Exception):
    pass


class DBUserNotExistsException(Exception):
    pass


class DBUserSenderNotExistsException(Exception):
    pass


class DBUserReceiverNotExistsException(Exception):
    pass


class DBMessageNotExistsException(Exception):
    pass
