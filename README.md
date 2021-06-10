# Проектная работа 8 спринта

# 2 спринт
Лайки, коменты, отмеченные

## Запуск

Для запуска проекта в docker-compose:

```shell
make run
```

После этого будут запущены приложения movie_api, ugc.
Через 60 секунд будет запущен etl сервис для movie_api (чтобы ES успел стартовать)

> Если etl так и не запустится, то через некоторое время запустите его вручную:
```make run_etl```

Структуру API ugc сервиса можно посмотреть по:
[http://localhost:8000/swagger](http://localhost:8000/swagger)

> Только авторизованные пользователи могут лайкать и коментировать фильмы.

## Примеры

**Лайкнуть фильм:**

```shell
curl -L -XPOST -d '{"toggle": "true"}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzI1Mzk2MiwianRpIjoiY2NhNWU4NTItMmIxNy00MmFkLWI2ZDYtNjUzZmJhMTIyZTQ0IiwibmJmIjoxNjIzMjUzOTYyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiMzg3MzI4NTctZjAzOC00ZGE1LWEwYjMtMWI2MWUzZDQ5N2YxIiwiZXhwIjo5OTczNzU0ODYyLCJwZXJtaXNzaW9ucyI6WyJzdXNwaWNpb3VzOnJlYWQiLCJyb2xlOndyaXRlIl0sImRldmljZSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNC4wLjMgU2FmYXJpLzYwNS4xLjE1In0.S2L5mrmlcsvFPQWEl3r62MVfYs5HyvS6rVFWUkGjahhwSUqsuAxDsmGUfP6LqRTEYqCn4V3v1FPo7dCo7A_VvEtfL02KFFIMN8vbpcoL7TPALhOMj5i0ldBsxP52y7L4NelrdUNwn0zOxVJdAne66OpaFXPwxZFawISmMl-EWehMtcB2-p9eKCmSntGlqJt4hHSIdAwVS4mHgW3Cl3Hwjr0sKptf_3JPHtcNvcJWikBiR0rxWLyN5tPSQj60HXlzhBKGjUEobu0hjBhY_vKmA25wFIK9dwH07YRmV8SBnkAxQ5s97GzPzvpPo8xD8raB8iDnX36pwW4T1JHdGewNDQ' \
'http://127.0.0.1:8000/movie/02e89d35-02cb-4ac7-85cc-6be241fd3b8d/likes'
```

**Оставить коментарий к фильму:**
```shell
curl -L -XPOST -d '{"content": "Самый лучший фильм!"}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzI1Mzk2MiwianRpIjoiY2NhNWU4NTItMmIxNy00MmFkLWI2ZDYtNjUzZmJhMTIyZTQ0IiwibmJmIjoxNjIzMjUzOTYyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiMzg3MzI4NTctZjAzOC00ZGE1LWEwYjMtMWI2MWUzZDQ5N2YxIiwiZXhwIjo5OTczNzU0ODYyLCJwZXJtaXNzaW9ucyI6WyJzdXNwaWNpb3VzOnJlYWQiLCJyb2xlOndyaXRlIl0sImRldmljZSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNC4wLjMgU2FmYXJpLzYwNS4xLjE1In0.S2L5mrmlcsvFPQWEl3r62MVfYs5HyvS6rVFWUkGjahhwSUqsuAxDsmGUfP6LqRTEYqCn4V3v1FPo7dCo7A_VvEtfL02KFFIMN8vbpcoL7TPALhOMj5i0ldBsxP52y7L4NelrdUNwn0zOxVJdAne66OpaFXPwxZFawISmMl-EWehMtcB2-p9eKCmSntGlqJt4hHSIdAwVS4mHgW3Cl3Hwjr0sKptf_3JPHtcNvcJWikBiR0rxWLyN5tPSQj60HXlzhBKGjUEobu0hjBhY_vKmA25wFIK9dwH07YRmV8SBnkAxQ5s97GzPzvpPo8xD8raB8iDnX36pwW4T1JHdGewNDQ' \
'http://127.0.0.1:8000/movie/02e89d35-02cb-4ac7-85cc-6be241fd3b8d/likes'
```

**Чтобы проверить данные о лайках и коментах в БД произведите запросы:**
```shell
docker-compose exec postgres psql -U postgres -d practikum -c 'select * from likes'
```
```shell
docker-compose exec postgres psql -U postgres -d practikum -c 'select * from comments'
```

# 1 спринт

Проект содержит 2 сервиса: сервис аналитики и ETL сервис.

### Сервис аналитики
Принимает запросы от клиентов и сохраняет данные в Kafka.

### ETL сервис
Отправляет данные из Kafka в CLickhouse.

<hr>
Оба сервиса используют один общий docker-compose файл, но между собой они разделены.

## Развертывание
1. Для каждого сервиса требуется прописать переменные в .env файле рядом с директорий src.  
Пример переменных можно найти в example.env.

2. Создать сеть `ugc`:
   ```shell
   docker-network create ugc
    ```
3. Построить контейнеры:
    ```shell
    docker-compose build
    ```
   
4. Поднять контейнеры
    ```shell
    docker-compose up
    ```


<hr>

### Примеры запросов:
Создать событие об истории просмотра фильма:
```shell
curl --location --request POST 'http://127.0.0.1:8000/collect' \
--header 'Content-Type: application/json' \
--data-raw '{
    "payload": {
        "movie_timestamp": 1621932759,
        "movie_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2",
        "user_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2"
    },
    "timestamp": 1,
    "language": "RU",
    "timezone": "Europe/Moscow",
    "fingerprint": {},
    "ip": "192.168.1.1",
    "type": "history",
    "version": "1.1"
}'
```