#! /bin/bash
echo '* libraries/restart-without-asking boolean true' | sudo debconf-set-selections
apt-get update
apt-get upgrade -y
apt-get install -y docker.io s3fs awscli
echo "user_allow_other" >> /etc/fuse.conf
mkdir /db
echo "s3fs#kieran-smith-rightmove-db /db fuse _netdev,iam_role=rightmove_webserver,allow_other" >> /etc/fstab
mount -a

chmod 666 /db/*
sudo -u ubuntu -i <<'EOF'
aws s3 sync s3://kieran-smith-rightmove-code ~
sudo docker build . -t rightmove
sudo docker run -p 80:80 -d -v /db:/db rightmove
EOF

