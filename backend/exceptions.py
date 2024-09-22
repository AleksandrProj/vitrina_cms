class UsageException(ValueError):
    """Исключение, если пользователь пытается удалить используемый объект"""

    def __init__(self, message):
        self.message = message