# hashing_login

Install requirements from requirements.txt with pip3 install -r requirements.txt

create a local postgres database and change the DATABASE_URL to your local 'postgresql:///<DB_NAME>'

run seed.py to populate tables and relationships

run a local flask server and connect to localhost:5000 or your preset connection

## Local Development
based off https://github.com/testdrivenio/flask-on-docker/tree/master

1. In an integrated terminal run `docker-compose up`
2. Visit 'http://localhost:5000'
3. TODO: Database does not seem to be connecting
