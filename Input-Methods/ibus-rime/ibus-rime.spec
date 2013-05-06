# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		ibus-rime
Version:	0.9.9
Release:	1%{?dist}
Summary:	RIME Input Method Engine - IBus Frontend

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://code.google.com/p/rimeime/
Source0:	http://rimeime.googlecode.com/files/ibus-rime-%{version}.tar.gz

Patch0:		0001_libexecdir.patch

BuildRequires:	cmake

BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(rime)

# From Debian
%description
RIME is a lightweight, extensible input method engine supporting various input
schematas including glyph-based input methods, romanization-based input methods
as well as those for Chinese dialects. It has the ability to compose phrases and
sentences intelligently and provide very accurate traditional Chinese output.
RIME's cross-platform core library is written in C++, and can work consistently
on different platforms with OS-specific wrappers.


%prep
%setup -q -n ibus-rime

%patch0 -p1 -b .libexecdir


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
install -dm755 $RPM_BUILD_ROOT%{_datadir}/ibus/component/
install -m644 rime.xml $RPM_BUILD_ROOT%{_datadir}/ibus/component/

install -dm755 $RPM_BUILD_ROOT%{_libexecdir}/
install -m755 build/ibus-engine-rime $RPM_BUILD_ROOT%{_libexecdir}/

install -dm755 $RPM_BUILD_ROOT%{_datadir}/ibus-rime/icons/
install -m644 zhung.svg $RPM_BUILD_ROOT%{_datadir}/ibus-rime/icons/


%files
%doc ChangeLog
%{_libexecdir}/ibus-engine-rime
%{_datadir}/ibus-rime/
%dir %{_datadir}/ibus/
%dir %{_datadir}/ibus/component/
%{_datadir}/ibus/component/rime.xml


%changelog
* Sun May 05 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.9-1
- Initial release
- Version 0.9.9
