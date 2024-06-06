import threading
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Tag(BaseModel):
    """
    Класс, представляющий метаданные, связанные с источником данных.
    Обеспечивает потокобезопасный способ изменения данных.

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
        Массив данных тега

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
    _lock: threading.Lock

    def __init__(self, **kwargs: Union[str, dict]) -> None:
        if isinstance(kwargs.get("id"), dict):
            if set(kwargs["id"].keys()) != {"tagName", "parentObjectId"}:
                raise ValueError(
                    "Атрибут 'id' должен содержать ключи 'tagName' и 'parentObjectId'"
                )
        super().__init__(**kwargs)

    def add_data(self, x: Union[str, int], y: int, q: Optional[int] = 0) -> None:
        """
        Добавляет данные тега.

        Возвращает
        -------
        None
            Не возвращает никаких значений. Она изменяет атрибут 'data' экземпляра класса.
        """
        self._lock = threading.Lock()
        with self._lock:
            if self.data is None:
                self.data = []
            data = {"x": x, "y": y, "q": q}
            self.data.append(data)

    def clear_data(self) -> None:
        """
        Очищает данные тега.

        Возвращает
        -------
        None
            Не возвращает никаких значений. Он изменяет атрибут 'data' экземпляра класса.
        """
        self._lock = threading.Lock()
        with self._lock:
            self.data = None
