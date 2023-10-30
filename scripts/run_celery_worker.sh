#!/bin/bash
run_command="poetry run celery -A src.dj_project worker -Q hello1,noti1.exchange -l INFO -B"

echo "$run_command"
eval $run_command
