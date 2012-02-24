# apsw version must match sqlite version

%define sqlite_version 3.7.7.1
%define real_version %{sqlite_version}-r1

Name:		python-apsw
Version:	3.7.7.1+r1
Release:	1%{?dist}
Summary:	Another Python SQLite Wrapper

Group:		Development/Languages
# Any OSI approved license
License:	Freely redistributable without restriction
URL:		https://code.google.com/p/apsw/
Source0:	https://apsw.googlecode.com/files/apsw-%{real_version}.zip

BuildRequires:	python-devel
BuildRequires:	sqlite-devel >= %{sqlite_version}
Requires:	sqlite >= %{sqlite_version}


%description
APSW is a Python wrapper for the SQLite embedded relational database engine. In
contrast to other wrappers such as pysqlite it focuses on being a minimal layer
over SQLite attempting just to translate the complete SQLite API into Python.


%package doc
Summary:	Another Python SQLite Wrapper - Documentation
BuildArch:	noarch


%description doc
APSW is a Python wrapper for the SQLite embedded relational database engine. In
contrast to other wrappers such as pysqlite it focuses on being a minimal layer
over SQLite attempting just to translate the complete SQLite API into Python.


%prep
%setup -q -n apsw-%{real_version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Remove hidden file in documentation directory
rm doc/.buildinfo

# Install documentation
install -dm755 $RPM_BUILD_ROOT%{_docdir}/
cp -avr doc/ $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitearch}/apsw*


%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/


%changelog
* Fri Feb 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.7.7.1+r1-1
- Initial release
- Version 3.7.7.1-r1
