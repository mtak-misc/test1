#!/bin/sh
pacman -Syu --noconfirm base-devel sudo git jq curl unzip schedtool
#curl -sLJO -H 'Accept: application/octet-stream' \
#"https://$GITHUB_TOKEN@api.github.com/repos/mtak-misc/pkgbuild-llvm-git/releases/assets/$( \
#curl -sL https://$GITHUB_TOKEN@api.github.com/repos/mtak-misc/pkgbuild-llvm-git/releases/tags/test \
#| jq '.assets[] | select(.name | contains("llvm")) | .id')" -o llvm-git.zip
#unzip llvm-git.zip
#pacman --noconfirm -U llvm-git*.pkg.tar.zst llvm-libs-git*.pkg.tar.zst
useradd builder  -u $USERID -m -G wheel && echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
cd /workspace/linux-lqx ; su builder -c "yes '' | BUILD_FLAGS=(CC=clang CXX=clang++ HOSTCC=clang HOSTCXX=clang++ LD=ld.lld LLVM=1 LLVM_IAS=1) makepkg --noconfirm -sc"
