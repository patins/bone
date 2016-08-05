#!/bin/sh
ssh -T root@bone.mit.edu << EOF
su web
cd ~/bone
git pull
docker-compose -f docker-compose.prod.yml build app
docker-compose -f docker-compose.prod.yml up --no-deps -d app
docker-compose -f docker-compose.prod.yml exec app python3 manage.py collectstatic --no-input
exit
EOF
