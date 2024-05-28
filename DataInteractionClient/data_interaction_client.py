from typing import List, Optional, Union

import requests

from exceptions.server_response_error_exception import ServerResponseErrorException
from exceptions.data_source_not_active_exception import DataSourceNotActiveException
from models.tag import Tag


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

    def __init__(self, base_url: str):
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

    def connect(self, data_source_id: str) -> List[Tag]:
        """
        Подключение к необходимому источнику данных и сбор метаданных источника.

        Параметры:
        data_source_id (str): Идентификатор источника данных для подключения.

        Возвращает:
        ----------
        List[Tag]
            Список тегов.

        Ошибки, исключения:
        ValueError: Если data_source_id не является строкой.
        DataSourceNotActiveException: Если источник данных неактивен.
        """
        if not isinstance(data_source_id, str):
            raise ValueError("data_source_id ожидаемый тип параметра [str]")
        url = f"{self.base_url}/smt/dataSources/connect"
        params = {"id": data_source_id}
        response = self._make_request(url, params)
        if not response["attributes"]["smtActive"]:
            raise DataSourceNotActiveException()
        else:
            return self._create_tags(response['tags'])

    def set_data(self, tags: List[Tag]) -> str:
        """
        Отправляет данные тегов на платформу.

        Параметры:
        tags (List[Tag]): Список объектов Tag. Каждый объект Tag имеет атрибуты 'id' и 'data'.

        Возвращает:
        str: Сообщение об успешном добавлении данных.

        Ошибки, исключения:
        requests.exceptions.RequestException: Если во время запроса произошла ошибка.
        Подробнее:
        https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/
        """
        url = f"{self.base_url}/smt/data/set"
        data = [{"tagId": tag.id, "data": tag.data} for tag in tags]
        self._make_request(url, {"data": data})
        return "Данные успешно добавлены"

    def get_data(self, request_data: dict) -> List[dict]:
        """
        Получает исторические данные для указанных параметров.

        Параметры:
        ----------
        requests_data (dict): Словарь, содержащий данные запроса.

        Возвращает:
        ----------
        List[dict]: Массив данных соответствующих запросу.

        Ошибки, исключения:
        requests.exceptions.RequestException: Если во время запроса произошла ошибка.
        Подробнее:
        https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/
        """
        url = f"{self.base_url}/smt/data/get"
        params = {
            "from": request_data['from_time'],
            "to": request_data['to_time'],
            "tagId": request_data['tag_id'],
            "maxCount": request_data['max_count'],
            "timeStep": request_data['time_step'],
            "format": request_data['format_param'],
            "actual": request_data['actual'],
            "value": request_data['value'],
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(url, {"params": params})
        return response['data']

    def _create_tags(self, tags_data: List[dict]) -> List[Tag]:
        """
        Создает экземпляры тегов из предоставленных данных.

        Параметры:
        ----------
        tags_data : List[dict]
            Список словарей, каждый из которых представляет данные тега.
            Каждый словарь должен содержать ключи 'id' и 'attributes'.

        Возвращает:
        ----------
        List[Tag]
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
    ) -> dict:
        """
        Метод создания словаря с данными для запроса.

        Параметры:
        ----------
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
        ----------
        dict
            Объект RequestData который содержит в себе атрибуты для запроса исторических данных.
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
        return request_data

    def _make_request(self, url: str, params: dict) -> requests.Response:
        """
        Выполняет POST-запрос по указанному URL-адресу с предоставленными параметрами.

        Параметры:
        ----------
        url (str): URL-адрес для отправки запроса.
        params (dict): параметры, которые нужно отправить вместе с запросом.

        Возвращает:
        ----------
        Requests.Response: ответ от платформы.

        Ошибки, исключения:
        ----------
        Requests.Exceptions.RequestException: Если в запросе возникла ошибка.
        ServerResponseErrorException: Если в ответе платформы значение error['id] отлично от 0.
        """
        try:
            response = requests.post(url, params=params, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Ошибка запроса: {e}") from e
        error_response = response.json()["error"]
        if error_response["id"] != 0:
            raise ServerResponseErrorException(message= f"error_id: {error_response['id']} {error_response['message']}")
        return response.json()
