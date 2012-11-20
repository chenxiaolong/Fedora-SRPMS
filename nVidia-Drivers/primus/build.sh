#!/bin/bash

# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

if [ ! -d primus ]; then
  git clone https://github.com/amonakov/primus.git
  pushd primus
else
  pushd primus
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

if [ -d primus-${GITDATE}-git${GITCOMMIT} ]; then
  rm -rvf primus-${GITDATE}-git${GITCOMMIT}
fi
if [ -f primus-${GITDATE}-git${GITCOMMIT}.tar.xz ]; then
  rm primus-${GITDATE}-git${GITCOMMIT}.tar.xz
fi
git clone primus primus-${GITDATE}-git${GITCOMMIT}
tar --exclude-vcs -Jcvf primus-${GITDATE}-git${GITCOMMIT}.tar.xz \
                        primus-${GITDATE}-git${GITCOMMIT}
rm -rvf primus-${GITDATE}-git${GITCOMMIT}

sed \
  -e "s/@FULLDATE@/${FULLDATE}/g" \
  -e "s/@GITDATE@/${GITDATE}/g" \
  -e "s/@GITCOMMIT@/${GITCOMMIT}/g" \
  < primus.spec.in \
  > primus-${GITDATE}-git${GITCOMMIT}.spec

rpmbuild -bs --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" \
  primus-${GITDATE}-git${GITCOMMIT}.spec
echo "Please build that source RPM and install the new RPMs"

rm primus-${GITDATE}-git${GITCOMMIT}.spec
rm primus-${GITDATE}-git${GITCOMMIT}.tar.xz
