# Django Blank
Шаблон для Django проекта.

Version 1.0

## Содержание проекта

```
app/
```
Приложениями проекта

```
config/
```
Настройка проекта. 

```
requirements/
 ```
Описание окружения проекта

```
utils/
``` 

## Разворачивание проекта

### Настройки БД PostgreSQL

* Создание БД
```
CREATE DATABASE django_blank_db;
CREATE USER django_blank_user WITH password 'PASSWORD';
GRANT ALL ON DATABASE django_blank_db TO django_blank_user;
```

* Дамп БД
```
pg_dump -d django_blank_db -f file_dump
```

* Загрузить дамп в БД (БД необходимо перед этим создать)
```
psql -d django_blank_db -f file_dump
```


### Запуск тестов с coverage:
```
coverage run --source='.' --omit 'env/*'  manage.py test
```

### Настройки окружения для разных версий Python

* Установить PyEnv
``` 
https://github.com/pyenv/pyenv-installer
```

* Export:
```
export PATH="/path.to.user/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
* Установить нужную версию Python 
```
pyenv install 3.7.1
```

* Создать виртуальное окружение с нужно версией Python: 
```
virtualenv -p ~/.pyenv/versions/3.7.1/bin/python3 name_env
```

### Установка mod_wsgi для apache2
Для разных версий python разные версии mod_wsgi.
Чтобы обновить спокойно mod_wsgi под конкретную версию python
нужно установить python  с помощью pyenv с shared_libs:
```
CONFIGURE_OPTS=--enable-shared pyenv install 3.7.1
```
где 3.7.1 - нужная версия python

После того как установили python в pyenv нужно создать virtualenv:
```
virtualenv -p ~/.pyenv/versions/3.7.1/bin/python3 name_env
```

затем включаем это окружение и устанавливаем mod_wsgi:
```
pip install mod_wsgi
```

затем нужно настроить apache2:
```
https://pypi.org/project/mod_wsgi/
```
Раздел: Connecting into Apache installation

Пример содежимого файла mod_wsgi для Apache2
```
LoadModule wsgi_module /home/bva/env_apache2_wsgi/lib/python3.7/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-x86_64-linux-gnu.so
WSGIPythonHome /home/bva/env_apache2_wsgi
```


После чего нужно только настроить apache2