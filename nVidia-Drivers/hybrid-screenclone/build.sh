#!/bin/bash

# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

if [ ! -d hybrid-screenclone ]; then
  git clone https://github.com/liskin/hybrid-screenclone.git
  pushd hybrid-screenclone
else
  pushd hybrid-screenclone
  git pull
fi

GITCOMMIT=$(git rev-list --max-count=1 --abbrev-commit HEAD)
DATE=($(LANG=C git log --max-count=1 | grep Date))
MONTH=1
for i in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec; do
  if [ "x${DATE[2]}" == "x${i}" ]; then
    break
  fi
  let MONTH++
done

if [ ${#MONTH} -lt 2 ]; then
  MONTH="0${MONTH}"
fi

if [ ${#DATE[3]} -lt 2 ]; then
  DATE[3]="0${DATE[3]}"
fi

# DATE[1] = Day of the week
# DATE[2] = Month (abbreviated English month names)
# DATE[3] = Day
# DATE[5] = Year
#  -e "s/@FULLDATE@/$(LANG=C date +%a\ %b\ %d\ %Y)/g" \
#  -e "s/@GITDATE@/$(LANG=C date +%Y%m%d)/g" \

GITDATE="${DATE[5]}${MONTH}${DATE[3]}"
FULLDATE="${DATE[1]} ${DATE[2]} ${DATE[3]} ${DATE[5]}"

popd

if [ -d hybrid-screenclone-${GITDATE}-git${GITCOMMIT} ]; then
  rm -rvf hybrid-screenclone-${GITDATE}-git${GITCOMMIT}
fi
if [ -f hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.tar.xz ]; then
  rm hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.tar.xz
fi
git clone hybrid-screenclone hybrid-screenclone-${GITDATE}-git${GITCOMMIT}
tar --exclude-vcs -Jcvf hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.tar.xz \
                        hybrid-screenclone-${GITDATE}-git${GITCOMMIT}
rm -rvf hybrid-screenclone-${GITDATE}-git${GITCOMMIT}

sed \
  -e "s/@FULLDATE@/${FULLDATE}/g" \
  -e "s/@GITDATE@/${GITDATE}/g" \
  -e "s/@GITCOMMIT@/${GITCOMMIT}/g" \
  < hybrid-screenclone.spec.in \
  > hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.spec

rpmbuild -bs --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" \
  hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.spec
echo "Please build that source RPM and install the new RPMs"

rm hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.spec
rm hybrid-screenclone-${GITDATE}-git${GITCOMMIT}.tar.xz
