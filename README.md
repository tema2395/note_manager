# Note Manager


## Требования

- Python 3.12.2
- [Poetry](https://python-poetry.org/docs/#installation)

## Установка и запуск

### Шаг 1: Клон репозитория


Сначала клонируйте репозиторий и перейдите в директорию проекта:

```sh
git clone https://github.com/tema2395/note_manager
cd note_manager
```


### Шаг 2: Установка зависимостей

Установите зависимости и активируйте виртуальное окружение

```sh
poetry install
poetry shell
```

### Шаг 3: Запуск приложения

```sh
poetry run uvicorn note_manager.main:app --reload
```
## Эндпоинты

- `POST /notes/` - Создание новой заметки
- `GET /notes/` - Получение списка заметок
- `GET /notes/{note_id}` - Получение конкретной заметки по айди
- `DELETE /notes/{note_id}` -  Удаление заметки по айди
- `GET /notes/search/` - Поиск заметок по ключевому слову или фразе в заголовке или содержании.