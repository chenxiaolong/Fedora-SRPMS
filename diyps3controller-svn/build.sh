#!/bin/bash
# Xiao-Long Chen <chenxiaolong@cxl.epac.to>

_svntrunk=http://diyps3controller.googlecode.com/svn/trunk/
_svnname=diyps3controller
_specfile=diyps3controller-svn.spec

[ -d ${_svnname} ] && rm -rvf ${_svnname}
svn checkout ${_svntrunk} ${_svnname}
_svnrev=$(svnversion ${_svnname})
mv ${_svnname} ${_svnname}-${_svnrev}svn
tar -Jcv --exclude-vcs -f ${_svnname}-${_svnrev}svn.tar.xz ${_svnname}-${_svnrev}svn
rm -rvf ${_svnname}-${_svnrev}svn
sed "s/_SVN_REV_/${_svnrev}/" < ${_specfile} > ${_specfile%.spec}.${_svnrev}.spec
_sources=$(spectool ${_specfile%.spec}.${_svnrev}.spec | awk '{ print $2 }')
echo "SOURCES: ${_sources}"
_sourcedir=$(rpm --eval '%{_sourcedir}')
spectool -g -R ${_specfile%.spec}.${_svnrev}.spec
for i in ${_sources}; do
  if [ ! -f "${_sourcedir}/${i##*/}" ]; then
    cp ${i##*/} ${_sourcedir}
  fi
done
rm ${_svnname}-${_svnrev}svn.tar.xz
rpmbuild -ba ${_specfile%.spec}.${_svnrev}.spec
rm ${_specfile%.spec}.${_svnrev}.spec
