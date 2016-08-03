#!/bin/sh
ssh -T root@bone.mit.edu << EOF
su web
cd ~/bone
git pull
docker-compose -f docker-compose.prod.yml build app
docker-compose -f docker-compose.prod.yml up --no-deps -d app
exit
EOF
