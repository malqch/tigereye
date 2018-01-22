cd /home/rock/Desktop/tigereye1
/home/rock/Desktop/tigereye1/env/bin/gunicorn -w4 -D wsgi
ps aux |grep gunicorn|grep tigereye|grep -v grep
