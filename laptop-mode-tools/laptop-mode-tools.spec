# Written By: Xiao-Long Chen chenxiaolong@cxl.epac.to>

Name:		laptop-mode-tools
Version:	1.61
Release:	1%{?dist}
Summary:	Power saving tools for Linux

Group:		System Environment/Base
License:	GPLv2
URL:		http://samwel.tk/laptop_mode/
Source0:	http://samwel.tk/laptop_mode/tools/downloads/laptop-mode-tools_%{version}.tar.gz

Source1:	laptop-mode-tools.service

Patch0:		0001_Use_systemd.patch
Patch1:		0002_Manage_with_systemd.patch
Patch2:		0003_Fix_udev_rules.patch
Patch3:		0004_Fix_paths.patch
Patch4:		0005_Hal_is_deprecated.patch

# pm-utils is arch-dependant (not really, but scripts were placed in
# /usr/lib64/pm-utils/)
#BuildArch:	noarch

Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

Requires:	acpid
Requires:	bluez
Requires:	ethtool
Requires:	hdparm
Requires:	sdparm
Requires:	wireless-tools
Requires:	xorg-x11-server-utils

%description
Laptop Mode Tools is a laptop power saving package for Linux systems. It allows
you to extend the battery life of your laptop, in several ways. It is the
primary way to enable the Laptop Mode feature of the Linux kernel, which lets
your hard drive spin down. In addition, it allows you to tweak a number of other
power-related settings using a simple configuration file.


%prep
%setup -q -n %{name}_%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
# Nothing to build


%install
export MAN_D=%{_mandir}
export INIT_D="none"
export DESTDIR=$RPM_BUILD_ROOT
export INSTALL="install"
./install.sh

# Install systemd service
install -dm755 $RPM_BUILD_ROOT%{_unitdir}/
install -m644 '%{SOURCE1}' $RPM_BUILD_ROOT%{_unitdir}/

# Fedora does not have apm
rm -rv $RPM_BUILD_ROOT%{_sysconfdir}/apm/

# Fedora does not have apmud either
rm -rv $RPM_BUILD_ROOT%{_sysconfdir}/power/

# Put udev rules in /usr/lib/udev/
mv $RPM_BUILD_ROOT{%{_sysconfdir},%{_prefix}/lib}/udev/

# Move udev scripts from /lib/udev/ to /usr/lib/udev/
mv $RPM_BUILD_ROOT{,%{_prefix}}/lib/udev/lmt-udev

# Move pm-utils scripts to correct directory
%if %{_lib} != "lib"
install -dm755 $RPM_BUILD_ROOT%{_libdir}/
mv $RPM_BUILD_ROOT{/usr/lib,%{_libdir}}/pm-utils/
%endif

install -dm755 $RPM_BUILD_ROOT/run/laptop-mode-tools/


%post
if [ ${1} -eq 1 ]; then 
  systemctl daemon-reload &>/dev/null || :
fi

%preun
if [ ${1} -eq 0 ]; then
  systemctl --no-reload disable laptop-mode-tools.service &>/dev/null || :
  systemctl stop laptop-mode-tools.service &>/dev/null || :
fi

%postun
systemctl daemon-reload &>/dev/null || :
if [ ${1} -ge 1 ]; then
  systemctl try-restart laptop-mode-tools.service &>/dev/null || :
fi


%files
%doc README Documentation/*.txt
%{_sbindir}/laptop_mode
%{_sbindir}/lm-profiler
%{_sbindir}/lm-syslog-setup
%{_sysconfdir}/acpi/actions/lm_*.sh
%{_sysconfdir}/acpi/events/lm_*
%config(noreplace) %dir %{_sysconfdir}/laptop-mode/
%config(noreplace) %dir %{_sysconfdir}/laptop-mode/conf.d/
%config(noreplace) %{_sysconfdir}/laptop-mode/*.conf
%config(noreplace) %{_sysconfdir}/laptop-mode/conf.d/*.conf
%{_libdir}/pm-utils/sleep.d/01laptop-mode
%{_prefix}/lib/udev/rules.d/99-laptop-mode.rules
%{_prefix}/lib/udev/lmt-udev
%dir %{_datadir}/laptop-mode-tools/
%dir %{_datadir}/laptop-mode-tools/module-helpers/
%dir %{_datadir}/laptop-mode-tools/modules/
%{_datadir}/laptop-mode-tools/module-helpers/*
%{_datadir}/laptop-mode-tools/modules/*
%{_mandir}/man8/laptop-mode.conf.8.gz
%{_mandir}/man8/laptop_mode.8.gz
%{_mandir}/man8/lm-profiler.8.gz
%{_mandir}/man8/lm-profiler.conf.8.gz
%{_mandir}/man8/lm-syslog-setup.8.gz
%{_unitdir}/laptop-mode-tools.service

%dir %{_sysconfdir}/laptop-mode/lm-ac-stop/
%dir %{_sysconfdir}/laptop-mode/nolm-ac-start/
%dir %{_sysconfdir}/laptop-mode/modules/
%dir %{_sysconfdir}/laptop-mode/nolm-ac-stop/
%dir %{_sysconfdir}/laptop-mode/batt-stop/
%dir %{_sysconfdir}/laptop-mode/batt-start/
%dir %{_sysconfdir}/laptop-mode/lm-ac-start/
%dir %{_sysconfdir}/laptop-mode/conf.d/board-specific/

%dir /run/laptop-mode-tools/

# Files created during runtime
%attr(644,-,-) %ghost /run/laptop-mode-tools/disabled-video-outputs
%attr(644,-,-) %ghost /run/laptop-mode-tools/enabled
%attr(644,-,-) %ghost /run/laptop-mode-tools/nolm-mountopts
%attr(644,-,-) %ghost /run/laptop-mode-tools/start-stop-undo-actions
%attr(644,-,-) %ghost /run/laptop-mode-tools/state
%attr(644,-,-) %ghost /run/laptop-mode-tools/state-brightness-command

%attr(644,-,-) %ghost /run/lock/lmt-battpoll.lock
%attr(644,-,-) %ghost /run/lock/lmt-invoc.lock
%attr(644,-,-) %ghost /run/lock/lmt-req.lock


%changelog
* Wed Sep 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.61-1
- Initial release
- Version 1.61
