# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _git_commit cec8d2183637e15313253a52648515d449bedff1

Name:		thinkdisp
Version:	1.3.1
Release:	1%{?dist}
Summary:	Indicator to automate the use of multiple monitors on NVIDIA Optimus systems

Group:		User Interface/X
License:	BSD
URL:		http://sagark.org/thinkdisp-about-installation/
Source0:	thinkdisp-%{version}.tar.xz
# Run this script to create the tarball from git
Source1:	create-git-snapshot.sh

# Use configuration in home directory
Patch0:		0001_User_Config.patch

BuildRequires:	desktop-file-utils
BuildRequires:	python-devel

Requires:	akmod-bbswitch
Requires:	bumblebee
Requires:	hybrid-screenclone
Requires:	notify-osd
Requires:	python-appindicator

%description
thinkdisp is a Display Manager that automates the many scripts/commands required
to use multiple monitors on Thinkpads with Nvidia Optimus. It appears as an
indicator applet for easy access.


%prep
%setup -q

%patch0 -p1 -b .user-config


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

desktop-file-validate \
  $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/thinkdisp.desktop

mv $RPM_BUILD_ROOT%{_datadir}/thinkdisp/{config,sample}.ini


%files
%doc README.md
%attr(4755,root,root) %{_bindir}/killdisp
%{_bindir}/thinkdisp
%dir %{_datadir}/thinkdisp/
%{_datadir}/thinkdisp/sample.ini
%{_sysconfdir}/xdg/autostart/thinkdisp.desktop
%{python_sitelib}/Thinkdisp-%{version}-py2.7.egg-info
%{python_sitelib}/thinkdisputil/


%changelog
* Sun Oct 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3.1-1
- Initial release
- Version 1.3.1
