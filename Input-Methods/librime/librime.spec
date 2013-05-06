# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		librime
# Version 0.9.9 depends on yaml-cpp 0.5, which isn't packaged in Fedora
Version:	0.9.8
Release:	1%{?dist}
Summary:	RIME Input Method Engine

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://code.google.com/p/rimeime/
Source0:	http://rimeime.googlecode.com/files/librime-%{version}.tar.gz

BuildRequires:	cmake

BuildRequires:	pkgconfig(kyotocabinet)
BuildRequires:	pkgconfig(libglog)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(opencc)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	pkgconfig(zlib)

BuildRequires:	boost-devel

Requires:	%{name}-tools = %{version}-%{release}

# From Debian
%description
RIME is a lightweight, extensible input method engine supporting various input
schematas including glyph-based input methods, romanization-based input methods
as well as those for Chinese dialects. It has the ability to compose phrases and
sentences intelligently and provide very accurate traditional Chinese output.
RIME's cross-platform core library is written in C++, and can work consistently
on different platforms with OS-specific wrappers.


%package devel
Summary:	Development files for librime
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for the rime library.


%package tools
Summary:	Tools for librime
Group:		Development/Tools

Requires:	%{name} = %{version}-%{release}

%description tools
This package contains the tools for the rime library.


%prep
%setup -q -n %{name}

#rm -rvf thirdparty/src/


%build
mkdir build
cd build
%cmake ..
#make %{?_smp_mflags}
make -j1


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog
%{_libdir}/librime.so.*


%files devel
%{_includedir}/rime_api.h
%{_libdir}/librime.so
%{_libdir}/pkgconfig/rime.pc
%{_datadir}/cmake/rime/RimeConfig.cmake


%files tools
%{_bindir}/rime_deployer
%{_bindir}/rime_dict_manager


%changelog
* Sun May 05 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.8-1
- Initial release
- Version 0.9.8
