Name:		libspotify
Version:	10.1.16
Release:	1%{?dist}
Summary:	C API package to utilize the Spotify music streaming service

Group:		System Environment/Libraries
License:	Redistributable, no modification permitted
URL:		http://developer.spotify.com/en/libspotify/overview/
%ifarch x86_64 i686
Source0:	http://developer.spotify.com/download/libspotify/libspotify-%{version}-Linux-%{_arch}-release.tar.gz
%endif

Requires:	glibc

%description
The libspotify C API package allows third-party developers to write applications
that utilize the Spotify music streaming service.


%package devel
Summary:	Headers for libspotify


%description devel
The libspotify C API package allows third-party developers to write applications
that utilize the Spotify music streaming service.

This package contains development files for libspotify


%prep
%setup -q -n %{name}-Linux-%{_arch}-release


%build
#make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
# Disable Makefile from running ldconfig
sed -i 's/ldconfig//' Makefile
# Fix pkgconfig file
sed -i '/sed.*PKG_PREFIX/ s/:$(prefix)/:\/usr/g' Makefile
make install prefix=$RPM_BUILD_ROOT/usr
# Fix libdir
if [[ "/usr/lib" != "%{_libdir}" ]]; then
  mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}
fi


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE ChangeLog README
%{_libdir}/%{name}.so*


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}



%changelog
* Mon Jan 2 2011 Xiao-Long Chen <chenxiaolong@cxl.epac.to> 10.1.16-1.fc16
- Initial release
