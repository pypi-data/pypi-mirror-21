class LockError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Storage '" + self.name + "' is locked!"
