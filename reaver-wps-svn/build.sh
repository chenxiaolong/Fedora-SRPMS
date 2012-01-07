#!/bin/bash
# Xiao-Long Chen <chenxiaolong@cxl.epac.to>

_svntrunk=http://reaver-wps.googlecode.com/svn/trunk/
_svnname=reaver-wps
_specfile=reaver-wps-svn.spec

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
for i in ${_sources}; do
  cp ${i} ${_sourcedir}
done
rm ${_svnname}-${_svnrev}svn.tar.xz
rpmbuild -ba ${_specfile%.spec}.${_svnrev}.spec
rm ${_specfile%.spec}.${_svnrev}.spec
