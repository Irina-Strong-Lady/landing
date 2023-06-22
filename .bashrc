# production
# export APP_CONFIG=production
# export DATABASE_URL='mysql://u2105133_mysql:swordfish1@localhost:3306/u2105133_mysql'
# python manage.py db upgrade

#development
# export DATABASE_URL='mysql://root:swordfish1@localhost:3306/mysql_dev'
python manage.py db upgrade
python manage.py runserver -h 172.28.29.118 -p 8000 -d -r