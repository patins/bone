bone.mit.edu [![Build Status](https://travis-ci.com/patins/bone.svg?token=qtHz376FXw1xGgVxnyHz&branch=master)](https://travis-ci.com/patins/bone)
==============
B1's website

## development setup
1. install virtualenv and python3
2. clone the project
3. create a virtualenv `virtualenv -p python3 venv`
4. activate the virtualenv `source venv/bin/scripts/activate`
5. install requirements `pip install -r requirements.txt`
6. create your local settings by copying `bone/bone/local_settings.example.py` to `bone/bone/local_settings.py`
7. run the thumbnail migrations `python manage.py makemigrations thumbnail`
8. setup the db `python manage.py migrate`
9. run it!! `python manage.py runserver`
