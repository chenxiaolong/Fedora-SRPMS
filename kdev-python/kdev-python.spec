# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Stop rpmbuild from complaining
%global _python_bytecompile_errors_terminate_build 0

%filter_from_requires /libpython2\.7/d
%filter_setup

Name:		kdev-python
Version:	1.4.1
Release:	1%{?dist}
Summary:	KDevelop plugin which provides Python language support

Group:		Development/Languages
# Unsure about the license
License:	Freely redistributable without restriction
# Also http://kde-apps.org/content/show.php/kdev-python?content=155472
URL:		https://projects.kde.org/projects/playground/devtools/plugins/kdev-python
Source0:	http://download.kde.org/stable/kdevelop/kdev-python/%{version}/src/kdev-python-v%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	kdevelop-pg-qt-devel
BuildRequires:	kdevplatform-devel

Requires:	kdevelop

%description
kdev-python is the Python language support plugin for the KDevelop Integrated
Development Environment. It features:

* Code completion
* Syntax highlighting
* Navigation features: Tooltips, Quickopen, Class Browser, ...
* Basic Python Debugger (pdb) support
* ... and much more!


%prep
%setup -q -n %{name}-v%{version}


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags} parser


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc DESIGN TODO
%dir %{_kde4_appsdir}/kdevappwizard/
%dir %{_kde4_appsdir}/kdevappwizard/templates/
%{_kde4_appsdir}/kdevappwizard/templates/django_project.tar.bz2
%{_kde4_appsdir}/kdevappwizard/templates/qtdesigner_app.tar.bz2
%{_kde4_appsdir}/kdevappwizard/templates/simple_pythonapp.tar.bz2
%{_kde4_appsdir}/kdevpythonsupport/
%{_kde4_datadir}/kde4/services/kdevpdb.desktop
%{_kde4_datadir}/kde4/services/kdevpythonsupport.desktop
%{_kde4_libdir}/kde4/kdevpdb.so
%{_kde4_libdir}/kde4/kdevpythonlanguagesupport.so
%{_kde4_libdir}/libkdev4pythoncompletion.so
%{_kde4_libdir}/libkdev4pythonduchain.so
%{_kde4_libdir}/libkdev4pythonparser.so
%{_kde4_libdir}/libpython2.7-kdevelop.so
%{_kde4_libdir}/libpython2.7-kdevelop.so.1.0


%changelog
* Sun Nov 25 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.4.1-1
- Initial release
- Version 1.4.1
