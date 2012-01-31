%define debian_rel 5

Name:		bdfresize
Version:	1.5
Release:	1.%{debian_rel}%{?dist}
Summary:	A tool for resizing BDF format font

Group:		User Interface/X
License:	GPLv2
URL:		http://packages.debian.org/sid/bdfresize
Source0:	http://ftp.de.debian.org/debian/pool/main/b/bdfresize/bdfresize_%{version}.orig.tar.gz
Source1:	http://ftp.de.debian.org/debian/pool/main/b/bdfresize/bdfresize_%{version}-%{debian_rel}.diff.gz


%description
Bdfresize is a command to magnify or reduce fonts which are described with
the standard BDF format.


%prep
%setup -q


%build
# Apply Debian patches
zcat "%{SOURCE1}" | patch -Np1

%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/bdfresize
%{_mandir}/man1/bdfresize.1.gz


%changelog
* Tue Jan 31 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.5-1.5
- 1.5 release with Debian release 5
- Initial release
