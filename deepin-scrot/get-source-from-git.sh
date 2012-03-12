#!/bin/bash

TEMPDIR=$(mktemp -d)
SOURCEDIR=$(cd $(dirname ${0}) | pwd)

pushd ${TEMPDIR}

git clone https://github.com/manateelazycat/deepin-scrot.git deepin-scrot-0.1
cd deepin-scrot-0.1
git checkout 0.1
cd ..
tar -Jcv --exclude-vcs -f deepin-scrot-0.1.tar.xz deepin-scrot-0.1
cp deepin-scrot-0.1.tar.xz ${SOURCEDIR}/

popd ${TEMPDIR}

rm -rvf ${TEMPDIR}
