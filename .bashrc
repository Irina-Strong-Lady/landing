# export DATABASE_URL='mysql://root:swordfish1@localhost:3306/mysql_dev'
python manage.py db upgrade
# python manage.py runserver -h 172.22.137.212 -p 8000 -d -r