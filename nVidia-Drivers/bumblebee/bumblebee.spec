# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		bumblebee
Version:	3.0.1
Release:	1%{?dist}
Summary:	A project aiming to support NVIDIA Optimus technology under Linux

Group:		System Environment/Base
License:	GPLv3
URL:		http://bumblebee-project.org/
Source0:	https://github.com/downloads/Bumblebee-Project/Bumblebee/bumblebee-%{version}.tar.gz

BuildRequires:	help2man
BuildRequires:	systemd-units

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(x11)

Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd

Requires(pre):	shadow-utils

Requires:	akmod-bbswitch
#Requires:	akmod-nvidia
Requires:	VirtualGL

%description
The Bumblebee Project proudly presents version 3.0 of Bumblebee, a project
aiming to support NVIDIA Optimus technology under Linux. After two months of
hard work this version has finally been considered stable enough for release.

If you thought that Bumblebee was dead, it's still alive and kicking! See
http://wiki.bumblebee-project.org/FAQ

The project has been fully rewritten in the C programming language, providing
increased performance and reliability, mostly thanks to a new developer in the
project, Jaron Viëtor (a.k.a. Thulinma). That bring the number of main
developers to 4, the three other ones being Peter Wu (a.k.a. Lekensteyn),
Joaquín Ignacio Aramendía (a.k.a. Samsagax) and Bruno Pagani (a.k.a.
ArchangeGabriel).

The most important new feature is automatic power management support. Yes, in
Bumblebee 3.0 "Tumbleweed", you've got Power Management working out of the box,
without any manual configuration needed. That's not the only one though, the
full changelog could be found at http://bumblebee-project.org/release-notes-3.0


%prep
%setup -q


%build
%configure \
%ifarch x86_64
  CONF_LDPATH_NVIDIA=%{_libdir}/nvidia:%{_prefix}/lib/nvidia \
%else
  CONF_LDPATH_NVIDIA=%{_libdir}/nvidia \
%endif
  CONF_MODPATH_NVIDIA=%{_libdir}/xorg/modules/extensions/nvidia

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Install systemd service
install -dm755 $RPM_BUILD_ROOT%{_unitdir}/
install -m644 scripts/systemd/bumblebeed.service $RPM_BUILD_ROOT%{_unitdir}/

# Put documentation in correct directory
mv $RPM_BUILD_ROOT%{_docdir}/{%{name},%{name}-%{version}}/


%pre
getent group bumblebee >/dev/null || groupadd -r bumblebee


%post
%if 0%{fedora} >= 18
%systemd_post bumblebeed.service
%else
if [ ${1} -eq 1 ]; then
  systemctl daemon-reload &>/dev/null || :
fi
%endif

%preun
%if 0%{fedora} >= 18
%systemd_preun bumblebeed.service
%else
if [ ${1} -eq 0 ]; then
  systemctl --no-reload disable bumblebeed.service &>/dev/null || :
  systemctl stop bumblebeed.service &>/dev/null || :
fi
%endif

%postun
%if 0%{fedora} >= 18
%systemd_postun_with_restart bumblebeed.service
%else
systemctl daemon-reload &>/dev/null || :
if [ ${1} -ge 1 ]; then
  systemctl try-restart bumblebeed.service &>/dev/null || :
fi
%endif


%files
%doc %{_docdir}/%{name}-%{version}/
%{_bindir}/bumblebee-bugreport
%{_bindir}/optirun
%{_sbindir}/bumblebeed
%dir %{_sysconfdir}/bash_completion.d/
%dir %{_sysconfdir}/bumblebee/
%{_sysconfdir}/bash_completion.d/bumblebee
%config(noreplace) %{_sysconfdir}/bumblebee/bumblebee.conf
%config(noreplace) %{_sysconfdir}/bumblebee/xorg.conf.nouveau
%config(noreplace) %{_sysconfdir}/bumblebee/xorg.conf.nvidia
%{_mandir}/man1/bumblebeed.1.gz
%{_mandir}/man1/optirun.1.gz
%{_unitdir}/bumblebeed.service


%changelog
* Fri Oct 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.1-1
- Initial release
- Version 3.0.1
