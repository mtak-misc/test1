#!/bin/sh
cd $1
BUILDOZER=$(find / | grep bin | grep buildozer)
echo $BUILDOZER
buildozer init
echo "android.accept_android_licenses = True" >> buildozer.spec
buildozer -v android debug
