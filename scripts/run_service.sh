#!/bin/bash
# for docker container
# run with env file /noti_service/envs/.env

base_dir=$(pwd)
config_path="$base_dir/configs"

cmd_collectstatic="poetry run python manage.py collectstatic --noinput"
cmd_migrations="poetry run python manage.py makemigrations"
cmd_migrate="poetry run python manage.py migrate"
run_command="poetry run gunicorn -c $config_path/gunicorn_config.py src.dj_project.wsgi"


echo "$cmd_collectstatic"
eval $cmd_collectstatic

echo "$cmd_migrations"
eval $cmd_migrations

echo "$cmd_migrate"
eval $cmd_migrate

echo "$run_command"
eval $run_command
