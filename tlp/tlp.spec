# This spec file was originally written by:
#
#   Christian Dersch <chrisdersch~at~googlemail~dot~com>
#
# and modified for Fedora packaging by:
#
#   Xiao-Long Chen <chenxiaolong@cxl.epac.to>
#
# This file is published under the same license terms as the package itself.
#

Name:		tlp
Version:	0.3.6
Release:	2
Summary:	Advanced energy-saving tools for laptops
Group:		System Environment/Daemons
License:	GPLv2
URL:		https://github.com/linrunner/TLP/wiki/TLP-Linux-Advanced-Power-Management
Source0:	%{name}-%{version}.tar.xz
# Tarballs are not provided upstream, so create one from git tags
Source1:	get-source-from-git.sh
Patch0:		0001-Use-etc-sysconfig-on-Fedora.patch
Patch1:		0002-Do-not-hardcode-paths-and-use-libexecdir.patch
Patch2:		0003-Fix-init-script-for-Fedora.patch
Patch3:		0004-Fix-Makefile-replace-LIBEXECDIR.patch

BuildRequires:	pm-utils desktop-file-utils
Requires:	dmidecode hdparm perl pm-utils rfkill wireless-tools
Requires(post):	chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts


%description
TLP is a collection of scripts enabling laptop-mode and
implementing power save features for laptop hardware.
For some additional features supported by IBM/Lenovo ThinkPads,
the tp_smapi package matching your kernel is required.	


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
# No build necessary


%install
rm -rf $RPM_BUILD_ROOT
make install LIBEXECDIR=libexec LIBDIR=%{_lib} DESTDIR=$RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man8/
install -m644 man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m644 man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/tlp.desktop


%files
%defattr(-,root,root,-)
%doc COPYING LICENSE README

%{_bindir}/bluetooth
%{_bindir}/run-on-ac
%{_bindir}/run-on-bat
%{_bindir}/tlp-stat
%{_bindir}/tlp-usblist
%{_bindir}/wifi
%{_bindir}/wwan
%{_sbindir}/tlp
%{_sysconfdir}/NetworkManager/dispatcher.d/99tlp-rdw-nm
/lib/udev/rules.d/40-tlp-rdw.rules
/lib/udev/rules.d/40-tlp.rules
/lib/udev/tlp-rdw-udev
/lib/udev/tlp-usb-udev

%{_mandir}/man1/bluetooth.1.gz
%{_mandir}/man1/run-on-ac.1.gz
%{_mandir}/man1/run-on-bat.1.gz
%{_mandir}/man1/wifi.1.gz
%{_mandir}/man1/wwan.1.gz
%{_mandir}/man8/tlp-stat.8.gz
%{_mandir}/man8/tlp.8.gz

%{_sysconfdir}/bash_completion.d/tlp
%{_sysconfdir}/xdg/autostart/tlp.desktop
%config(noreplace) %{_sysconfdir}/sysconfig/tlp
%{_initddir}/tlp

%{_libdir}/pm-utils/power.d/zztlp
%{_libdir}/pm-utils/sleep.d/48tlp-rdw-lock
%{_libdir}/pm-utils/sleep.d/49bay
%{_libdir}/pm-utils/sleep.d/49wwan
%{_libexecdir}/tlp-pm/tlp-functions
%{_libexecdir}/tlp-pm/tlp-nop
%{_libexecdir}/tlp-pm/tlp-rf-func


%post
/sbin/chkconfig --add tlp


%preun
if [ ${1} -eq 0 ]; then
  /sbin/service tlp stop &>/dev/null || :
  /sbin/chkconfig --del tlp
fi


%postun
if [ ${1} -ge 1 ]; then
  /sbin/service tlp condrestart &>/dev/null || :
fi


%changelog
* Tue Apr 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-2
- Fix Makefile: Didn't replace @LIBEXECDIR@

* Tue Apr 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Package for Fedora

* Tue Dec 20 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Upgrade to version 0.3.5

* Thu Nov 24 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Downgrade to version 0.3.3 due to problems with the non-official 0.3.4

* Thu Nov 17 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Upgrade to version 0.3.4

* Wed Jul 27 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Fixed issue with tlp-stat (usb) (tlp 0.3.2-4, thanks to linrunner)
- Fixed issue in spec, now config file won't be overwritten after updates

* Mon Jul 25 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Fixed issue with usb suspend (thanks to linrunner)
- Corrected the makefile_suse.diff patch (wrong path)

* Mon Jul 18 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Upgrade to version 0.3.2

* Sun May 01 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Upgrade to version 0.3.0.201

* Mon Mar 21 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Fixed wrong path for scripts in /usr/lib/pm-utils/

* Sun Mar 20 2011 Christian Dersch <chrisdersch~at~googlemail~dot~com>
- Initial build
