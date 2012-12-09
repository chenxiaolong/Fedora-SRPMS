# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libkqueue
Version:	1.0.6
Release:	1%{?dist}
Summary:	Portable userspace implementation of the kqueue event notification mechanism

Group:		System Environment/Libraries
License:	BSD
URL:		http://mark.heily.com/project/libkqueue
Source0:	http://mark.heily.com/sites/mark.heily.com/files/libkqueue-%{version}.tar.gz

%description
libkqueue is a portable userspace implementation of the kqueue(2) kernel event
notification mechanism. It acts as a translator between the kevent structure and
the native kernel facilities of the host machine.


%package devel
Summary:	Development files for libkqueue
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description devel
libkqueue is a portable userspace implementation of the kqueue(2) kernel event
notification mechanism. It acts as a translator between the kevent structure and
the native kernel facilities of the host machine.


%prep
%setup -q

sed -i 's/-Werror//g' config.inc


%build
#export CFLAGS="%{optflags} -Wno-error"
# Not an autotools configure script, but the configure macro works anyway
export debug=yes
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/libkqueue.so.0.0

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/libkqueue.so.*


%files devel
%dir %{_includedir}/kqueue/
%dir %{_includedir}/kqueue/sys/
%{_includedir}/kqueue/sys/event.h
%{_libdir}/libkqueue.a
%{_libdir}/libkqueue.so
%{_libdir}/pkgconfig/libkqueue.pc
%{_mandir}/man2/kevent.2.gz
%{_mandir}/man2/kqueue.2.gz


%changelog
* Sun Dec 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.6-1
- Initial release
- Version 1.0.6
