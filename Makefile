app_name            ?=
project_name        ?=
ZIP_FILE_NAME       :=
APPLICATION_NAME    :=
APP_PLAN            := B1
STORAGE_PLAN        := Standard_LRS
STORAGE             := $(shell cat .env | grep STORAGE | cut -d '=' -f2)
PYTHON_VERSION      := $(shell cat .env | grep PYTHON_VERSION | cut -d '=' -f 2)
LOCATION            := $(shell cat .env | grep LOCATION | cut -d '=' -f 2)
RESOURCE_GROUP      := $(shell cat .env | grep RESOURCE_GROUP | cut -d '=' -f2)


run:
	@python manage.py runserver

install:
	@brew install azure-cli

setup:
	@python3 -m venv .venv         \
	&& source ./.venv/bin/activate \
	&& pip install --upgrade pip   \
	&& pip install -r requirements.txt

migrate:
	@python manage.py migrate

startproject:
	@django-admin startproject $(project_name) .                                                          \
	&& sed -e 's/<project-name>/$(project_name)/g' ./manage.tpl > manage.bak                              \
	&& mv manage.bak manage.py                                                                            \
	&& sed -e 's/<project-name>/$(project_name)/g' ./production.tpl > ./production.bak                    \
	&& mv ./production.bak ./production.py                                                                \
	&& mv ./production.py ./$(project_name)                                                               \
	&& sed -e 's/<project-name>/$(project_name)/g' ./wsgi.tpl > ./wsgi.bak                                \
	&& mv ./wsgi.bak ./wsgi.py                                                                            \
	&& mv ./wsgi.py ./$(project_name)                                                                     \
	&& sed -e "s/^        'DIRS': \[\],/\t\t'DIRS': \[BASE_DIR \/ 'templates'\],/g" ./$(project_name)/settings.py \
	> ./$(project_name)/settings.bak                                                                      \
	&& mv ./$(project_name)/settings.bak ./$(project_name)/settings.py                                    \
	&& echo "\nSTATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)" >> ./$(project_name)/settings.py

startapp:
	@python manage.py startapp $(app_name)

makemigrations:
	@python manage.py makemigrations

createsuperuser:
	@python manage.py createsuperuser

group:
	@az group create         \
	--name $(RESOURCE_GROUP) \
	--location $(LOCATION)

storage:
	@az storage account create         \
    --name $(STORAGE)                  \
	--resource-group $(RESOURCE_GROUP) \
    --sku $(STORAGE_PLAN)

create:
	@az webapp up                          \
		--runtime PYTHON:$(PYTHON_VERSION) \
		--sku $(APP_PLAN)                  \
		--logs                             \
		--name $(APPLICATION_NAME)         \
		--resource-group $(RESOURCE_GROUP)

config:
	@az webapp config appsettings set      \
		--resource-group $(RESOURCE_GROUP) \
		--name $(APPLICATION_NAME)         \
		--settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

deploy:
	@zip -r $(ZIP_FILE_NAME).zip . -x '.??*' \
	&& az webapp deploy                      \
		--name $(APPLICATION_NAME)           \
		--resource-group $(RESOURCE_GROUP)   \
		--src-path $(ZIP_FILE_NAME).zip      \
		--type zip

azure-setup:
	@make group     \
	&& make storage \
	&& make create  \
	&& make config  \
	&& make deploy
