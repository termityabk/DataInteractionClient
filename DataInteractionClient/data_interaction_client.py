from typing import List, Optional, Union

import httpx
from exceptions.data_source_not_active_exception import \
    DataSourceNotActiveException
from exceptions.no_data_to_send_exception import NoDataToSendException
from exceptions.server_response_error_exception import \
    ServerResponseErrorException
from models.tag import Tag
from pydantic import BaseModel
from pydantic.decorator import validate_arguments


class DataInteractionClient(BaseModel):
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
    set_data(tags: List[Tag])
        Отправляет данные для указанных тегов.
    get_data(tag_id: Union[str, dict, List[Union[str, dict]]],
        from_time: Optional[Union[str, int]] = None,
        to_time: Optional[Union[str, int]] = None,
        max_count: Optional[int] = None,
        time_step: Optional[int] = None,
        value: Optional[Union[type, List[type]]] = None,
        format_param: Optional[bool] = None,
        actual: Optional[bool] = None,)
        Получает данные для указанных параметров.
    _make_tags_list(tags_data: List[dict])
        Создает экземпляры тегов из предоставленных данных.
    _make_request(url: str, params: dict)
        Выполняет HTTP-запрос к указанному URL с указанными параметрами.
    _async_make_request(url: str, params: dict) -> httpx.Response
        Асинхронно выполняет HTTP-запрос к указанному URL-адресу с предоставленными параметрами.

    Ошибки, исключения:
    -------
    pydantic_core._pydantic_core.ValidationError: При несоответствии типов атрибутов.
        Подробнее см. https://docs.pydantic.dev/2.7/errors/validation_errors/
    httpx.HTTPStatusError: Если в запросе есть ошибка.
        Подробнее см. https://www.python-httpx.org/exceptions/
    httpx.RequestError: Если при выполнении запроса произошла ошибка.
        Подробнее см. https://www.python-httpx.org/exceptions/
    DataSourceNotActiveException: Если источник данных неактивен.
    NoDataToSendException: Если отсутствуют данные для запроса.
    ServerResponseErrorException: Если в ответе платформы значение error['id'] отлично от 0.
    """

    base_url: str

    @validate_arguments
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
        -------
        pydantic_core._pydantic_core.ValidationError: При несоответствии типов атрибутов.
            Подробнее см. https://docs.pydantic.dev/2.7/errors/validation_errors/
        httpx.HTTPStatusError: Если в запросе есть ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        httpx.RequestError: Если при выполнении запроса произошла ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        DataSourceNotActiveException: Если источник данных неактивен.
        """
        url = f"{self.base_url}/smt/dataSources/connect"
        params = {"id": data_source_id}
        response = self._make_request(url, params)
        if not response["attributes"]["smtActive"]:
            raise DataSourceNotActiveException()
        else:
            return self._make_tags_list(response["tags"])

    @validate_arguments
    def set_data(self, tags: List[Tag]) -> str:
        """
        Отправляет данные тегов на платформу.

        Параметры:
        -------
        tags (List[Tag]): Список объектов Tag. Каждый объект Tag имеет атрибуты 'id' и 'data'.

        Возвращает:
        -------
        None 
        При успешном добавлении данных ничего не возвращает.

        Ошибки, исключения:
        -------
        pydantic_core._pydantic_core.ValidationError: При несоответствии типов атрибутов.
            Подробнее см. https://docs.pydantic.dev/2.7/errors/validation_errors/
        httpx.HTTPStatusError: Если в запросе есть ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        httpx.RequestError: Если при выполнении запроса произошла ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        NoDataToSendException: Если отсутствуют данные для запроса.
        ServerResponseErrorException: Если в ответе платформы значение error['id'] отлично от 0.
        """
        url = f"{self.base_url}/smt/data/set"
        data = [
            {"tagId": tag.id, "data": tag.data} for tag in tags if tag.data is not None
        ]
        if not data:
            raise NoDataToSendException()
        else:
            self._make_request(url, {"data": data})
            for tag in tags:
                tag.clear_data()

    @validate_arguments
    def get_data(
        self,
        tag_id: Union[str, dict, List[Union[str, dict]]],
        from_time: Optional[Union[str, int]] = None,
        to_time: Optional[Union[str, int]] = None,
        max_count: Optional[int] = None,
        time_step: Optional[int] = None,
        value: Optional[Union[type, List[type]]] = None,
        format_param: Optional[bool] = None,
        actual: Optional[bool] = None,
    ) -> List[dict]:
        """
        Получает исторические данные для указанных параметров.

        Параметры:
        ----------
        Параметры:
        tag_id : Union[str, List[str]]
            Массив идентификаторов тэгов, для которых запрашиваются данные.
        from_time : Optional[Union[str, int]]
            Временная метка начала запрашиваемого периода. По умолчанию — None.
        to_time : Optional[Union[str, int]]
            Временная метка конца запрашиваемого периода. По умолчанию — None.
        Optional[int] = None,
            Максимальное количество данных в ответе. По умолчанию — None.
        time_step: Optional[int]
            Шаг времени между соседними возвращаемыми значениями, микросекунды. По умолчанию — None.
        value: Optional[Union[type, List[type]]]
            Фильтр по значению. По умолчанию — None.
        format_param: Optional[bool]
            Если ключ присутствует и не равен None, то метки времени
            в ответе будут конвертированы в строки согласно формату ISO 8601, временная зона
            будет соответствовать временной зоне, установленной на сервере, на котором работает
            платформа. По умолчанию — None.
        actual: Optional[bool]
            Возвращает только реально записанные в базу данных значения, неинтерполированные. По умолчанию — None.

        Возвращает:
        ----------
        List[dict]: Массив данных соответствующих запросу.

        Ошибки, исключения:
        -------
        pydantic_core._pydantic_core.ValidationError: При несоответствии типов атрибутов.
            Подробнее см. https://docs.pydantic.dev/2.7/errors/validation_errors/
        httpx.HTTPStatusError: Если в запросе есть ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        httpx.RequestError: Если при выполнении запроса произошла ошибка.
            Подробнее см. https://www.python-httpx.org/exceptions/
        ServerResponseErrorException: Если в ответе платформы значение error['id'] отлично от 0.
        """
        url = f"{self.base_url}/smt/data/get"
        params = {
            "from": from_time,
            "to": to_time,
            "tagId": tag_id,
            "maxCount": max_count,
            "timeStep": time_step,
            "format": format_param,
            "actual": actual,
            "value": value,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(url, {"params": params})
        return response["data"]

    @validate_arguments
    def _make_tags_list(self, tags_data: List[dict]) -> List[Tag]:
        """
        Создает список тегов из предоставленных данных.

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
        return [Tag(id=item["id"], attributes=item["attributes"]) for item in tags_data]

    @validate_arguments
    def _make_request(self, url: str, params: dict) -> httpx.Response:
        """
        Выполняет синхронный POST-запрос по указанному URL-адресу с предоставленными параметрами.

        Параметры:
        ----------
        url (str): URL-адрес для отправки запроса.
        params (dict): параметры, которые нужно отправить вместе с запросом.

        Возвращает:
        ----------
        httpx.Response: ответ от платформы.

        Ошибки, исключения:
        ----------
        httpx.HTTPStatusError: Если в запросе есть ошибка.
        httpx.RequestError: Если при выполнении запроса произошла ошибка.
        ServerResponseErrorException: Если в ответе платформы значение error['id] отлично от 0.
        """
        try:
            response = httpx.post(url, params=params, timeout=5)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(f"Ошибка запроса: {e}") from e
        except httpx.RequestError as e:
            raise httpx.RequestError(f"Ошибка при выполнении запроса: {e}")
        error_response = response.json()["error"]
        if error_response["id"] != 0:
            raise ServerResponseErrorException(
                message=f"error_id: {error_response['id']} {error_response['message']}"
            )
        return response.json()
