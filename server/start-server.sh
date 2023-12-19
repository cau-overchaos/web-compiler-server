cd /home/test/web-compiler-server/server
nohup pipenv run gunicorn --bind 0.0.0.0:5000 run:app > output.log 2>&1 &
