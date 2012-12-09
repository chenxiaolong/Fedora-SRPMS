# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libpthread_workqueue
Version:	0.8.2
Release:	1%{?dist}
Summary:	Portable implementation of the Mac OS X pthread_workqueue API

Group:		System Environment/Libraries
License:	BSD and ASL 2.0
URL:		http://sourceforge.net/p/libpwq/wiki/Home/
Source0:	http://downloads.sourceforge.net/project/libpwq/libpthread_workqueue-%{version}.tar.gz

%description
libpthread_workqueue is a portable implementation of the pthread_workqueue API
first introduced in Mac OS X. It is primarily intended for use with libdispatch
but can be used as a general purpose thread pool library for C programs.


%package devel
Summary:	Development files for libpthread_workqueue
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description devel
libpthread_workqueue is a portable implementation of the pthread_workqueue API
first introduced in Mac OS X. It is primarily intended for use with libdispatch
but can be used as a general purpose thread pool library for C programs.


%prep
%setup -q

# Shut up rpmlint
find . -type f ! -name configure -exec chmod 644 {} \+


%build
export CFLAGS="%{optflags} -I$(pwd)/include -I$(pwd)/src"
%configure
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/libpthread_workqueue.so.0.0


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/libpthread_workqueue.so.*


%files devel
%{_includedir}/pthread_workqueue.h
%{_libdir}/libpthread_workqueue.so
%{_mandir}/man3/pthread_workqueue.3.gz


%changelog
* Sun Dec 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.8.2-1
- Initial release
- Version 0.8.2
