class StorageError(Exception):
    pass


class ImageNotFoundError(StorageError):
    pass


class StorageUnavailableError(StorageError):
    pass