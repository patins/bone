bone.mit.edu [![Build Status](https://travis-ci.com/patins/bone.svg?token=qtHz376FXw1xGgVxnyHz&branch=master)](https://travis-ci.com/patins/bone)
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

## workflow
1. branch from master (`git checkout master; git checkout -b my-feature`)
the branch name should be related to the feature you're working on
2. work on your feature and add appropriate tests
3. commit and push (`git push -u origin my-feature`)
4. create a pull request to master
5. let travis tests pass
6. wait for thumbs up
7. deployed maybe some day
