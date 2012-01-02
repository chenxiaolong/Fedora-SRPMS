Name:          bsdtar
Version:       2.8.5
Release:       1%{?dist}
Summary:       bsdtar and bsdcpio command line utilities from libarchive
Group:         Applications/Archiving
License:       BSD
URL:           http://code.google.com/p/libarchive/
Source0:       http://libarchive.googlecode.com/files/libarchive-%{version}.tar.gz

BuildRequires: bison
BuildRequires: sharutils
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: libunistring-devel


%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%prep
%setup -q -n libarchive-%{version}


%build
autoreconf -vfi
%configure --disable-static --enable-bsdtar --enable-bsdcpio --disable-rpath
make %{?_smp_mflags}


%check
# The checking currently fails because 'test_option_b' creates tar files that
# are 3072 bytes big, but expects 2048. libarchive copies the extended attributes
# to the tar archive, so this is reproducible on an SELinux enabled partition.
# Bug report: http://code.google.com/p/libarchive/issues/detail?id=131
#make check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
iconv -f latin1 -t utf-8 < NEWS > NEWS.utf8
cp NEWS.utf8 NEWS

# Remove files that belong to libarchive

# Source headers
rm -rf $RPM_BUILD_ROOT/usr/include/
# Libraries and pkgconfig files
rm -rf $RPM_BUILD_ROOT%{_libdir}/
# Unneeded man pages
find $RPM_BUILD_ROOT%{_datadir} -type f ! -name 'bsdtar*' ! -name 'bsdcpio*' -exec rm {} \;


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/bsdtar
%{_bindir}/bsdcpio
%doc COPYING NEWS README
%{_mandir}/man1/bsdtar.1.gz
%{_mandir}/man1/bsdcpio.1.gz


%changelog
* Sat Jan 01 2012 chenxiaolong@cxl.epac.to - 2.8.5-1
- Downgrade to 2.8.5 for Fedora 16

* Sat Jan 01 2012 chenxiaolong@cxl.epac.to - 3.0.2-1
- Initial release
