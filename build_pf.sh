#!/bin/sh

USERID=$1

adduser -u ${USERID} builder -D -G wheel && echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
addgroup builder abuild
chown builder -R ..
chown builder -R /tmp
mkdir -p /var/cache/distfiles
chmod a+w /var/cache/distfiles
chgrp abuild /var/cache/distfiles
chmod g+w /var/cache/distfiles
su builder -c "abuild-keygen -a -i -n"
apk add bash git

cd ./linux-edge
su builder -c "abuild checksum"
su builder -c "abuild deps" 

su builder -c "abuild"        
cp $(find /home/builder -name linux-pf*.apk) ./
