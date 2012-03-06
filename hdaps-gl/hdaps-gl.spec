Name:		hdaps-gl
Version:	0.0.5
Release:	1%{?dist}
Summary:	Lenovo/IBM ThinkPad accelerometer OpenGL monitor

Group:		Applications/System
License:	GPL+
URL:		http://hdaps.sf.net/
Source0:	http://downloads.sourceforge.net/project/hdaps/hdaps-gl/hdaps-gl-%{version}/hdaps-gl-%{version}.tar.gz

BuildRequires:	freeglut-devel
Requires:	tp_smapi-kmod


%description
A tool that renders a fake ThinkPad laptop on the screen and tilts it based on
the data from the hdaps accelerometer kernel module from tp_smapi.


%prep
%setup -q


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
install -dm755 $RPM_BUILD_ROOT%{_bindir}/
install -m755 hdaps-gl $RPM_BUILD_ROOT%{_bindir}/


%files
%defattr(-,root,root,-)
%{_bindir}/hdaps-gl


%changelog
* Tue Mar 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.5-1
- Initial release
- Version 0.0.5
