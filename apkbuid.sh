#!/bin/sh
cd $1
buildozer init
echo "android.accept_android_licenses = True" >> buildozer.spec
buildozer -v android debug
