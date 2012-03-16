Name:		nvidia-no-prelink
Version:	1.0
Release:	1%{?dist}
Summary:	Disable prelinking on nVidia libraries

Group:		System Environment/Libraries
License:	GPLv2+
URL:		http://made.by.me
Source0:	%{name}.conf

BuildArch:	noarch

Requires:	prelink

%description
Disable prelinking on the proprietary nVidia libraries since it can cause Wine
applications to crash or hang the entire system.


%prep
# No tarball


%build
# No build necessary


%install
rm -rf $RPM_BUILD_ROOT
install -dm755 $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/
install -m644 %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/prelink.conf.d/%{name}.conf


%changelog
* Fri Mar 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0-1
- Initial release
