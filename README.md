# Проект Financial Risks Scoring
Проект "Скоринг финансовых рисков" - это веб-приложение, которое позволяет расчитать рейтинг и уровень риска страхователя по заявкам на страхование гражданско-правовой ответственности (т.н. продукт "Финансовые риски"). 

## Домен
<!-- https://kareits.com/
https://51.250.111.36/ -->

## Инструкция как разернуть в Docker

- Загрзуить образы с хаба
`sudo docker compose -f docker-compose.production.yml pull`

- Остановить контейнеры и удалить их
`sudo docker compose -f docker-compose.production.yml down`

- Запустить контейнеры на основе образов
`sudo docker compose -f docker-compose.production.yml up -d`


## Основной стек технологий

- Python 3.9
- Django 3.2.3
- pandas
- CSS
- Bootstrap 5

## Как подготовить базу данных
- Сделать миграции
`sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations`

- Применить миграции
`sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate`

- Создать суперпользователя
`sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser`

- Собрать статику
`sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput`

## Ресурсы Financial Risks Scoring
**auth/login/**: аутентификация зарегистрированного пользователя.

**auth/password_change/**: смена пароля для аутентифицированного пользователя.

**index/**: домашняя страница с реестром запросов на скоринг, которые сделал аутентифицированный пользователь.

**make_request/**: сделать запрос на скоринг путем загрузки анкеты в формате Excel.

**requests/<int:pk>/**: получить детали запроса с расчитанным скорингом и уровнем риска, а также с возможностью скачать отчет по скорингу в формате pdf.

**company/**: поиск компании по БИН в базе данных и вывод наименования компания, если найдено.


## Роли пользователей
**Аутентифицированный пользователь (user)** — доступна главная страница с реестром запросов, страница для смены пароля, страница для отправки запроса на скоринг, страница для поиска компании по БИН.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым.

## Использование
- Использовать приложение могут только зарегистрированные и аутентифицированные пользователи - сотрудники АО "СК "Jusan Garant"
- Создание и редактирование пользователей, сбор паролей пользователей осуществляется только Администраторами.

## Авторство
Игорь Ли aka kareits# jusan_credit_scoring
