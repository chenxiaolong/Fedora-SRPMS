#!/bin/bash

# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Patches from https://github.com/liskin/patches/tree/master/hacks

FEDORA_VER=$(sed -n 's/%fedora[ \t]*\(.*\)/\1/p' /etc/rpm/macros.dist)

if [ ! -d xorg-x11-drv-intel ]; then
  fedpkg co -a -B xorg-x11-drv-intel
  cd xorg-x11-drv-intel/f${FEDORA_VER}
else
  cd xorg-x11-drv-intel/f${FEDORA_VER}
  fedpkg pull
fi

if [ -f build.spec ]; then
  rm build.spec
fi

fedpkg sources

SPEC_VER=$(rpmspec -q --qf '%{version}\n' xorg-x11-drv-intel.spec | head -1)
SPEC_REL=$(rpmspec -q --qf '%{release}\n' xorg-x11-drv-intel.spec | head -1)
SPEC_REL_NO_DIST=${SPEC_REL/.fc${FEDORA_VER}/}

SPEC_REL_MAJOR=${SPEC_REL_NO_DIST%%.*}
SPEC_REL_MINOR=${SPEC_REL_NO_DIST#*.}
if [ "x${SPEC_REL_MAJOR}" == "x${SPEC_REL_MINOR}" ]; then
  let SPEC_REL_MAJOR++
  SPEC_REL=${SPEC_REL_MAJOR}
else
  let SPEC_REL_MAJOR++
  SPEC_REL=${SPEC_REL_MAJOR}.${SPEC_REL_MINOR}
fi

sed \
  -e "s/^\(Release:[ \t]*\).*$/\1${SPEC_REL}%{dist}/" \
  -e "/%changelog/ a \
* $(LANG=C date +%a\ %b\ %d\ %Y) Fedora-SRPMS Autobuilder <Fedora-SRPMS@github> - ${SPEC_VER}-${SPEC_REL} \\
- Patched to support virtual display \\
" \
  -e '1 i \
Patch100: xserver-xorg-video-intel-2.20.10_virtual_crtc.patch \
Provides: xorg-x11-drv-intel-virtual-crtc' \
  -e '/^%setup/ a \
%patch100 -p1 -b .virtual-crtc' \
  < xorg-x11-drv-intel.spec \
  > build.spec

cp ../../xserver-xorg-video-intel-2.20.10_virtual_crtc.patch .
#spectool -g build.spec

rpmbuild -bs --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" build.spec

echo "Please build that source RPM and install the new RPMs"

rm build.spec
