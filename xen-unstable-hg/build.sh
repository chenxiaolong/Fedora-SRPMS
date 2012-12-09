#!/bin/bash

# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

VERSION=$(grep Version xen-unstable.spec.in | awk '{print $2}')

if [ ! -d xen-unstable ]; then
  hg --config 'extensions.progress=' clone \
    http://xenbits.xen.org/hg/xen-unstable.hg xen-unstable
  pushd xen-unstable
else
  pushd xen-unstable
  hg --config 'extensions.progress=' pull
fi

mkdir tools/BUILD/
pushd tools/BUILD/
../configure
popd

ln -s Tools.mk.in config/Tools.mk

cp scripts/git-checkout.sh{,.orig}
sed -i 's/clone/clone --depth 0/' scripts/git-checkout.sh

make -C tools qemu-xen-traditional-dir-find
make -C tools qemu-xen-dir-find
make -C tools/firmware ovmf
make -C tools/firmware seabios-dir
make -C tools/firmware ovmf-find

mv scripts/git-checkout.sh{.orig,}

rm config/Tools.mk
rm -rvf tools/BUILD/
rm -rvf tools/config/

HGCOMMIT=$(hg log --limit 1 --template '{rev}:{node|short}')
HGREV=${HGCOMMIT%:*}
HGNODE=${HGCOMMIT#*:}
DATE=($(hg log --limit 1 --template '{date|date}'))
MONTH=1
for i in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec; do
  if [ "x${DATE[1]}" == "x${i}" ]; then
    break
  fi
  let MONTH++
done

if [ ${#MONTH} -lt 2 ]; then
  MONTH="0${MONTH}"
fi

if [ ${#DATE[2]} -lt 2 ]; then
  DATE[2]="0${DATE[2]}"
fi

# DATE[0] = Day of the week
# DATE[1] = Month (abbreviated English month names)
# DATE[2] = Day
# DATE[4] = Year
#  -e "s/@FULLDATE@/$(LANG=C date +%a\ %b\ %d\ %Y)/g"

FULLDATE="${DATE[0]} ${DATE[1]} ${DATE[2]} ${DATE[4]}"

popd

if [ -d xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}} ]; then
  rm -rvf xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}
fi
if [ -f xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.tar.xz ]; then
  rm xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.tar.xz
fi
#hg --config 'extensions.progress=' clone \
#  xen-unstable xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}
# Need to keep the git clones
cp -r xen-unstable xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}
tar --exclude-vcs -Jcvf xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.tar.xz \
                        xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}
rm -rf xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}

sed \
  -e "s/@FULLDATE@/${FULLDATE}/g" \
  -e "s/@HGREV@/${HGREV}/g" \
  -e "s/@HGNODE@/${HGNODE}/g" \
  < xen-unstable.spec.in \
  > xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.spec

spectool -g xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.spec

rpmbuild -bs --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" \
  xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.spec
echo "Please build that source RPM and install the new RPMs"

# Not deleting the generated spec and tarball for this package since they take
# way too long to regenerate
#rm xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.spec
#rm xen-unstable-${VERSION}-r${HGREV}.hg${HGNODE}.tar.xz
