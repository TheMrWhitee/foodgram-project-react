# Продуктовый помощник
Проект Foodgram позволяет добавлять на сайт рецепты, подписываться на интересные рецепты или авторов, 
добавлять рецепты в корзину и скачивать, автоматически сформированный, список продуктов для приготовления выбранных блюд.
Можно использовать в качестве персональной поваренной книги, чтобы не потерять понравившиеся рецепты и не записывать их по старинке в тетрадку или добавлять в закладки браузера))
***
## Стек технологий
Python 3.7+, Django 3.1+, Django REST Framework, Djoser, Docker, Docker-compose, GitHub Actions, React
***
## Установка
#### После клонирования репозитория перейдите в каталог infra/, соберите и запустите проект командой:
    sudo docker-compose up --build

### Следующие команды выполняются в новом окне терминала в этом же каталоге.
#### Создайте и примените миграции:
    sudo docker exec -it infra_backend_1 python manage.py makemigrations
    sudo docker exec -it infra_backend_1 python manage.py migrate

#### Соберите статику:
    sudo docker exec -it infra_backend_1 python manage.py collectstatic

#### Создайте суперпользователя:
    sudo docker exec -it infra_backend_1 python manage.py createsuperuser

#### Загрузите в базу данных список ингредиентов для будущих рецептов:
    sudo docker exec -it infra_backend_1 bash
    python loaddata.py < ingredients.csv

Документация на API будет доступна по адресу /api/docs/redoc.html

Для ознакомления приложение запущено по адресу: http://foodgramyndx.co.vu/recipes

![example workflow](https://github.com/TheMrWhitee/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
