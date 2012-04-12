#!/bin/sh

# Taken from xorg-x11-drv-nvidia's SPEC file

VERSION=$(rpmspec -q --qf '%{version}\n' nvidia-kmod.spec | head -n 1)

if [ ! -f NVIDIA-Linux-x86-${VERSION}.run ]; then
  wget -c "ftp://download.nvidia.com/XFree86/Linux-x86/${VERSION}/NVIDIA-Linux-x86-${VERSION}.run"
fi
if [ ! -f NVIDIA-Linux-x86_64-${VERSION}.run ]; then
  wget -c "ftp://download.nvidia.com/XFree86/Linux-x86_64/${VERSION}/NVIDIA-Linux-x86_64-${VERSION}.run"
fi

sh NVIDIA-Linux-x86-${VERSION}.run --extract-only --target nvidiapkg-x86
sh NVIDIA-Linux-x86_64-${VERSION}.run --extract-only --target nvidiapkg-x64

tar -Jcvf nvidia-kmod-data-${VERSION}.tar.xz nvidiapkg-*/LICENSE nvidiapkg-*/kernel
