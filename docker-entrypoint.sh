sleep 5

source .env

#uwsgi -i main.ini
python manage.py runserver 0.0.0.0:8000 &
sleep infinity