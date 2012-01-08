%define _svn_rev _SVN_REV_

Name:		wit-svn
Version:	0
Release:	1.%{_svn_rev}svn%{?dist}
Summary:	A set of tools to manipulate Wii and GameCube ISO images and WBFS containers

Group:		Applications/File
License:	GPLv2
URL:		http://hcs64.com/vgmstream.html
Source0:	wiimms-iso-tools-%{_svn_rev}svn.tar.xz

Provides:	wwt wwt-svn
Provides:	wit
Obsoletes:	wit
BuildRequires:	fuse-devel
BuildRequires:	dos2unix
BuildRequires:	wget


%description
Wiimms ISO Tools is a set of command line tools to manipulate Wii and GameCube
ISO images and WBFS containers. The toolset consists of the following tools:

wit (Wiimms ISO Tool):
This is the main ISO manipulation tool : It can list, analyze, verify, convert,
split, join, patch, mix, extract, compose, rename and compare Wii and GameCube
discs. It can create and dump different other Wii file formats.

wwt (Wiimms WBFS Tool):
This is the main WBFS manipulation tool (WBFS manager) : It can create, check,
repair, verify and clone WBFS files and partitions. It can list, add, extract,
remove, rename and recover ISO images as part of a WBFS.

wdf (Wiimms WDF Tool):
wdf is a support tool for WDF, WIA and CISO archives. It convert (pack and
unpack), compare and dump WDF, WIA (dump and cat only) and CISO archives. The
default command depends on the program file name (see command descriptions).
Usual names are wdf, unwdf, wdf-cat, wdf-cmp and wdf-dump (with or without
minus signs). »wdf +CAT« replaces the old tool wdf-cat and »wdf +DUMP« the old
tool wdf-dump.

wfuse (Wiimms FUSE Tool):
Mount a Wii or GameCube image or a WBFS file or partition to a mount point
using FUSE (Filesystem in Userspace). Use 'wfuse --umount mountdir' for
unmounting.


%prep
%setup -q -n wiimms-iso-tools-%{_svn_rev}svn


%build
make %{?_smp_mflags}
make doc


%install
rm -rf $RPM_BUILD_ROOT
# Fix install script
sed -i \
  -e "s|BASE_PATH=\".*\"|BASE_PATH=\"$RPM_BUILD_ROOT\/usr\"|" \
  -e "s|SHARE_PATH=\".*\"|SHARE_PATH=\"$RPM_BUILD_ROOT%{_datadir}/wit\"|" \
  install.sh
PATH="${PATH}:bin" ./install.sh
# Fix paths in /usr/share/load-titles.sh
sed -i \
  -e "s|BASE_PATH=\".*\"|BASE_PATH=\"%{_prefix}\"|" \
  -e "s|SHARE_PATH=\".*\"|SHARE_PATH=\"%{_datadir}/wit\"|" \
  $RPM_BUILD_ROOT%{_datadir}/wit/load-titles.sh
# Convert documentation to UTF-8
pushd doc
for i in wii-homebrew-{beta,update,announce}.forum; do
  iconv -f iso-8859-1 -t utf-8 ${i} > ${i}.utf-8
  cp ${i}.utf-8 ${i}
done
# Fix line endings
dos2unix wit-source.txt
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%{_bindir}/wit
%{_bindir}/wwt
%{_bindir}/wdf
%{_bindir}/wfuse
%{_bindir}/wdf-cat
%{_bindir}/wdf-dump
%{_datadir}/wit/


%changelog
* Fri Jan 6 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0-1
- SVN Package initial release
