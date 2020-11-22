##  PLEASE READ README.md FILE AND EDIT config.py and create a .env file from .env.example


## STARTING UP WITHOUT DOCKER

## 1.SETTING UP
## Download python
www.python.org/downloads

## Creating a virtual environment (optional)
python -m venv env

## Connecting to a virtual env
source <path to activate file>

## Installing requirements
pip install -r requirements.txt

## Running tests

python tests.py




## STARTING UP WITH DOCKER


docker build .

sudo docker-compose up

docker-compose run web python manage.py createsuperuser


