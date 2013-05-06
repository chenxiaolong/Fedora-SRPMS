# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		brise
Version:	0.18
Release:	1%{?dist}
Summary:	RIME Input Method Engine - Schema Data

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://code.google.com/p/rimeime/
Source0:	http://rimeime.googlecode.com/files/brise-%{version}.tar.gz

BuildRequires:	librime-tools

Requires:	librime >= 0.9.8

# From Debian
%description
RIME is a lightweight, extensible input method engine supporting various input
schematas including glyph-based input methods, romanization-based input methods
as well as those for Chinese dialects. It has the ability to compose phrases and
sentences intelligently and provide very accurate traditional Chinese output.
RIME's cross-platform core library is written in C++, and can work consistently
on different platforms with OS-specific wrappers.


%prep
%setup -q -n %{name}


%build
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog
%{_datadir}/rime-data/


%changelog
* Sun May 05 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.18-1
- Initial release
- Version 0.18
