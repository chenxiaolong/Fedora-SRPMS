#!/bin/bash
# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

ARCHIVE="bootstraplinux_ubuntu12_32.tar.xz"
DIR="ubuntu12_32"

if [ -x /usr/lib/rpm/redhat/find-requires ] ; then
  FINDREQ=/usr/lib/rpm/redhat/find-requires
else
  FINDREQ=/usr/lib/rpm/find-requires
fi

unset LANG

TMP_DIR=$(mktemp --tmpdir=$(pwd)/ -d)
pushd ${TMP_DIR}/ &>/dev/null
cp $RPM_BUILD_ROOT/usr/lib/steam/${ARCHIVE} ./
DIR=${ARCHIVE#*_}
DIR=${DIR%%.*}
tar Jxf ${ARCHIVE} ${DIR}/steam
rm ${ARCHIVE}
echo ${TMP_DIR}/${DIR}/steam | ${FINDREQ}
rm ${TMP_DIR}/${DIR}/steam
popd &>/dev/null
rmdir ${TMP_DIR}/${DIR}/
rmdir ${TMP_DIR}/

${FINDREQ} $*
