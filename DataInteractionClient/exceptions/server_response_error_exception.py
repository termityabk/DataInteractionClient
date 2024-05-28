class ServerResponseErrorException(Exception):
    """
    Класс исключения, который вызывается при получении от сервера id ошибки отличном от "0".

    Атрибуты
    ----------
    message : str
        Сообщение об ошибке.

    """

    def __init__(self, message: str):
        self.message = f"Сервер вернул внутреннюю ошибку: {message}"
        super().__init__(self.message)
