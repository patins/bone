bone.mit.edu [![Build Status](https://travis-ci.org/patins/bone.svg?branch=master)](https://travis-ci.org/patins/bone)
==============
B1's website

## development
1. Install Docker and docker-compose. Use [Docker Toolbox](https://www.docker.com/products/docker-toolbox) to do this easily.
2. Get your shell docker-ready:
  ```
  docker-machine start
  eval $(docker-machine env)
  ```
3. Create app.env. Specify
  ```
  SECRET_KEY=generate a random string
  DEBUG=True
  ```
4. Start developing!! The dev server will be available at your docker-machine's IP address, port 8000. To docker your docker-machine's IP run `docker-machine ip`.
5. If it's your first time starting this container, you'll want to run DB migrations `docker-compose exec app python3 manage.py migrate` and create a superuser with your kerberos as the username `docker-compose exec app python3 manage.py createsuperuser`.

## aditional notes
to run a django command: `docker-compose exec app python3 manage.py yourcommand`

to run `docker-compose up` in the background use `docker-compose up -d`
## workflow
1. branch from master (`git checkout master; git checkout -b my-feature`)
the branch name should be related to the feature you're working on
2. work on your feature and add appropriate tests
3. commit and push (`git push -u origin my-feature`)
4. create a pull request to master
5. let travis tests pass
6. wait for thumbs up
7. deployed maybe some day
