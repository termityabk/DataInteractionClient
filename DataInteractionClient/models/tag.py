from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic.decorator import validate_arguments


class Tag(BaseModel):
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

    Ошибки, исключения:
    -------
    ValueError: Если структура id отличается от ожидаемой.
    """

    id: Union[str, Dict[str, str]]
    attributes: dict
    data: Optional[List[dict]] = None

    @validate_arguments
    def __init__(self, **kwargs: Union[str, dict]) -> None:
        if isinstance(kwargs.get("id"), dict):
            if set(kwargs["id"].keys()) != {"tagName", "parentObjectId"}:
                raise ValueError(
                    "Атрибут 'id' должен содержать ключи 'tagName' и 'parentObjectId'"
                )
        super().__init__(**kwargs)

    @validate_arguments
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
