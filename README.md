Project is designed to take user`s name, date, location and output weather forecast based on input data.

Requirements 
Python 3.8.0

How to run

1. create virtual enviroment (python -m venv .venv)
2. activate virtual enviroment(.venv/bin/activate)
3. install requirements(-r requirements.txt)
4. sign up on https://www.visualcrossing.com/weather-api to get your key
5. enter your key to the 'key' variable in weather_reporto.py
6. start server(uwsgi --http 0.0.0.0:8000 --wsgi-file weather_reporto.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191)
7. send request using JSON format in Postman

