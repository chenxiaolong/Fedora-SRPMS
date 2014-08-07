# Written by Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libdvdcss
Version:	1.3.0
Release:	1%{?dist}
Summary:	A portable abstraction library for DVD decryption

Group:		System Environment/Libraries
License:	GPLv2+
URL:		http://www.videolan.org/developers/libdvdcss.html
Source0:	http://download.videolan.org/pub/videolan/libdvdcss/1.3.0/libdvdcss-%{version}.tar.bz2

BuildRequires:	gcc-c++

%description
libdvdcss is a simple library designed for accessing DVDs like a block device
without having to bother about the decryption.


%package devel
Summary:	Development files for libdvdcss
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development files for the libdvdcss library.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

find %{buildroot} -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libdvdcss.so.*


%files devel
%{_includedir}/dvdcss/
%{_libdir}/pkgconfig/
%{_libdir}/libdvdcss.so


%changelog
* Thu Aug 07 2014 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3.0-1
- Initial release
