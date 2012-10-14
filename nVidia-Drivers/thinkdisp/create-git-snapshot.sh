#!/usr/bin/bash

SPEC_VER=$(rpmspec -q --qf '%{version}\n' thinkdisp.spec | head -1)
GIT_COMMIT=$(cat thinkdisp.spec | sed -n 's/%define[ ]*_git_commit[ ]*\(.*\)/\1/p')

git clone https://github.com/sagark/thinkdisp.git thinkdisp-${SPEC_VER}

pushd thinkdisp-${SPEC_VER}/
git checkout ${GIT_COMMIT}
popd

tar -Jc --exclude-vcs -f thinkdisp-${SPEC_VER}.tar.xz thinkdisp-${SPEC_VER}/
rm -rf thinkdisp-${DATE}/
echo "Created thinkdisp-${SPEC_VER}.tar.xz"
