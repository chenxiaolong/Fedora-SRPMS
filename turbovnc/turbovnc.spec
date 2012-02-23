# This spec file is largely based off of the Fedora 17 TigerVNC spec file

Name:		turbovnc
Version:	1.0.2
Release:	1%{?dist}
Summary:	Highly-optimized VNC server for real-time video applications

Group:		User Interface/Desktops
License:	GPLv2
URL:		http://www.virtualgl.org/
Source0:	http://downloads.sourceforge.net/project/virtualgl/TurboVNC/%{version}/turbovnc-%{version}.tar.gz

# systemd service
Source1:	turbovnc.service
# Deprecated note
Source2:	turbovnc.sysconfig
# Desktop file
Source3:	turbovnc.desktop

# Avoid conflicts with TigerVNC
Patch0:		resolve_conflicts_with_TigerVNC.patch
# Move java classes to /usr/share/turbovnc/classes
Patch1:		change_java_jar_path.patch

BuildRequires:	automake
BuildRequires:	imake
BuildRequires:	desktop-file-utils
BuildRequires:	turbojpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	libXaw-devel
BuildRequires:	pam-devel
BuildRequires:	systemd-units

Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.  TurboVNC is a sleek and
fast VNC distribution, containing a high-performance implementation of
Tight encoding designed to work in conjunction with VirtualGL.


%package server
Summary:	TurboVNC server
Group:		User Interface/X
Requires:	%{name}-server-minimal
Requires:	xorg-x11-xauth

%description server
The VNC system allows you to access the same desktop from a wide
variety of platforms.  This package includes set of utilities
which make usage of TurboVNC server more user friendly.


%package server-minimal
Summary:	A minimal installation of TurboVNC server
Group:		User Interface/X

Requires:	mesa-dri-drivers, xkeyboard-config, xorg-x11-xkb-utils

%description server-minimal
The VNC system allows you to access the same desktop from a wide
variety of platforms. This package contains minimal installation
of TurboVNC server, allowing others to access the desktop on your
machine.


%package server-applet
Summary:	Java TurboVNC viewer applet for TurboVNC server
Group:		User Interface/X
Requires:	turbovnc-server, java, jpackage-utils
BuildArch:	noarch

%description server-applet
The Java TurboVNC viewer applet for web browsers. Install this package to allow
clients to use web browser when connect to the TurboVNC server.


%prep
%setup -q -n vnc/vnc_unixsrc

%patch0 -p1
%patch1 -p1


%build
mv vncserver.in vncserver.turbo.in

autoreconf -vfi

# turbojpeg linking error
export JPEG_LDFLAGS="-L%{_libdir} -lturbojpeg"

%configure --with-x

make %{?_smp_mflags}

# xserver build target does not support parallel builds
make xserver -j1 #{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make xserver-install DESTDIR=$RPM_BUILD_ROOT

# Install systemd service
install -dm755 $RPM_BUILD_ROOT%{_unitdir}/
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}@.service

# Remove old SysVinit scripts
rm -rvf $RPM_BUILD_ROOT%{_initddir}

# sysconfig file
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

# desktop file
install -dm755 $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications/ %{SOURCE3}

# Rename manual pages so that they don't conflict with TigerVNC
mv $RPM_BUILD_ROOT%{_mandir}/man1/vncserver{,.turbo}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/vncviewer{,.turbo}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/vncpasswd{,.turbo}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/vncconnect{,.turbo}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/Xvnc{,.turbo}.1

# What the heck is the manual page for Xserver doing here?
rm $RPM_BUILD_ROOT%{_mandir}/man1/Xserver.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README ReadMe.rtf
%{_bindir}/vncviewer.turbo
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/vncviewer.turbo.1.gz


%files server
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/turbovncserver-auth.conf
%config(noreplace) %{_sysconfdir}/turbovncserver.conf
# No longer a configuration file, just a notice, so no need for 'noreplace'
%config %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}@.service
%{_bindir}/vncserver.turbo
%{_bindir}/autocutsel
%{_mandir}/man1/vncserver.turbo.1.gz


%files server-minimal
%defattr(-,root,root,-)
%{_bindir}/vncconnect.turbo
%{_bindir}/vncpasswd.turbo
%{_bindir}/Xvnc.turbo
%{_mandir}/man1/vncconnect.turbo.1.gz
%{_mandir}/man1/vncpasswd.turbo.1.gz
%{_mandir}/man1/Xvnc.turbo.1.gz


%files server-applet
%defattr(-,root,root,-)
%doc classes/README
%{_datadir}/%{name}/classes/*


%post server
if [ ${1} -eq 1 ]; then
  # Initial installation
  /bin/systemctl daemon-reload &>/dev/null || :
fi


%preun server
if [ ${1} -eq 0 ]; then
  # Package removal, not upgrade
  SERVICES=$(ls /etc/systemd/system/ | grep 'turbovnc@:.*\.service' 2>/dev/null)
  # Try to stop user provided TurboVNC services, if any
  if [ ! -z "${SERVICES}" ]; then
    for i in ${SERVICES}; do
      /bin/systemctl --no-reload disable ${i} &>/dev/null || :
      /bin/systemctl stop ${i} &>/dev/null || :
    done
  fi
fi


%postun server
/bin/systemctl daemon-reload &>/dev/null || :
if [ ${1} -ge 1 ]; then
  # Package upgrade, not uninstall
  SERVICES=$(ls /etc/systemd/system/ | grep 'turbovnc@:.*\.service' 2>/dev/null)
  # Try to restart user provided TurboVNC services, if any
  if [ ! -z "${SERVICES}" ]; then
    for i in ${SERVICES}; do
      /bin/systemctl try-restart ${i} &>/dev/null || :
    done
  fi
fi


%changelog
* Wed Feb 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.2-1
- Initial release
- Version 1.0.2
