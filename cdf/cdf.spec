Name:		cdf
Version:	0.2
Release:	1%{?dist}
Summary:	Colorized df utility

Group:		Applications/Text
License:	GPLv2
URL:		http://bmp-plugins.berlios.de/misc/cdf/cdf.html
Source0:	http://download.berlios.de/bmp-plugins/cdf-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
The main features of cdf are:
* customizable color schemes
* eye-friendly capacity bars
* most of such utils needs some 3rd party libraries, python interpreter and
  so on, while cdf written in pure C


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{_bindir}/cdf


%changelog
* Fri May 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2-1
- Initial release
