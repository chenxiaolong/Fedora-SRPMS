# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		nxt-python
Version:	2.2.2
Release:	1%{?dist}
Summary:	A pure-python interface for the Lego Mindstorms NXT

Group:		Applications/Engineering
License:	GPLv3
URL:		https://code.google.com/p/nxt-python/
Source0:	https://nxt-python.googlecode.com/files/nxt-python-%{version}.tar.gz 

BuildArch:	noarch

BuildRequires:	python-devel

Requires:	pybluez
Requires:	pygtk2
Requires:	pyusb
Requires(pre):	shadow-utils

Provides:	nxt_python
Obsoletes:	nxt_python

%description
NXT-Python is a package for controlling a LEGO NXT robot using the Python
programming language. It can communicate using either USB or Bluetooth. It is
available under the Gnu GPL v3 license. It is based on NXT_Python, where
releases halted in May 2007.


%prep
%setup -q


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install udev rule
install -dm755 $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/
cat << EOF >> $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/70-lego.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="0694", GROUP="lego", MODE="0660"
EOF


%pre
getent group lego >/dev/null || groupadd -r lego

 
%files
%doc LICENSE README
%doc examples/*
%{_bindir}/nxt_filer
%{_bindir}/nxt_push
%{_bindir}/nxt_server
%{_bindir}/nxt_test
%{python_sitelib}/*
%{_prefix}/lib/udev/rules.d/70-lego.rules


%changelog
* Tue Dec 25 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.2-1
- Initial release
- Version 2.2.2
