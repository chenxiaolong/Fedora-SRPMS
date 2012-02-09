%define _svn_rev _SVN_REV_

Name:		reaver-wps-svn
Version:	0
Release:	1.%{_svn_rev}svn%{?dist}
Summary:	A tool to brute force attack against Wifi Protected Setup (WPS)

Group:		Applications/File
License:	GPLv2
URL:		http://hcs64.com/vgmstream.html
Source0:	reaver-wps-%{_svn_rev}svn.tar.xz

Provides:	reaver-wps
Obsoletes:	reaver-wps
BuildRequires:	libpcap-devel
BuildRequires:	sqlite-devel


%description
Reaver implements a brute force attack against Wifi Protected Setup (WPS)
registrar PINs in order to recover WPA/WPA2 passphrases, as described in
http://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf.

Reaver has been designed to be a robust and practical attack against WPS, and
has been tested against a wide variety of access points and WPS implementations.

On average Reaver will recover the target AP's plain text WPA/WPA2 passphrase
in 4-10 hours, depending on the AP. In practice, it will generally take half
this time to guess the correct WPS pin and recover the passphrase.


%prep
%setup -q -n reaver-wps-%{_svn_rev}svn


%build
cd src
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
pushd src
# Binaries
install -dm755 "$RPM_BUILD_ROOT%{_bindir}"
install -m755 reaver "$RPM_BUILD_ROOT%{_bindir}"
install -m755 wash "$RPM_BUILD_ROOT%{_bindir}"
# Configuration
install -dm755 "$RPM_BUILD_ROOT%{_sysconfdir}/reaver/"
install -m644 reaver.db "$RPM_BUILD_ROOT%{_sysconfdir}/reaver/"
popd

pushd docs
# Man pages
install -dm755 "$RPM_BUILD_ROOT%{_mandir}/man1/"
install -m644 reaver.1.gz "$RPM_BUILD_ROOT%{_mandir}/man1/"
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/LICENSE
%doc docs/README
%{_bindir}/reaver
%{_bindir}/wash
%config(noreplace) %{_sysconfdir}/reaver/reaver.db
%{_mandir}/man1/reaver.1.gz


%changelog
* Mon Feb 6 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0-1
- Rename walsh to wash to reflect upstream changes
- Add sqlite-devel to the build dependencies

* Sat Jan 7 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0-1
- SVN Package initial release
