#!/usr/bin/env bash

SPEC_VER="$(rpmspec -q --qf '%{version}\n' bbswitch-kmod.spec | head -1)"

echo "Getting latest upstream version..."
UPSTREAM_VER=$(wget -q 'https://github.com/Bumblebee-Project/bbswitch/downloads' -O - | sed -n 's/.*bbswitch-\(.*\)\.tar\.gz.*/\1/p' | head -n 1)

echo ""

echo -e "spec file version: ${SPEC_VER}"
echo -e "Upstream version:  ${UPSTREAM_VER}"
