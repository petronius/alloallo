# Allo Allo

Social networking for people who find it easier to use traditional telephone calls rather than a web/computer interface.

Django 1.8, Python 3, Twilio, and Braintree payments.

## Starting the app
```bash
$ git clone https://github.com/petronius/alloallo.git
$ mkvirtualenv alloallo
$ pip install -r requirements/local.txt
$ cp alloallo/alloallo/settings/local_template.py alloallo/alloallo/settings/local.py
$ python manage.py migrate
$ python manage.py runserver
```
