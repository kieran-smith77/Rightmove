#! /bin/bash
echo '* libraries/restart-without-asking boolean true' | sudo debconf-set-selections
apt-get update
apt-get upgrade -y
apt-get install -y docker.io s3fs awscli

mkdir /db

echo "s3fs#kieran-smith-rightmove-db /db fuse _netdev,iam_role=rightmove_webserver" >> /etc/fstab
mount -a

chmod 666 /db/*
sudo -u ubuntu -i <<'EOF'
aws s3 sync s3://kieran-smith-rightmove-code ~
sudo docker build . -t rightmove
sudo docker run -p 80:80 -d -v $(pwd)/db:/db rightmove
EOF

