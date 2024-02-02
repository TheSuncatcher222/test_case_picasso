# Picasso

Тестовое задание: Загрузка и обработка файлов

### Цель

Разработать Django REST API, который позволяет загружать файлы на сервер, а затем асинхронно обрабатывать их с использованием Celery.

### Требования

- ✅ Создать Django проект.
- ✅ Использовать Django REST Framework для создания API.
- ✅ Реализовать модель File, которая будет представлять загруженные файлы. Модель должна содержать поля:
  - file: поле типа FileField, используемое для загрузки файла;
  - uploaded_at: поле типа DateTimeField, содержащее дату и время загрузки файла;
  - processed: поле типа BooleanField, указывающее, был ли файл обработан.
- ✅ Реализовать сериализатор для модели File.
- ✅ Создать API эндпоинт upload/:
  - принимает POST-запросы для загрузки файлов;
  - при загрузке файла необходимо создать объект модели File, сохранить файл на сервере;
  - запустить асинхронную задачу для обработки файла с использованием Celery;
  - в ответ на успешную загрузку файла вернуть статус 201 и сериализованные данные файла.
- ✅ Реализовать Celery задачу для обработки файла:
  - задача должна быть запущена асинхронно
  - изменять поле processed модели File на True после обработки файла.
- ✅ Реализовать API эндпоинт files/:
  - возвращает список всех файлов с их данными, включая статус обработки.

### Дополнительные требования

- ✅ Использовать Docker для развертывания проекта.
- ✅ Реализовать механизм для обработки различных типов файлов (например, изображений, текстовых файлов и т.д.).
- ✅ Предусмотреть обработку ошибок и возвращение соответствующих кодов статуса и сообщений об ошибках.

### Усложнения

- Тесты (постарайтесь достичь покрытия в 70% и больше)
- Опишите, как изменится архитектура, если мы ожидаем большую нагрузку
- Попробуйте оценить, какую нагрузку в RPS сможет выдержать ваш сервис

Ответы к комментариям:
1) Тесты
Я люблю работать с Pytest.
Не проводил тесты библиотек.

2) Как изменится архитектура.
Все-таки Python - это не совсем про параллельное выполнение задач. Особенно в совокупности с синхронным Django.
При огромной нагрузке необходимо будет создавать отдельный сервер со своим брокером сообщений, на который Django будет присылать запросы.
Желательно на C++/Go языках, которые больше приспособлены к тяжелым парарлельным задачам.
Ну или Python в режиме многопроцессорного использования (но не многопоточного, GIL все сведет на нет, и просто замедлит сервер).
PostgreSQL можно оставить, так как он поддерживает асинхронный доступ и не будет узким горлом. Я уже использовал asyncpg - полет нормальный.

3) Попробуйте оценить, какую нагрузку нагрузку в RPS выдержит сервис.
Это очень неоднозначный вопрос. Все зависии от количества серверов, от количества воркеров Gunicorn.
От самого критерия для фиксации "отказа нагрузки".
Из документации Gunicorn:
`Gunicorn should only need 4-12 worker processes to handle hundreds or thousands of requests per second.`
Django также не сильно нагружен, только принять и сохранить.
Страдать будут именно фоновые задачи при широком развитии.
При этом данный аспект сильно зависит и от конфигурации сервера.
Существуют сервисы по нагрузочному тестированию, которые могут по факту показать результаты.
В данном случае запросы выполняются условно не более чем в 100 миллисекунд, тогда при терпимо ожидании в 5 секунд, можно синхронно обработать не менее 50_000 запросов.


### Развертка

1) Загрузить актуальную версию проекта

```
git clone git@github.com:TheSuncatcher222/test_case_picasso.git
```

2) Перейти в папку app

```
cd test_case_picasso/app
```

3) Создать файл переменных окружения из примера

```
cp .env.example .env
```

4) Изменить переменные окружения (если необходимо)
```
(на примере редактора Nano)
nano .env
```

5) Перейти в корневую папку проекта
```
cd ..
```

6) Запустить Docker (убедитесь, что `docker daemon` запущен в системе!)

```
docker-compose up --build -d
```

7) Проверить доступность проекта на `localhost:8000`

```
http://localhost:8000/
http://localhost:8000/docs/swagger/
```

8) Проверить тесты

```
docker compose exec backend_picasso bash
flake8
pytest
```
