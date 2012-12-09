# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libdispatch
Version:	0.0.197
Release:	1%{?dist}
Summary:	Portable version of Mac OS X's libdispatch

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://mark.heily.com/project/libdispatch
Source0:	http://mark.heily.com/sites/mark.heily.com/files/libdispatch-0.0.197.tar.gz

Patch0:		http://mark.heily.com/sites/mark.heily.com/files/use_gnu_ld.patch

BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	clang
BuildRequires:	quilt

BuildRequires:	libblocksruntime-devel
BuildRequires:	libpthread_workqueue-devel

BuildRequires:	pkgconfig(libkqueue)

%description
The libdispatch project consts of the user space implementation of the Grand
Central Dispatch API as seen in Mac OS X version 10.7.


%package devel
Summary:	Development files for libdispatch
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}
Requires:	libblocksruntime-devel
Requires:	libpthread_workqueue-devel
Requires:	pkgconfig(libkqueue)

%description devel
The libdispatch project consts of the user space implementation of the Grand
Central Dispatch API as seen in Mac OS X version 10.7.


%prep
%setup -q

%patch0 -p1 -b .gnu-ld

autoreconf -vfi

cp /usr/include/unistd.h dispatch/
sed -i 's/__block/__block2/g' dispatch/unistd.h
sed -i 's/<unistd.h>/"unistd.h"/g' dispatch/dispatch.h


%build
export KQUEUE_CFLAGS="-I/usr/include/kqueue"
%configure
#make %{?_smp_mflags}
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/libdispatch.so.*


%files devel
%dir %{_includedir}/dispatch/
%{_includedir}/dispatch/*.h
%{_libdir}/libdispatch.a
%{_libdir}/libdispatch.so
%{_mandir}/man3/dispatch*.3.gz


%changelog
* Sun Dec 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.197-1
- Initial release
- Version 0.0.97
