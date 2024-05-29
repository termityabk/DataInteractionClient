from typing import Optional


class NoDataToSendException(Exception):
    """
    Класс исключения, предназначенный для ситуаций, когда данные для отправки отсутствуют.

    Атрибуты:
    ----------
    message : str
        Сообщение об ошибке, по умолчанию "Нет данных для отправки".
    """

    def __init__(self, message: Optional[str] = "Нет данных для отправки."):
        self.message = message
        super().__init__(self.message)
