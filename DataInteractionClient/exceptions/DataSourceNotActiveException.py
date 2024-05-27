class DataSourceNotActiveException(Exception):
    """
    Класс исключения, который вызывается, когда источник данных неактивен.

    Атрибуты
    ----------
    message : str
        Сообщение об ошибке, по умолчанию "Источник данных неактивен."

    """

    def __init__(self, message="Источник данных неактивен."):
        self.message = message
        super().__init__(self.message)
