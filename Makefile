app_name            ?=
project_name        ?=
plan                := B1
version             := 3.9
zip_file_name       :=
application_name    :=
resource_group_name :=

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

create:
	@az webapp up                   \
		--runtime PYTHON:$(version) \
		--sku $(plan)               \
		--logs                      \
		--name $(application_name)  \
		--resource-group $(resource_group_name)

config:
	@az webapp config appsettings set           \
		--resource-group $(resource_group_name) \
		--name $(application_name)              \
		--settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

deploy:
	@zip -r $(zip_file_name).zip . -x '.??*'    \
	&& az webapp deploy                         \
		--name $(application_name)              \
		--resource-group $(resource_group_name) \
		--src-path $(zip_file_name).zip         \
		--type zip
