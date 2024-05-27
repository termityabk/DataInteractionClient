from typing import List, Optional, Union

import requests
from exceptions.DataSourceNotActiveException import DataSourceNotActiveException
from models.RequestData import RequestData
from models.Tag import Tag


class DataInteractionClient:
    """
    Класс, представляющий клиент взаимодействия с источниками данных.

    Атрибуты
    ----------
    base_url : str
        Базовый URL платформы.

    Методы
    -------
    connect(data_source_id: str)
        Подключается к источнику данных с указанным идентификатором.
    set_data(tags: list)
        Отправляет данные для указанных тегов.
    get_data(from_time, to_time, tag_id: list, max_count: int, time_step: int, value, format_param: bool = None, actual: bool = True)
        Получает данные для указанных параметров.
    create_tags(tags_data: list)
        Создает экземпляры тегов из предоставленных данных.
    _make_request(url: str, params: dict)
        Выполняет HTTP-запрос к указанному URL с указанными параметрами.
    """

    def __init__(self, base_url):
        """
        Инициализирует новый экземпляр класса Client.

        Параметры:
        ----------
        base_url : str
            Базовый URL платформы.

        Возвращает:
        -------
        None
        """
        self.base_url = base_url

    def connect(self, data_source_id: str):
        """
        Подключение к необходимому источнику данных и сбор метаданных источника.

        Параметры:
        data_source_id (str): Идентификатор источника данных для подключения.

        Возвращает:
        dict: Ответ сервера в формате JSON.

        Ошибки, исключения:
        ValueError: Если data_source_id не является строкой.
        DataSourceNotActiveException: Если источник данных неактивен.
        """
        if not isinstance(data_source_id, str):
            raise ValueError("data_source_id ожидаемый тип параметра [str]")
        url = f"{self.base_url}/smt/dataSources/connect"
        params = {"id": data_source_id}
        response = self._make_request(url, params)
        if response.json()["attributes"]["smtActive"]:
            return response.json()
        else:
            raise DataSourceNotActiveException()

    def set_data(self, tags: list):
        """
        Отправляет данные тегов на сервер.

        Параметры:
        tags (list): Список объектов Tag. Каждый объект Tag имеет атрибуты 'id' и 'data'.

        Возвращает:
        dict: Ответ сервера в формате JSON.

        Ошибки, исключения:
        requests.exceptions.RequestException: Если во время запроса произошла ошибка.
        Подробнее:
        https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/
        """
        url = f"{self.base_url}/smt/data/set"
        data = [{"tagId": tag.id, "data": tag.data} for tag in tags]
        response = self._make_request(url, {"data": data})
        return response.json()

    def get_data(self, requests_data: RequestData):
        """
        Получает исторические данные для указанных параметров.

        Параметры:
        ----------
        requests_data (RequestData): Объект, содержащий данные запроса.

        Возвращает:
        ----------
        dict: Ответ сервера в формате JSON.

        Ошибки, исключения:
        requests.exceptions.RequestException: Если во время запроса произошла ошибка.
        Подробнее:
        https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/
        """
        url = f"{self.base_url}/smt/data/get"
        params = {
            "from": requests_data.from_time,
            "to": requests_data.to_time,
            "tagId": requests_data.tag_id,
            "maxCount": requests_data.max_count,
            "timeStep": requests_data.time_step,
            "format": requests_data.format_param,
            "actual": requests_data.actual,
            "value": requests_data.value,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(url, {"params": params})
        return response.json()

    def create_tags(self, tags_data: list):
        """
        Создает экземпляры тегов из предоставленных данных.

        Параметры:
        ----------
        tags_data : list
            Список словарей, каждый из которых представляет данные тега.
            Каждый словарь должен содержать ключи 'id' и 'attributes'.

        Возвращает:
        ----------
        list
            Список созданных экземпляров тегов.
        """
        return [Tag(item["id"], item["attributes"]) for item in tags_data]

    def create_request_data(
        self,
        tag_id: Union[str, List[str]],
        from_time: Optional[Union[str, int]] = None,
        to_time: Optional[Union[str, int]] = None,
        max_count: Optional[int] = None,
        time_step: Optional[int] = None,
        value: Optional[Union[type, List[type]]] = None,
        format_param: Optional[bool] = None,
        actual: Optional[bool] = None,
    ) -> RequestData:
        """
        Метод создания словаря с данными для запроса.

        Параметры:
        tag_id : Union[str, List[str]], обязательно
            Массив идентификаторов тэгов, для которых запрашиваются данные.
        from_time : Union[str, int], необязательно
            Временная метка начала запрашиваемого периода. По умолчанию — None.
        to_time : Union[str, int], необязательно
            Временная метка конца запрашиваемого периода. По умолчанию — None.
        max_count: int, необязательно
            Максимальное количество данных в ответе. По умолчанию — None.
        time_step: int, необязательно
            Шаг времени между соседними возвращаемыми значениями, микросекунды. По умолчанию — None.
        value: Union[type, List[type]], необязательно.
            Фильтр по значению. По умолчанию — None.
        format_param: bool, необязательно
            Если ключ присутствует и не равен None, то метки времени
            в ответе будут конвертированы в строки согласно формату ISO 8601, временная зона
            будет соответствовать временной зоне, установленной на сервере, на котором работает
            платформа. По умолчанию — None.
        actual: bool, необязательно
            Возвращает только реально записанные в базу данных значения, неинтерполированные. По умолчанию — None.


        Возвращает:
        obj: Объект RequestData который содержит в себе атрибуты для запроса исторических данных.
        """
        request_data = {
            "tag_id": tag_id,
            "from_time": from_time,
            "to_time": to_time,
            "max_count": max_count,
            "time_step": time_step,
            "value": value,
            "format_param": format_param,
            "actual": actual,
        }

        return RequestData(request_data)

    def _make_request(self, url: str, params: dict):
        """
        Выполняет POST-запрос по указанному URL-адресу с предоставленными параметрами.

        Параметры:
        url (str): URL-адрес для отправки запроса.
        params (dict): параметры, которые нужно отправить вместе с запросом.

        Возвращает:
        Requests.Response: ответ от сервера.

        Ошибки, исключения:
        Requests.Exceptions.RequestException: Если в запросе возникла ошибка.
        """
        try:
            response = requests.post(url, params=params, timeout=5)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Ошибка запроса: {e}") from e
