from typing import List, Union


class RequestData:
    """
    Класс представления аргументов для запроса исторических данных.
    Атрибуты
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
    Методы
    -------
    _validate_time(time: Union[str, int]) -> Union[str, int]
        Проверяет параметры времени.
    _validate_tag_id(tag_id: Union[str, List[str]]) -> Union[str, List[str]]
        Проверяет параметр tag_id.
    _validate_max_count(max_count: int) -> int
        Проверяет параметр max_count.
    _validate_time_step(time_step: int) -> int
        Проверяет параметр time_step.
    _validate_value(value: Union[type, List[type]]) -> Union[type, List[type]]
        Проверяет параметр value.
    """

    def __init__(self, data: dict):
        self.from_time = self._validate_time(data["from_time"])
        self.to_time = self._validate_time(data["to_time"])
        self.tag_id = self._validate_tag_id(data["tag_id"])
        self.max_count = self._validate_max_count(data["max_count"])
        self.time_step = self._validate_time_step(data["time_step"])
        self.value = self._validate_value(data["value"])
        self.format_param = data["format_param"]
        self.actual = data["actual"]

    def update(
        self,
        from_time: Union[str, int] = None,
        to_time: Union[str, int] = None,
        max_count: int = None,
        time_step: int = None,
        value: Union[type, List[type]] = None,
        format_param: bool = None,
        actual: bool = None,
    ):
        """
        Обновляет атрибуты экземпляра RequestData.

        Параметры:
        ----------
        from_time (Union[str, int]): Новое значение from_time.
        to_time (Union[str, int]): Новое значение to_time.
        max_count (int): Новое значение max_count.
        time_step (int): Новое значение time_step.
        value (Union[type, List[type]]): Новое значение value.
        format_param (bool): Новое значение format_param.
        actual (bool): Новое значение actual.
        """
        self.from_time = self._validate_time(from_time)
        self.to_time = self._validate_time(to_time)
        self.max_count = self._validate_max_count(max_count)
        self.time_step = self._validate_time_step(time_step)
        self.value = self._validate_value(value)
        self.format_param = format_param
        self.actual = actual

    def _validate_time(self, time: Union[str, int]) -> Union[str, int]:
        """
        Проверяет параметры временных меток.

        Параметры:
        ----------
        time (Union[str, int]): Проверяемая временная метка. Параметр может быть строкой или целым числом.

        Возвращает:
        ----------
        Union[str, int]: Валидированную временную метку. Если временная метка не None и не является строкой или целым числом,
                        возникает ValueError. В противном случае временная метка возвращается как есть.

        Ошибки, исключения:
        ValueError: Если временная метка не None и не является строкой или целым числом.
        """
        if time is not None and not isinstance(time, (str, int)):
            raise ValueError("Временная метка, ожидаемый тип параметра [str, int]")
        return time

    def _validate_tag_id(self, tag_id: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Проверяет параметр tag_id.

        Параметры:
        ----------
        tag_id (Union[str, List[str]]): Проверяемый tagId. Может быть строкой или списком строк.

        Возвращает:
        ----------
        Union[str, List[str]]: Валидированный tagId. Если tagId не является
                               строкой или списком строк, возникает ValueError. В противном случае,
                               введенный tagId возвращается как есть.

        Ошибки, исключения:
        ValueError: Если tagId не является строкой или списком строк.
        """
        if not isinstance(tag_id, (str, list)):
            raise ValueError("tag_id, ожидаемый тип параметра [str, list]")
        if isinstance(tag_id, list) and not all(
            isinstance(id, (str, dict)) for id in tag_id
        ):
            raise ValueError(
                "Для всех элементов массива тегов tag_id, ожидаемый тип параметра [str, dict]"
            )
        return tag_id

    def _validate_max_count(self, max_count: int) -> int:
        """
        Проверяет параметр max_count.

        Параметры:
        ----------
        max_count (int): Проверяемый max_count. Должен быть целым числом.

        Возвращает:
        ----------
        int: Валидированный max_count. Если max_count не является None и не является
             целым числом, возникает ValueError. В противном случае, введенный max_count возвращается как есть.

        Ошибки, исключения:
        ValueError: Если max_count не является None и не является целым числом.
        """
        if max_count is not None and not isinstance(max_count, int):
            raise ValueError("max_count, ожидаемый тип параметра [int]")
        return max_count

    def _validate_time_step(self, time_step: int) -> int:
        """
        Проверяет параметр time_step.

        Параметры:
        ----------
        time_step (int): Проверяемый time_step. Должен быть целым числом.

        Возвращает:
        ----------
        int: Валидированный time_step. Если time_step не является None и не является целым числом,
             возникает ValueError. В противном случае, введенный time_step возвращается как есть.

        Ошибки, исключения:
        ValueError: Если time_step не является None и не является целым числом.
        """
        if time_step is not None and not isinstance(time_step, int):
            raise ValueError("time_step, ожидаемый тип параметра [int]")
        return time_step

    def _validate_value(
        self, value: Union[type, List[type]]
    ) -> Union[type, List[type]]:
        """
        Проверяет параметр value.

        Параметры:
        ----------
        value (Union[type, List[type]]): Проверяемый value. Может быть типом или списком типов.

        Возвращает:
        ----------
        Union[type, List[type]]: Валидированный value. Если value не является None и не является
                                 одним типом или списком типов, возникает ValueError. В противном случае,
                                 введенное значение возвращается как есть.

        Ошибки, исключения:
        ValueError: Если value не является None и не является одним типом или списком типов.
        """
        if value is not None and not isinstance(value, (type, list)):
            raise ValueError(
                "value должен быть типом или массивом типов [type, List[type]]"
            )
        if isinstance(value, list) and not all(isinstance(v, type) for v in value):
            raise ValueError(
                "Каждый элемент массива значений value должен быть типом [type]"
            )
        return value
