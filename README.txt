DEVEL:
mkvirtualenv alloallo
pip install -r requirements/local.txt
cp alloallo/alloallo/settings/local_template.py alloallo/alloallo/settings/local.py
python manage.py migrate

python manage.py runserver

DEPLOY:
