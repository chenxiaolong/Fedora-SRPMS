#!/bin/sh
#Get current SVN revision
./get_svn_revision.sh

#SVN revision
SVN_REV=`cat svn_revision | sed -e 's/^.*r//'`
#UMPlayer version
UMPLAYER_VER=`cat src/version.cpp | grep "#define VERSION " | sed -e 's/#define VERSION "//g' -e 's/ /_/g' -e 's/"$//g'`

svn export . /tmp/umplayer-${UMPLAYER_VER}_svn_r${SVN_REV}
CURRDIR=`pwd`
pushd /tmp
#Create tarball
tar jcvf "umplayer-${UMPLAYER_VER}_svn_r${SVN_REV}.tar.bz2" "umplayer-${UMPLAYER_VER}_svn_r${SVN_REV}/"
rm -r "/tmp/umplayer-${UMPLAYER_VER}_svn_r${SVN_REV}"
sed -e "s/REPLACESVN/${SVN_REV}/" -e "s/REPLACEVER/${UMPLAYER_VER}/" < "${CURRDIR}/umplayer.spec" > /tmp/umplayer.spec
#This is now the default in the major RPM distributions
RPMDEVDIR=${HOME}/rpmbuild
cp "/tmp/umplayer-${UMPLAYER_VER}_svn_r${SVN_REV}.tar.bz2" "${RPMDEVDIR}/SOURCES"
rpmbuild -ba --rmsource newpackage.spec
popd
