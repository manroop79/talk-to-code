apt-add-repository ppa:deadsnakes/ppa
apt-get update
apt-get install python3.10 python3.10-dev python3.10-distutils --yes
# Create a symbolic link so "python" command points to python 3.10
ln -T /usr/bin/python3.10 /usr/bin/python