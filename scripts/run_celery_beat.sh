#!/bin/bash
run_command="poetry run celery -A src.dj_project worker -Q hello,noti.exchange -l INFO"

echo "$run_command"
eval $run_command
