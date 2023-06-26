# constant settings
export APP_ADMIN=iogontar@gmail.com
export MAIL_USERNAME=pravo@irina23.site
export MAIL_PASSWORD=swordfish1
export MAIL_SERVER=mail.irina23.site
export MAIL_PORT=587
export TELEBOT=5853561544:AAFOJg0BzxZJ5v4_6JSmP4hxzU0MgmafLjU

# production
export APP_CONFIG=production
export DATABASE_URL='mysql://u2105133_mysql:swordfish1@localhost:3306/u2105133_mysql'
python manage.py db upgrade

# development
# export DATABASE_URL='mysql://root:swordfish1@localhost:3306/mysql_dev'
# python manage.py db upgrade
# python manage.py runserver -h 0.0.0.0 -p 8000 -d -r