#!/usr/bin/env bash
rm -rf special_random/main/migrations; rm devel.sqlite;

python manage.py makemigrations main
python manage.py migrate
python manage.py createsuperuser --username root --email root@root.com --noinput
python manage.py changepassword root

python manage.py fake_cats

#python manage.py setloader set1.txt
python manage.py setloader ITG\ Moscow\ Tournament\ 3/


 while true; do python manage.py runserver 0.0.0.0:8000; sleep 2; done
