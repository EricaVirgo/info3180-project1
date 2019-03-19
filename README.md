# Project 1
Starter code for Project 1

https://docs.sqlalchemy.org/en/latest/core/defaults.html

sudo service postgresql start

sudo sudo -u postgres psql
create user "project1";
create database "project1";

python flask-migrate.py db init
python flask-migrate.py db migrate
python flask-migrate.py db upgrade

