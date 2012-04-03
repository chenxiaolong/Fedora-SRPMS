#!/bin/bash

TEMPDIR=$(mktemp -d)
SOURCEDIR=$(cd $(dirname ${0}) && pwd)
VERSION=$(rpmspec -q --qf '%{version}' tlp.spec | head -n 1)

pushd ${TEMPDIR}

git clone https://github.com/linrunner/TLP.git tlp-${VERSION}
cd tlp-${VERSION}
git checkout ${VERSION}
cd ..
tar -Jcv --exclude-vcs -f tlp-${VERSION}.tar.xz tlp-${VERSION}/
cp tlp-${VERSION}.tar.xz ${SOURCEDIR}/

popd ${TEMPDIR}

rm -rvf ${TEMPDIR}
