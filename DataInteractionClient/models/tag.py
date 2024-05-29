from typing import Optional, Union


class Tag:
    """
    Класс, представляющий метаданные, связанные с источником данных.

    Атрибуты
    ----------
    id : str, dict
        Уникальный идентификатор тега.
        Может быть представлен в виде строки или словаря:
          {
              "tagName": "tag name",
              "parentObjectId": "object id"
          }
    parentObjectId: str
        Заполняется при наличии. По умолчанию пустая строка.
    attributes : dict
        Атрибуты тега.
    data : list
        Массив данных тэга

    Методы
    -------
    add_data(x: Union[str, int], y: int, q: Optional[int] = 0)
        Добавляет данные к тегу.
    clear_data
        Очищает данные тега.
    """

    def __init__(self, tag_id: Union[str, dict], attributes: dict, data: list = None):
        """
        Инициализирует экземпляр класса Tag.

        Параметры
        ----------
        tag_id : Union[str, dict]
            Идентификатор тега. Если это словарь, он должен содержать ключи 'tagName' и 'parentObjectId'.
        attributes : dict
            Атрибуты тега.
        data : list, опционально
            Массив данных тега. По умолчанию None.

        Ошибки, исключения:
        KeyError
            Если в словаре отсутствуют ключи 'tagName' и 'parentObjectId'.
        """
        if isinstance(tag_id, dict):
            try:
                self.id = tag_id["tagName"]
                self.parent_object_id = tag_id["parentObjectId"]
            except KeyError:
                raise KeyError("Необходимо указать ключи 'tagName' и 'parentObjectId'")
        else:
            self.id = tag_id
            self.parent_object_id = ""
        self.attributes = attributes
        self.data = data

    def add_data(self, x: Union[str, int], y: int, q: Optional[int] = 0):
        """
        Добавляет данные тега.

        Возвращает
        -------
        None
            Эта функция не возвращает никаких значений. Она изменяет атрибут 'data' экземпляра класса.
        """
        if self.data is None:
            self.data = []
        data = {
            "x": x,
            "y": y,
            "q": q,
        }
        self.data.append(data)

    def clear_data(self):
        """
        Очищает данные тега.

        Возвращает
        -------
        None
            Эта функция не возвращает никаких значений. Она изменяет атрибут 'data' экземпляра класса.
        """
        self.data = None
