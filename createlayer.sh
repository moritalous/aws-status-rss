# /bin/sh

cd work

yum install -y python3 python3-pip zip gcc libxml2-devel libxslt-devel

pip3 install -r requirement.txt -t python/
zip -r layer.zip python
