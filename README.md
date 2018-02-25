# AlgoJ 

Prototype online judge that uses django, django-q, redis and docker. Runs mainly with python3, though support for other languages can be added.
It's designed to be very lightweight and to be mainly used inside a class setting.

## Demo

![Demo video](https://thumbs.gfycat.com/DisguisedNauticalIaerismetalmark-size_restricted.gif)


## Installation

To install it, first clone the repository:

`git clone https://github.com/eilx2/algoj`


Go to the algoj directory. Then create a new virtual environment inside:

`virtualenv -p python3 algoj-env`


Enable it:

`source algoj-env/bin/activate`


Now install the requirements:

`pip install -r requirements.txt`

You'll also need Redis in order for the evaluation system to work. See here on how to install it:

https://redis.io/topics/quickstart

### Docker
You'll need docker to run submissions in isolation. To install it see here:
https://docs.docker.com/install/


After this, you'll need to build the image. Go inside the `docker` directory, then run:

`docker built -t judge-docker .`

## Running

First run redis by using:

`redis-server --port 6379`

If you want to use another port, you must also change the `Q_CLUSTER['redis']['port']` value inside the `settings.py` file of the project.


Now run a django-q cluster in the background using:


`python3 manage.py qcluster &`


Then run the server itself:

`python3 manage.py runserver`
