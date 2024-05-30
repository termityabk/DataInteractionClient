# DataInteractionClient

Клиент взаимодействия с источниками данных
Python пакет, который предоставляет коннекторам клиент для взаимодействия с платформой.
Коннектор собирает данные и при помощи клиента отправляет их во внутреннюю систему (в платформу).
Взаимодействие с платформой происходит через HTTP API.

## Этапы работы клиента взаимодействия с источниками данных:

- Инициализация, в ходе которой происходит подключение к необходимому источнику данных и сбор метаданных источника.

```python
from DataInteractionClient import DataInteractionClient

client = DataInteractionClient("http://0.0.0.0:8000")
    # Создание экземпляра класса клиента.
    # Принимает базовый URL-адрес платформы.

tags = client.connect("1")
    # Подключение к платформе данных, используя метод подключения клиента.
    # Метод проверяет существование указанного источника данных и возвращает список тэгов,
    # в которые коннектор должен записывать данные. В случае, если источник данных неактивен,
    # то выбрасывается исключение и список тэгов не возвращается.
```

- Отправка данных по требованию, как отдельными частями, так и объединенными группами.

```python
tags[0].add_data("2018-06-26 17:16:00", 5555, 1)
    # Добавление данных в тэг.
    # Обеспечивает накопление данных в объекте тега.

client.set_data(tags)
    # Отправка данных на платформу.
    # Принимает массив объектов Тег.
    # Возвращает сообщение об успешном добавлении данных или выбрасывает исключение.

tags[0].clear_data()
    # Очистка данных тэга.
    # Вызывается неявно каждый раз, когда отправка данных на платформу завершилась успешно.
```

- Получение данных по запросу коннектора.

```python
get = client.get_data(tag_id='fds', from_time='100', to_time=1000000, max_count=100, time_step=100000, format_param=True)
    # Получение данных с платформы, используя метод клиента.
    # Принимает данные для запроса.
    # Возвращает данные в виде списка словарей.
```

## Документация

```bash
# Запустит сервер и дополнительно откроет в веб-браузере индексную страницу модуля. На каждой обслуживаемой странице вверху есть панель навигации, где вы можете получить справку по отдельному элементу, выполнить поиск по всем модулям по ключевому слову в строке синопсиса и перейти на страницы «Указатель модулей» , «Темы» и «Ключевые слова» .
python -m pydoc -b
```

## Тестирование

```bash
# Запуск тестов
coverage run -m unittest discover

# Отчёт о тестовом покрытии
coverage report -m
```