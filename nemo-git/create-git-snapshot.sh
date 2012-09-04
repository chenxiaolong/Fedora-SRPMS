#!/usr/bin/bash

DATE=$(date +%Y%m%d)

git clone https://github.com/linuxmint/nemo.git nemo-${DATE}

pushd nemo-${DATE}/
SHA=$(git rev-list --max-count=1 --abbrev-commit HEAD)
popd

tar -Jc --exclude-vcs -f nemo-${DATE}-git${SHA}.tar.xz nemo-${DATE}/
rm -rf nemo-${DATE}/
echo "Created nemo-${DATE}-git${SHA}.tar.xz"
