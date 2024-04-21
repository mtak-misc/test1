#!/bin/sh

USERID=$1

apk upgrade
apk add alpine-sdk sudo

adduser builder -u ${USERID} -D -G wheel && echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
addgroup builder abuild
chown builder -R ..
chown builder -R /tmp
mkdir -p /var/cache/distfiles
chmod a+w /var/cache/distfiles
chgrp abuild /var/cache/distfiles
chmod g+w /var/cache/distfiles
su builder -c "abuild-keygen -a -i -n"
apk add bash git

cd linux-lts
cp ../config.lts /home/builder

# sed -i -e '/unset LDFLAGS/a \ \tcp /home/builder/config.lts "$srcdir"/$_flavor.$_arch.config' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_TRACKPOINT' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_TOUCHKIT' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_SYNAPTICS_SMBUS' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_SYNAPTICS' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_SMBUS' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_SENTELIC' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_LOGIPS2PP' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_LIFEBOOK' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_FOCALTECH' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_ELANTECH_SMBUS' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_CYPRESS' APKBUILD
sed -i -e '/unset LDFLAGS/a \ \tscripts/config --file "$srcdir"/lts.x86_64.config -e CONFIG_MOUSE_PS2_ALPS' APKBUILD
# sed -i -e '/CONFIG_MOUSE_PS2=m/a CONFIG_MOUSE_PS2_SENTELIC=y' lts.x86_64.config
# sed -i -e '/d792b0b606374ff6a09302fdd0c8d8fda3944c278018cd1162510613d1f306714654890875a4eda3da2fc2afe180e7e20cf825bcb942157efeb40a0fe0cfd4c2/d' APKBUILD

su builder -c "abuild checksum"
su builder -c "abuild deps"                

su builder -c "abuild"        
cp $(find /home/builder -name linux-lts*.apk) .
