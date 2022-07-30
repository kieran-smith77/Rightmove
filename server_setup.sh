#! /bin/bash
apt-get update
apt-get upgrade -y
apt-get install -y docker.io awscli

sudo -u ubuntu -i <<'EOF'
aws s3 sync s3://kieran-smith-rightmove-code ~
sudo docker build . -t rightmove
sudo docker run -p 80:80 -d rightmove
EOF
