%define _svn_rev _SVN_REV_
%define _sdl_ver 1.2.14

Name:		diyps3controller-svn
Version:	0.40
Release:	1.%{_svn_rev}svn%{?dist}
Summary:	Control a video game console with a PC

Group:		Applications/Communications
License:	GPLv2
URL:		https://code.google.com/p/diyps3controller/
Source0:	diyps3controller-%{_svn_rev}svn.tar.xz
Source1:	http://www.libsdl.org/release/SDL-%{_sdl_ver}.tar.gz

BuildRequires:	libusb1-devel
BuildRequires:	wxGTK-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	glib2-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXi-devel
BuildRequires:	desktop-file-utils


%description
The purpose of this software is to control a video game console with a PC. It
works with the PS3 and there is experimental support for the Xbox 360.

It operates:
* over bluetooth: works with Linux (PS3) only. A compatible bluetooth dongle is
  required.
* over usb: works with Linux (PS3, 360) and Windows (PS3). A usb-usb adapter is
  required.

The application gets data from the PC peripherals (mice, keyboards and joysticks
) and sends controls to the PS3 over bluetooth or usb. Other controls such as
gesture or voice are possible through the use of external software that emulate
PC peripherals.


%prep
%setup -q -n diyps3controller-%{_svn_rev}svn

# Patched libSDL required
pushd libsdl
tar zxvf '%{SOURCE1}'

pushd SDL-%{_sdl_ver}
patch -Np1 -i ../patch
%configure
make %{?_smp_mflags}
popd

mkdir lib
mkdir -p include/SDL
cp SDL-%{_sdl_ver}/build/.libs/libSDL.so lib/
cp SDL-%{_sdl_ver}/include/* include/SDL/
popd


%build
pushd GIMX
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd GIMX
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd $RPM_BUILD_ROOT/usr
mv lib %{_lib}
popd

# Validate desktop files
for i in $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop; do
  sed -i '/Version=0\.25/d' ${i}
  desktop-file-validate ${i}
done

# Do not use setuid permissions
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/*


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/bdaddr
%{_bindir}/emu
%{_bindir}/emuclient
%{_bindir}/gimx-bluetooth
%{_bindir}/gimx-config
%{_bindir}/gimx-fpsconfig
%{_bindir}/gimx-serial
%{_bindir}/hcirevision
%{_bindir}/sixaddr
%{_bindir}/usbspoof
%{_libdir}/libSDL-9.2.so.0
%{_datadir}/applications/gimx-bluetooth.desktop
%{_datadir}/applications/gimx-config.desktop
%{_datadir}/applications/gimx-fpsconfig.desktop
%{_datadir}/applications/gimx-serial.desktop
%{_datadir}/pixmaps/gimx-bluetooth.png
%{_datadir}/pixmaps/gimx-config.png
%{_datadir}/pixmaps/gimx-fpsconfig.png
%{_datadir}/pixmaps/gimx-serial.png


%changelog
* Tue Jun 19 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.41-1
- SVN Package initial release
