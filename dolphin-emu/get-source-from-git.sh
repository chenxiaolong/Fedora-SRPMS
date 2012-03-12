#!/bin/bash

TEMPDIR=$(mktemp -d)
SOURCEDIR=$(cd $(dirname ${0}) | pwd)

pushd ${TEMPDIR}

git clone https://code.google.com/p/dolphin-emu/ dolphin-emu-3.0
cd dolphin-emu-3.0
git checkout 3.0
cd ..
tar -Jcv --exclude-vcs -f dolphin-emu-3.0.tar.xz dolphin-emu-3.0
cp dolphin-emu-3.0.tar.xz ${SOURCEDIR}/

popd ${TEMPDIR}

rm -rvf ${TEMPDIR}
