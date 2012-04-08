Name:		binwalk
Version:	0.4.3
Release:	1%{?dist}
Summary:	A tool for searching a given binary image for embedded files and executable code

Group:		Development/Tools
License:	MIT
URL:		https://code.google.com/p/binwalk/
Source0:	https://binwalk.googlecode.com/files/binwalk-%{version}.tar.gz

BuildRequires:	file-devel
BuildRequires:	libcurl-devel


%description
Binwalk is a tool for searching a given binary image for embedded files and
executable code. Specifically, it is designed for identifying files and code
embedded inside of firmware images. Binwalk uses the libmagic library, so it
is compatible with magic signatures created for the Unix file utility.

Binwalk also includes a custom magic signature file which contains improved
signatures for files that are commonly found in firmware images such as
compressed/archived files, firmware headers, Linux kernels, bootloaders,
filesystems, etc.


%prep
%setup -q


%build
cd src
%configure --enable-libmagic
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/README
%{_bindir}/binwalk
# No (noreplace) because the program may upgrade the magic files causing them
# to not be updated the next time the package upgrades.
%config %{_sysconfdir}/binwalk/magic.binarch
%config %{_sysconfdir}/binwalk/magic.bincast
%config %{_sysconfdir}/binwalk/magic.binwalk


%changelog
* Sun Apr 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.3-1
- Initial release
