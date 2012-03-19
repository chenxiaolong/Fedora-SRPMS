# Disable useless debuginfo package
%define debug_package %{nil}

Name:		overlook-fing
Version:	1.4
Release:	1%{?dist}
Summary:	Ultimate tool for network discovery and scanning

Group:		Applications/Internet
License:	Redistributable, no modification permitted
URL:		http://over-look.com/site/
Source0:	http://www.over-look.com/site/index.php/fing-download-linux/64bit/113-overlook-fing-1-4/download

BuildRequires:	dos2unix


%description
Born from the ashes of Look@LAN, Fing is the ultimate command line tool for
network and service discovery. Taking advantage of a brand new cross-platform
network engine, it reaches an impressive discovery sharpness and speed.


%prep
%setup -q -c -n %{name}-%{version}


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
# Install libraries
install -dm755 $RPM_BUILD_ROOT%{_libdir}/fing/
install -m755 ./usr/lib/fing/*.so* $RPM_BUILD_ROOT%{_libdir}/fing/

# Install binaries
install -dm755 $RPM_BUILD_ROOT%{_libexecdir}/fing/
install -m755 ./usr/lib/fing/fing.bin \
              $RPM_BUILD_ROOT%{_libexecdir}/fing/

# Install launcher script
cat > fing.launcher << EOF
#!/bin/sh
LD_LIBRARY_PATH="%{_libdir}/fing" %{_libexecdir}/fing/fing.bin ${@}
EOF
install -dm755 $RPM_BUILD_ROOT%{_bindir}/
install -m755 fing.launcher $RPM_BUILD_ROOT%{_bindir}/fing

# Install data files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/fing/template/conf/
install -m644 ./usr/share/fing/template/conf/*.properties \
              $RPM_BUILD_ROOT%{_datadir}/fing/template/conf/

# CRLF -> Unix
dos2unix ./usr/share/fing/doc/*.txt


%files
%defattr(-,root,root,-)
%doc ./usr/share/fing/doc/*.txt
%{_bindir}/fing
%{_libdir}/fing/*.so*
%{_libexecdir}/fing/fing.bin
%{_datadir}/fing/template/conf/*.properties


%changelog
* Mon Mar 19 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.4-1
- Initial release
