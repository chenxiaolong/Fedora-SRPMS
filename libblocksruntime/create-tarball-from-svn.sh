#!/bin/bash

TEMPDIR=$(mktemp -d)
SOURCEDIR=$(cd $(dirname ${0}) && pwd)
VERSION=$(rpmspec -q --qf '%{version}\n' libblocksruntime.spec | head -n 1)

pushd ${TEMPDIR}

svn checkout svn://svn.code.sf.net/p/blocksruntime/code/tags/REL_${VERSION/./_} libblocksruntime-${VERSION}
tar -Jcv --exclude-vcs -f libblocksruntime-${VERSION}.tar.xz libblocksruntime-${VERSION}
cp libblocksruntime-${VERSION}.tar.xz ${SOURCEDIR}/

popd ${TEMPDIR}

rm -rvf ${TEMPDIR}
