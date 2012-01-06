#!/bin/bash
# Xiao-Long Chen <chenxiaolong@cxl.epac.to>

_svntrunk=https://vgmstream.svn.sourceforge.net/svnroot/vgmstream
_svnname=vgmstream

[ -d ${_svnname} ] && rm -rvf ${_svnname}
svn checkout ${_svntrunk} ${_svnname}
_svnrev=$(svnversion ${_svnname})
mv ${_svnname} ${_svnname}-${_svnrev}svn
tar --exclude-vcs Jcvf ${_svnname}-${_svnrev}svn.tar.xz ${_svnname}-${_svnrev}svn
rm -rvf ${_svnname}-${_svnrev}svn
sed "s/@SVN_REV@/${_svnrev}/" < vgmstream.spec > vgmstream.${_svnrev}.spec
_sources=$(spectool vgmstream.${_svnrev}.spec | awk '{ print $2 }')
echo "SOURCES: ${_sources}"
_sourcedir=$(rpm --eval '%{_sourcedir}')
for i in ${_sources}; do
  cp ${i} ${_sourcedir}
done
rm ${_svnname}-${_svnrev}svn.tar.xz
rpmbuild -ba vgmstream.${_svnrev}.spec
rm vgmstream.${_svnrev}.spec
