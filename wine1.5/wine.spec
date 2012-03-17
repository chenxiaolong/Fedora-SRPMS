%global no64bit 0
Name:           wine
Version:        1.5.0
Release:        1%{?dist}
Summary:        A Windows 16/32/64 bit emulator

Group:          Applications/Emulators
License:        LGPLv2+
URL:            http://www.winehq.org/
Source0:        http://ibiblio.org/pub/linux/system/emulators/wine/wine-%{version}.tar.bz2
Source10:       http://downloads.sourceforge.net/wine/wine-%{version}.tar.bz2.sign

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop

# wine bugs

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if !%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm}
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  freeglut-devel
BuildRequires:  lcms-devel
BuildRequires:  libieee1284-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libusb-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  ncurses-devel
BuildRequires:  openldap-devel
BuildRequires:  unixODBC-devel
BuildRequires:  openssl-devel
BuildRequires:  sane-backends-devel
BuildRequires:  zlib-devel
BuildRequires:  fontforge freetype-devel
BuildRequires:  libgphoto2-devel
# #217338
# isdn has issues on ARM atm
%ifnarch %{arm}
BuildRequires:  isdn4k-utils-devel
%endif
# modular x
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libXxf86dga-devel libXxf86vm-devel
BuildRequires:  libXrandr-devel libXrender-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  cups-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libXcursor-devel
BuildRequires:  dbus-devel
%if !0%{?fedora} >= 16
BuildRequires:  hal-devel
%endif
BuildRequires:  gnutls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  gsm-devel
BuildRequires:  libv4l-devel
BuildRequires:  fontpackages-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel
BuildRequires:  libtiff-devel
BuildRequires:  prelink
BuildRequires:  gettext-devel
BuildRequires:  chrpath

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildRequires:  openal-soft-devel
BuildRequires:  icoutils
%endif


Requires:       wine-desktop = %{version}-%{release}
Requires:       wine-fonts = %{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{version}-%{release}
Requires:       wine-capi(x86-32) = %{version}-%{release}
Requires:       wine-cms(x86-32) = %{version}-%{release}
Requires:       wine-ldap(x86-32) = %{version}-%{release}
Requires:       wine-twain(x86-32) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-openal(x86-32) = %{version}-%{release}
%endif
%endif

%ifarch %{ix86}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-wow(x86-32) = %{version}-%{release}
%endif
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
Requires:       wine-capi(x86-64) = %{version}-%{release}
Requires:       wine-cms(x86-64) = %{version}-%{release}
Requires:       wine-ldap(x86-64) = %{version}-%{release}
Requires:       wine-twain(x86-64) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-openal(x86-64) = %{version}-%{release}
%endif
Requires:       wine-wow(x86-64) = %{version}-%{release}
Conflicts:      wine-wow(x86-32) = %{version}-%{release}
%endif

# ARM parts
%ifarch %{arm}
Requires:       wine-core = %{version}-%{release}
Requires:       wine-capi = %{version}-%{release}
Requires:       wine-cms = %{version}-%{release}
Requires:       wine-ldap = %{version}-%{release}
Requires:       wine-twain = %{version}-%{release}
Requires:       wine-pulseaudio = %{version}-%{release}
Requires:       wine-openal = %{version}-%{release}
Requires:       wine-wow = %{version}-%{release}
%endif

%description
While Wine is usually thought of as a Windows(TM) emulator, the Wine
developers would prefer that users thought of Wine as a Windows
compatibility layer for UNIX. This package includes a program loader,
which allows unmodified Windows 3.x/9x/NT binaries to run on x86 and x86_64
Unixes. Wine does not require MS Windows, but it can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the 
wine-* sub packages.

%package core
Summary:        Wine core package
Group:          Applications/Emulators
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes:      wine-arts < 0.9.34
Provides:       wine-arts = %{version}-%{release}
Obsoletes:      wine-tools <= 1.1.27
Provides:       wine-tools = %{version}-%{release}
# removed as of 1.3.25 (new sound api)
Obsoletes:      wine-esd <= 1.3.24
Provides:       wine-esd = %{version}-%{release}
Obsoletes:      wine-jack <= 1.3.24
Provides:       wine-jack = %{version}-%{release}
# removed as of 1.3.19 (we don't support oss4)
Obsoletes:      wine-oss <= 1.3.18
Provides:       wine-oss = %{version}-%{release}
# removed as of 1.3.16
Obsoletes:      wine-nas <= 1.3.15
Provides:       wine-nas = %{version}-%{release}
# require -common so we get wine.inf (#528335)
Requires:       wine-common = %{version}-%{release}

%ifarch %{ix86}
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gnutls(x86-32)
Requires:       libXrender(x86-32)
Requires:       libXcursor(x86-32)
%endif

%ifarch x86_64
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gnutls(x86-64)
Requires:       libXrender(x86-64)
Requires:       libXcursor(x86-64)
%endif

%ifarch %{arm}
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       libXrender
Requires:       libXcursor
%endif

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%package wow
Summary:        Files for wine wow separation
Group:          Applications/Emulators

%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
%endif

%ifarch %{ix86}
Requires:       wine-core(x86-32) = %{version}-%{release}
%endif

%ifarch %{arm}
Requires:       wine-core = %{version}-%{release}
%endif

%description wow
%{summary}

%if 0%{?fedora} >= 15
%package systemd
Summary:        Systemd config for the wine binfmt handler
Group:          Applications/Emulators
Requires:       systemd >= 23
BuildArch:      noarch

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.

%package sysvinit
Summary:        SysV initscript for the wine binfmt handler
Group:          Applications/Emulators
BuildArch:      noarch

%description sysvinit
Register the wine binary handler for windows executables via SysV init files.
%endif

%package desktop
Summary:        Desktop integration features for wine
Group:          Applications/Emulators
Requires(post): /sbin/chkconfig, /sbin/service,
Requires(post): desktop-file-utils >= 0.8
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): desktop-file-utils >= 0.8
%ifarch %{arm}
Requires:       wine-core = %{version}-%{release}
%else
Requires:       wine-core(x86-32) = %{version}-%{release}
%endif
Requires:       wine-common = %{version}-%{release}
%if 0%{?fedora} >= 15
Requires:       wine-systemd = %{version}-%{release}
%endif
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
Group:         Applications/Emulators
BuildArch:     noarch
Requires:      wine-courier-fonts = %{version}-%{release}
Requires:      wine-small-fonts = %{version}-%{release}
Requires:      wine-system-fonts = %{version}-%{release}
Requires:      wine-marlett-fonts = %{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{version}-%{release}
Requires:      wine-tahoma-fonts = %{version}-%{release}
Requires:      wine-symbol-fonts = %{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
%if 0%{?fedora} > 12
Requires:      liberation-narrow-fonts
%endif

%description fonts
%{summary}

%package courier-fonts
Summary:       Wine Courier font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}


%package tahoma-fonts
Summary:       Wine Tahoma font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description tahoma-fonts
%{summary}


%package symbol-fonts
Summary:       Wine Symbol font family
Group:         User Interface/X
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package common
Summary:        Common files
Group:          Applications/Emulators
Requires:       wine-core = %{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package ldap
Summary: LDAP support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description twain
Twain support for wine

%package capi
Summary: ISDN support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description capi
ISDN support for wine

%package devel
Summary: Wine development environment
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}
%ifarch %{ix86}
Requires: wine-alsa(x86-32) = %{version}-%{release}
Requires: alsa-plugins-pulseaudio(x86-32)
%endif
%ifarch x86_64
Requires: wine-alsa(x86-64) = %{version}-%{release}
Requires: alsa-plugins-pulseaudio(x86-64)
%endif
%ifarch %{arm}
Requires: wine-alsa = %{version}-%{release}
Requires: alsa-plugins-pulseaudio
%endif

%description pulseaudio
This package pulse in the alsa pulseaudio backend to allow for pulse playback
over alsa.

%package alsa
Summary: Alsa support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%package openal
Summary: Openal support for wine
Group: System Environment/Libraries
Requires: wine-core = %{version}-%{release}

%description openal
This package adds an openal driver for wine.
%endif

%prep
%setup -q

%build
# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073

export CFLAGS="`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
 --without-xinput2 \
%ifarch x86_64
 --enable-win64 \
%endif
 --disable-tests

%{__make} TARGETFLAGS="" %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall \
        includedir=%{buildroot}%{_includedir}/wine \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
chrpath --delete %{buildroot}%{_bindir}/wineserver
%ifarch x86_64
chrpath --delete %{buildroot}%{_bindir}/wine64
%else
chrpath --delete %{buildroot}%{_bindir}/wine
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_initrddir}
install -p -c -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/wine
%if 0%{?fedora} >= 15
mkdir -p %{buildroot}%{_sysconfdir}/binfmt.d/
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/binfmt.d/wine.conf
%endif

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# extract and install icons
%if 0%{?fedora} > 10
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e '3s/368/64/'  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

%endif

# install desktop files
desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --vendor=fedora \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

cp %{SOURCE3} README-FEDORA

cp %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install fonts
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-courier-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/cou* %{buildroot}/%{_datadir}/fonts/wine-courier-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-system-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/*sys.* %{buildroot}/%{_datadir}/fonts/wine-system-fonts/
mv %{buildroot}/%{_datadir}/wine/fonts/vgas*.* %{buildroot}/%{_datadir}/fonts/wine-system-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-small-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/sma* %{buildroot}/%{_datadir}/fonts/wine-small-fonts/
mv %{buildroot}/%{_datadir}/wine/fonts/jsma* %{buildroot}/%{_datadir}/fonts/wine-small-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-marlett-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/marlett.ttf %{buildroot}/%{_datadir}/fonts/wine-marlett-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-ms-sans-serif-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/sse* %{buildroot}/%{_datadir}/fonts/wine-ms-sans-serif-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/tahoma* %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts/

install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-symbol-fonts
mv %{buildroot}/%{_datadir}/wine/fonts/symbol.ttf %{buildroot}/%{_datadir}/fonts/wine-symbol-fonts/

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

%clean
rm -rf %{buildroot}

%if 0%{?fedora} >= 15
%post sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi

%post desktop
update-desktop-database &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%else
%post desktop
update-desktop-database &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun desktop
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%postun desktop
update-desktop-database &>/dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans desktop
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post ldap -p /sbin/ldconfig
%postun ldap -p /sbin/ldconfig

%post cms -p /sbin/ldconfig
%postun cms -p /sbin/ldconfig

%post twain -p /sbin/ldconfig
%postun twain -p /sbin/ldconfig

%post capi -p /sbin/ldconfig
%postun capi -p /sbin/ldconfig

%post alsa -p /sbin/ldconfig
%postun alsa -p /sbin/ldconfig

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%post openal -p /sbin/ldconfig
%postun openal -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
# meta package

%files wow
%defattr(-,root,root,-)
%ifarch %{ix86} %{arm}
%{_bindir}/wine
%endif
%{_bindir}/wineserver
%{_libdir}/wine/wineboot.exe.so

%files core
%defattr(-,root,root,-)
%doc ANNOUNCE
%doc COPYING.LIB
%doc LICENSE
%doc LICENSE.OLD
%doc AUTHORS
%doc README-FEDORA
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%{_bindir}/winedump
%{_libdir}/wine/explorer.exe.so
%{_libdir}/wine/cabarc.exe.so
%{_libdir}/wine/control.exe.so
%{_libdir}/wine/cmd.exe.so
%{_libdir}/wine/notepad.exe.so
%{_libdir}/wine/plugplay.exe.so
%{_libdir}/wine/progman.exe.so
%{_libdir}/wine/taskmgr.exe.so
%{_libdir}/wine/winedbg.exe.so
%{_libdir}/wine/winefile.exe.so
%{_libdir}/wine/winemine.exe.so
%{_libdir}/wine/winemsibuilder.exe.so
%{_libdir}/wine/winepath.exe.so
%{_libdir}/wine/winver.exe.so
%{_libdir}/wine/wordpad.exe.so
%{_libdir}/wine/write.exe.so
%{_libdir}/wine/wusa.exe.so
%{_libdir}/wine/dxdiag.exe.so

%ifarch %{ix86} %{arm}
%{_bindir}/wine
%ifnarch %{arm}
%{_bindir}/wine-preloader
%endif
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif

%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*
%{_libdir}/wine/attrib.exe.so
%{_libdir}/wine/aspnet_regiis.exe.so
%{_libdir}/wine/cacls.exe.so
%{_libdir}/wine/cscript.exe.so
%{_libdir}/wine/expand.exe.so
%{_libdir}/wine/extrac32.exe.so
%{_libdir}/wine/hostname.exe.so
%{_libdir}/wine/ipconfig.exe.so
%{_libdir}/wine/winhlp32.exe.so
%{_libdir}/wine/mshta.exe.so
%{_libdir}/wine/msiexec.exe.so
%{_libdir}/wine/net.exe.so
%{_libdir}/wine/ngen.exe.so
%{_libdir}/wine/ntoskrnl.exe.so
%{_libdir}/wine/oleview.exe.so
%{_libdir}/wine/ping.exe.so
%{_libdir}/wine/reg.exe.so
%{_libdir}/wine/regasm.exe.so
%{_libdir}/wine/regedit.exe.so
%{_libdir}/wine/regsvcs.exe.so
%{_libdir}/wine/regsvr32.exe.so
%{_libdir}/wine/rpcss.exe.so
%{_libdir}/wine/rundll32.exe.so
%{_libdir}/wine/secedit.exe.so
%{_libdir}/wine/servicemodelreg.exe.so
%{_libdir}/wine/services.exe.so
%{_libdir}/wine/start.exe.so
%{_libdir}/wine/termsv.exe.so
%{_libdir}/wine/view.exe.so
%{_libdir}/wine/winebrowser.exe.so
%{_libdir}/wine/wineconsole.exe.so
%{_libdir}/wine/winemenubuilder.exe.so
%{_libdir}/wine/winecfg.exe.so
%{_libdir}/wine/winedevice.exe.so
%{_libdir}/wine/wscript.exe.so
%{_libdir}/wine/uninstaller.exe.so
%{_libdir}/libwine.so.1*
%{_libdir}/wine/acledit.dll.so
%{_libdir}/wine/aclui.dll.so
%{_libdir}/wine/activeds.dll.so
%{_libdir}/wine/actxprxy.dll.so
%{_libdir}/wine/advapi32.dll.so
%{_libdir}/wine/advpack.dll.so
%{_libdir}/wine/amstream.dll.so
%{_libdir}/wine/apphelp.dll.so
%{_libdir}/wine/appwiz.cpl.so
%{_libdir}/wine/atl.dll.so
%{_libdir}/wine/authz.dll.so
%{_libdir}/wine/avicap32.dll.so
%{_libdir}/wine/avifil32.dll.so
%{_libdir}/wine/avrt.dll.so
%{_libdir}/wine/bcrypt.dll.so
%{_libdir}/wine/browseui.dll.so
%{_libdir}/wine/cabinet.dll.so
%{_libdir}/wine/cards.dll.so
%{_libdir}/wine/cfgmgr32.dll.so
%{_libdir}/wine/clock.exe.so
%{_libdir}/wine/clusapi.dll.so
%{_libdir}/wine/comcat.dll.so
%{_libdir}/wine/comctl32.dll.so
%{_libdir}/wine/comdlg32.dll.so
%{_libdir}/wine/compstui.dll.so
%{_libdir}/wine/credui.dll.so
%{_libdir}/wine/crtdll.dll.so
%{_libdir}/wine/crypt32.dll.so
%{_libdir}/wine/cryptdlg.dll.so
%{_libdir}/wine/cryptdll.dll.so
%{_libdir}/wine/cryptnet.dll.so
%{_libdir}/wine/cryptui.dll.so
%{_libdir}/wine/ctapi32.dll.so
%{_libdir}/wine/ctl3d32.dll.so
%{_libdir}/wine/d3d10.dll.so
%{_libdir}/wine/d3d10core.dll.so
%{_libdir}/wine/d3dcompiler_*.dll.so
%{_libdir}/wine/d3dim.dll.so
%{_libdir}/wine/d3drm.dll.so
%{_libdir}/wine/d3dx9_*.dll.so
%{_libdir}/wine/d3dx10_*.dll.so
%{_libdir}/wine/d3dxof.dll.so
%{_libdir}/wine/dbgeng.dll.so
%{_libdir}/wine/dbghelp.dll.so
%{_libdir}/wine/dciman32.dll.so
%{_libdir}/wine/ddraw.dll.so
%{_libdir}/wine/ddrawex.dll.so
%{_libdir}/wine/devenum.dll.so
%{_libdir}/wine/dhcpcsvc.dll.so
%{_libdir}/wine/dinput.dll.so
%{_libdir}/wine/dinput8.dll.so
%{_libdir}/wine/dispex.dll.so
%{_libdir}/wine/dmband.dll.so
%{_libdir}/wine/dmcompos.dll.so
%{_libdir}/wine/dmime.dll.so
%{_libdir}/wine/dmloader.dll.so
%{_libdir}/wine/dmscript.dll.so
%{_libdir}/wine/dmstyle.dll.so
%{_libdir}/wine/dmsynth.dll.so
%{_libdir}/wine/dmusic.dll.so
%{_libdir}/wine/dmusic32.dll.so
%{_libdir}/wine/dplay.dll.so
%{_libdir}/wine/dplayx.dll.so
%{_libdir}/wine/dpnaddr.dll.so
%{_libdir}/wine/dpnet.dll.so
%{_libdir}/wine/dpnhpast.dll.so
%{_libdir}/wine/dpnlobby.dll.so
%{_libdir}/wine/dpwsockx.dll.so
%{_libdir}/wine/drmclien.dll.so
%{_libdir}/wine/dsound.dll.so
%{_libdir}/wine/dssenh.dll.so
%{_libdir}/wine/dswave.dll.so
%{_libdir}/wine/dwmapi.dll.so
%{_libdir}/wine/dxdiagn.dll.so
%{_libdir}/wine/dxgi.dll.so
%{_libdir}/wine/eject.exe.so
%{_libdir}/wine/explorerframe.dll.so
%{_libdir}/wine/faultrep.dll.so
%{_libdir}/wine/fltlib.dll.so
%{_libdir}/wine/fusion.dll.so
%{_libdir}/wine/fwpuclnt.dll.so
%{_libdir}/wine/gameux.dll.so
%{_libdir}/wine/gdi32.dll.so
%{_libdir}/wine/gdiplus.dll.so
%{_libdir}/wine/glu32.dll.so
%{_libdir}/wine/gphoto2.ds.so
%{_libdir}/wine/gpkcsp.dll.so
%{_libdir}/wine/hal.dll.so
%{_libdir}/wine/hh.exe.so
%{_libdir}/wine/hhctrl.ocx.so
%{_libdir}/wine/hid.dll.so
%{_libdir}/wine/hlink.dll.so
%{_libdir}/wine/hnetcfg.dll.so
%{_libdir}/wine/httpapi.dll.so
%{_libdir}/wine/iccvid.dll.so
%{_libdir}/wine/icinfo.exe.so
%{_libdir}/wine/icmp.dll.so
%{_libdir}/wine/ieframe.dll.so
%{_libdir}/wine/imaadp32.acm.so
%{_libdir}/wine/imagehlp.dll.so
%{_libdir}/wine/imm32.dll.so
%{_libdir}/wine/inetcomm.dll.so
%{_libdir}/wine/inetcpl.cpl.so
%{_libdir}/wine/inetmib1.dll.so
%{_libdir}/wine/infosoft.dll.so
%{_libdir}/wine/initpki.dll.so
%{_libdir}/wine/inkobj.dll.so
%{_libdir}/wine/inseng.dll.so
%{_libdir}/wine/iphlpapi.dll.so
%{_libdir}/wine/itircl.dll.so
%{_libdir}/wine/itss.dll.so
%{_libdir}/wine/jscript.dll.so
%{_libdir}/wine/kernel32.dll.so
%{_libdir}/wine/ktmw32.dll.so
%{_libdir}/wine/loadperf.dll.so
%{_libdir}/wine/localspl.dll.so
%{_libdir}/wine/localui.dll.so
%{_libdir}/wine/lodctr.exe.so
%{_libdir}/wine/lz32.dll.so
%{_libdir}/wine/mapi32.dll.so
%{_libdir}/wine/mapistub.dll.so
%{_libdir}/wine/mciavi32.dll.so
%{_libdir}/wine/mcicda.dll.so
%{_libdir}/wine/mciseq.dll.so
%{_libdir}/wine/mciwave.dll.so
%{_libdir}/wine/mgmtapi.dll.so
%{_libdir}/wine/midimap.dll.so
%{_libdir}/wine/mlang.dll.so
%{_libdir}/wine/mmcndmgr.dll.so
%{_libdir}/wine/mmdevapi.dll.so
%{_libdir}/wine/mofcomp.exe.so
%{_libdir}/wine/mountmgr.sys.so
%{_libdir}/wine/mpr.dll.so
%{_libdir}/wine/mprapi.dll.so
%{_libdir}/wine/mciqtz32.dll.so
%{_libdir}/wine/msacm32.dll.so
%{_libdir}/wine/msacm32.drv.so
%{_libdir}/wine/msadp32.acm.so
%{_libdir}/wine/mscat32.dll.so
%{_libdir}/wine/mscoree.dll.so
%{_libdir}/wine/msctf.dll.so
%{_libdir}/wine/msdaps.dll.so
%{_libdir}/wine/msdmo.dll.so
%{_libdir}/wine/msftedit.dll.so
%{_libdir}/wine/msg711.acm.so
%{_libdir}/wine/msgsm32.acm.so
%{_libdir}/wine/mshtml.dll.so
%{_libdir}/wine/mshtml.tlb.so
%{_libdir}/wine/msi.dll.so
%{_libdir}/wine/msident.dll.so
%{_libdir}/wine/msimtf.dll.so
%{_libdir}/wine/msimg32.dll.so
%{_libdir}/wine/msimsg.dll.so
%{_libdir}/wine/msisip.dll.so
%{_libdir}/wine/msisys.ocx.so
%{_libdir}/wine/msnet32.dll.so
%{_libdir}/wine/mspatcha.dll.so
%{_libdir}/wine/mssign32.dll.so
%{_libdir}/wine/mssip32.dll.so
%{_libdir}/wine/msrle32.dll.so
%{_libdir}/wine/mstask.dll.so
%{_libdir}/wine/msvcirt.dll.so
%{_libdir}/wine/msvcp60.dll.so
%{_libdir}/wine/msvcp70.dll.so
%{_libdir}/wine/msvcp71.dll.so
%{_libdir}/wine/msvcp80.dll.so
%{_libdir}/wine/msvcp90.dll.so
%{_libdir}/wine/msvcp100.dll.so
%{_libdir}/wine/msvcr70.dll.so
%{_libdir}/wine/msvcr71.dll.so
%{_libdir}/wine/msvcr80.dll.so
%{_libdir}/wine/msvcr90.dll.so
%{_libdir}/wine/msvcr100.dll.so
%{_libdir}/wine/msvcrt.dll.so
%{_libdir}/wine/msvcrt20.dll.so
%{_libdir}/wine/msvcrt40.dll.so
%{_libdir}/wine/msvcrtd.dll.so
%{_libdir}/wine/msvfw32.dll.so
%{_libdir}/wine/msvidc32.dll.so
%{_libdir}/wine/mswsock.dll.so
%{_libdir}/wine/msxml.dll.so
%{_libdir}/wine/msxml2.dll.so
%{_libdir}/wine/msxml3.dll.so
%{_libdir}/wine/msxml4.dll.so
%{_libdir}/wine/msxml6.dll.so
%{_libdir}/wine/nddeapi.dll.so
%{_libdir}/wine/netapi32.dll.so
%{_libdir}/wine/netsh.exe.so
%{_libdir}/wine/newdev.dll.so
%{_libdir}/wine/normaliz.dll.so
%{_libdir}/wine/npmshtml.dll.so
%{_libdir}/wine/ntdll.dll.so
%{_libdir}/wine/ntdsapi.dll.so
%{_libdir}/wine/ntprint.dll.so
%{_libdir}/wine/objsel.dll.so
%{_libdir}/wine/odbc32.dll.so
%{_libdir}/wine/odbccp32.dll.so
%{_libdir}/wine/ole32.dll.so
%{_libdir}/wine/oleacc.dll.so
%{_libdir}/wine/oleaut32.dll.so
%{_libdir}/wine/olecli32.dll.so
%{_libdir}/wine/oledb32.dll.so
%{_libdir}/wine/oledlg.dll.so
%{_libdir}/wine/olepro32.dll.so
%{_libdir}/wine/olesvr32.dll.so
%{_libdir}/wine/olethk32.dll.so
%{_libdir}/wine/pdh.dll.so
%{_libdir}/wine/photometadatahandler.dll.so
%{_libdir}/wine/pidgen.dll.so
%{_libdir}/wine/powrprof.dll.so
%{_libdir}/wine/presentationfontcache.exe.so
%{_libdir}/wine/printui.dll.so
%{_libdir}/wine/propsys.dll.so
%{_libdir}/wine/psapi.dll.so
%{_libdir}/wine/pstorec.dll.so
%{_libdir}/wine/qcap.dll.so
%{_libdir}/wine/qedit.dll.so
%{_libdir}/wine/qmgr.dll.so
%{_libdir}/wine/qmgrprxy.dll.so
%{_libdir}/wine/quartz.dll.so
%{_libdir}/wine/query.dll.so
%{_libdir}/wine/rasapi32.dll.so
%{_libdir}/wine/rasdlg.dll.so
%{_libdir}/wine/regapi.dll.so
%{_libdir}/wine/resutils.dll.so
%{_libdir}/wine/riched20.dll.so
%{_libdir}/wine/riched32.dll.so
%{_libdir}/wine/rpcrt4.dll.so
%{_libdir}/wine/rsabase.dll.so
%{_libdir}/wine/rsaenh.dll.so
%{_libdir}/wine/rstrtmgr.dll.so
%{_libdir}/wine/rtutils.dll.so
%{_libdir}/wine/samlib.dll.so
%{_libdir}/wine/sc.exe.so
%{_libdir}/wine/scarddlg.dll.so
%{_libdir}/wine/sccbase.dll.so
%{_libdir}/wine/scrrun.dll.so
%{_libdir}/wine/schannel.dll.so
%{_libdir}/wine/secur32.dll.so
%{_libdir}/wine/sensapi.dll.so
%{_libdir}/wine/serialui.dll.so
%{_libdir}/wine/setupapi.dll.so
%{_libdir}/wine/sfc_os.dll.so
%{_libdir}/wine/shdoclc.dll.so
%{_libdir}/wine/shdocvw.dll.so
%{_libdir}/wine/shell32.dll.so
%{_libdir}/wine/shfolder.dll.so
%{_libdir}/wine/shlwapi.dll.so
%{_libdir}/wine/slbcsp.dll.so
%{_libdir}/wine/slc.dll.so
%{_libdir}/wine/snmpapi.dll.so
%{_libdir}/wine/softpub.dll.so
%{_libdir}/wine/spoolsv.exe.so
%{_libdir}/wine/stdole2.tlb.so
%{_libdir}/wine/stdole32.tlb.so
%{_libdir}/wine/sti.dll.so
%{_libdir}/wine/svchost.exe.so
%{_libdir}/wine/svrapi.dll.so
%{_libdir}/wine/sxs.dll.so
%{_libdir}/wine/t2embed.dll.so
%{_libdir}/wine/tapi32.dll.so
%{_libdir}/wine/taskkill.exe.so
%{_libdir}/wine/traffic.dll.so
%{_libdir}/wine/unicows.dll.so
%{_libdir}/wine/unlodctr.exe.so
%{_libdir}/wine/updspapi.dll.so
%{_libdir}/wine/url.dll.so
%{_libdir}/wine/urlmon.dll.so
%{_libdir}/wine/usbd.sys.so
%{_libdir}/wine/user32.dll.so
%{_libdir}/wine/usp10.dll.so
%{_libdir}/wine/uxtheme.dll.so
%{_libdir}/wine/userenv.dll.so
%{_libdir}/wine/vbscript.dll.so
%{_libdir}/wine/vcomp.dll.so
%{_libdir}/wine/vdmdbg.dll.so
%{_libdir}/wine/version.dll.so
%{_libdir}/wine/wbemprox.dll.so
%{_libdir}/wine/wer.dll.so
%{_libdir}/wine/wevtapi.dll.so
%{_libdir}/wine/wiaservc.dll.so
%{_libdir}/wine/windowscodecs.dll.so
%{_libdir}/wine/winegstreamer.dll.so
%{_libdir}/wine/winejoystick.drv.so
%{_libdir}/wine/winemapi.dll.so
%{_libdir}/wine/winex11.drv.so
%{_libdir}/wine/wing32.dll.so
%{_libdir}/wine/winhttp.dll.so
%{_libdir}/wine/wininet.dll.so
%{_libdir}/wine/winmm.dll.so
%{_libdir}/wine/winnls32.dll.so
%{_libdir}/wine/winspool.drv.so
%{_libdir}/wine/winsta.dll.so
%{_libdir}/wine/wmi.dll.so
%{_libdir}/wine/wmic.exe.so
%{_libdir}/wine/wmiutils.dll.so
%{_libdir}/wine/spoolss.dll.so
%{_libdir}/wine/winscard.dll.so
%{_libdir}/wine/wintab32.dll.so
%{_libdir}/wine/wintrust.dll.so
%{_libdir}/wine/wlanapi.dll.so
%{_libdir}/wine/wnaspi32.dll.so
%{_libdir}/wine/ws2_32.dll.so
%{_libdir}/wine/wshom.ocx.so
%{_libdir}/wine/wsock32.dll.so
%{_libdir}/wine/wtsapi32.dll.so
%{_libdir}/wine/wuapi.dll.so
%{_libdir}/wine/wuaueng.dll.so
%{_libdir}/wine/security.dll.so
%{_libdir}/wine/sfc.dll.so
%{_libdir}/wine/wineps.drv.so
%{_libdir}/wine/d3d8.dll.so
%{_libdir}/wine/d3d9.dll.so
%{_libdir}/wine/opengl32.dll.so
%{_libdir}/wine/wined3d.dll.so
%{_libdir}/wine/dnsapi.dll.so
%{_libdir}/wine/iexplore.exe.so
%{_libdir}/wine/xapofx1_1.dll.so
%{_libdir}/wine/xcopy.exe.so
%{_libdir}/wine/xinput1_1.dll.so
%{_libdir}/wine/xinput1_2.dll.so
%{_libdir}/wine/xinput1_3.dll.so
%{_libdir}/wine/xinput9_1_0.dll.so
%{_libdir}/wine/xmllite.dll.so
%{_libdir}/wine/xolehlp.dll.so
%{_libdir}/wine/xpsprint.dll.so

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm}
%{_libdir}/wine/winevdm.exe.so
%{_libdir}/wine/ifsmgr.vxd.so
%{_libdir}/wine/mmdevldr.vxd.so
%{_libdir}/wine/monodebg.vxd.so
%{_libdir}/wine/rundll.exe16.so
%{_libdir}/wine/vdhcp.vxd.so
%{_libdir}/wine/user.exe16.so
%{_libdir}/wine/vmm.vxd.so
%{_libdir}/wine/vnbt.vxd.so
%{_libdir}/wine/vnetbios.vxd.so
%{_libdir}/wine/vtdapi.vxd.so
%{_libdir}/wine/vwin32.vxd.so
%{_libdir}/wine/w32skrnl.dll.so
%{_libdir}/wine/avifile.dll16.so
%{_libdir}/wine/comm.drv16.so
%{_libdir}/wine/commdlg.dll16.so
%{_libdir}/wine/compobj.dll16.so
%{_libdir}/wine/ctl3d.dll16.so
%{_libdir}/wine/ctl3dv2.dll16.so
%{_libdir}/wine/ddeml.dll16.so
%{_libdir}/wine/dispdib.dll16.so
%{_libdir}/wine/display.drv16.so
%{_libdir}/wine/gdi.exe16.so
%{_libdir}/wine/imm.dll16.so
%{_libdir}/wine/krnl386.exe16.so
%{_libdir}/wine/keyboard.drv16.so
%{_libdir}/wine/lzexpand.dll16.so
%{_libdir}/wine/mmsystem.dll16.so
%{_libdir}/wine/mouse.drv16.so
%{_libdir}/wine/msacm.dll16.so
%{_libdir}/wine/msvideo.dll16.so
%{_libdir}/wine/ole2.dll16.so
%{_libdir}/wine/ole2conv.dll16.so
%{_libdir}/wine/ole2disp.dll16.so
%{_libdir}/wine/ole2nls.dll16.so
%{_libdir}/wine/ole2prox.dll16.so
%{_libdir}/wine/ole2thk.dll16.so
%{_libdir}/wine/olecli.dll16.so
%{_libdir}/wine/olesvr.dll16.so
%{_libdir}/wine/rasapi16.dll16.so
%{_libdir}/wine/setupx.dll16.so
%{_libdir}/wine/shell.dll16.so
%{_libdir}/wine/sound.drv16.so
%{_libdir}/wine/storage.dll16.so
%{_libdir}/wine/stress.dll16.so
%{_libdir}/wine/system.drv16.so
%{_libdir}/wine/toolhelp.dll16.so
%{_libdir}/wine/twain.dll16.so
%{_libdir}/wine/typelib.dll16.so
%{_libdir}/wine/ver.dll16.so
%{_libdir}/wine/w32sys.dll16.so
%{_libdir}/wine/win32s16.dll16.so
%{_libdir}/wine/win87em.dll16.so
%{_libdir}/wine/winaspi.dll16.so
%{_libdir}/wine/windebug.dll16.so
%{_libdir}/wine/wineps16.drv16.so
%{_libdir}/wine/wing.dll16.so
%{_libdir}/wine/winhelp.exe16.so
%{_libdir}/wine/winnls.dll16.so
%{_libdir}/wine/winoldap.mod16.so
%{_libdir}/wine/winsock.dll16.so
%{_libdir}/wine/wintab.dll16.so
%{_libdir}/wine/wow32.dll.so
%endif

%files common
%defattr(-,root,root,-)
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*
%{_datadir}/wine/generic.ppd
%{_datadir}/wine/wine.inf
%{_datadir}/wine/l_intl.nls

%files fonts
%defattr(-,root,root,-)
%dir %{_datadir}/wine/fonts

%files courier-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-courier-fonts

%files system-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-system-fonts

%files small-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-small-fonts

%files marlett-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-marlett-fonts

%files ms-sans-serif-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-ms-sans-serif-fonts

%files tahoma-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%files symbol-fonts
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_datadir}/fonts/wine-symbol-fonts

%files desktop
%defattr(-,root,root,-)
%{_datadir}/applications/fedora-wine-notepad.desktop
%{_datadir}/applications/fedora-wine-winefile.desktop
%{_datadir}/applications/fedora-wine-winemine.desktop
%{_datadir}/applications/fedora-wine-mime-msi.desktop
%{_datadir}/applications/fedora-wine.desktop
%{_datadir}/applications/fedora-wine-regedit.desktop
%{_datadir}/applications/fedora-wine-uninstaller.desktop
%{_datadir}/applications/fedora-wine-winecfg.desktop
%{_datadir}/applications/fedora-wine-wineboot.desktop
%{_datadir}/applications/fedora-wine-winhelp.desktop
%{_datadir}/applications/fedora-wine-wordpad.desktop
%{_datadir}/applications/fedora-wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%if 0%{?fedora} >= 10
%{_datadir}/icons/hicolor/scalable/apps/*svg
%endif

%if 0%{?fedora} >= 15
%files systemd
%defattr(0644,root,root)
%config %{_sysconfdir}/binfmt.d/wine.conf

%files sysvinit
%defattr(0755,root,root)
%endif
%{_initrddir}/wine

# ldap subpackage
%files ldap
%defattr(-,root,root,-)
%{_libdir}/wine/wldap32.dll.so

# cms subpackage
%files cms
%defattr(-,root,root,-)
%{_libdir}/wine/mscms.dll.so

# twain subpackage
%files twain
%defattr(-,root,root,-)
%{_libdir}/wine/twain_32.dll.so
%{_libdir}/wine/sane.ds.so

# capi subpackage
%files capi
%defattr(-,root,root,-)
%{_libdir}/wine/capi2032.dll.so

%files devel
%defattr(-,root,root,-)
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%{_libdir}/*.so
%{_libdir}/wine/*.a
%{_libdir}/wine/*.def

%files pulseaudio
%defattr(-,root,root,-)
# empty meta package for deps

%files alsa
%defattr(-,root,root,-)
%{_libdir}/wine/winealsa.drv.so

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%files openal
%defattr(-,root,root,-)
%{_libdir}/wine/openal32.dll.so
%endif

%changelog
* Fri Mar 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.5-1
- Upgrade to version 1.5

* Wed Mar 07 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-1
- version upgrade

* Tue Mar 06 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.8.rc6
- version upgrade

* Sat Feb 25 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.7.rc5
- version upgrade

* Tue Feb 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.6.rc4
- fix dependency issue (#795295)

* Sun Feb 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.5.rc4
- version upgrade

* Fri Feb 17 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.4.rc3
- version upgrade
- cleanup arm dependency fixes

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-0.3.rc2
- Fix architecture dependencies on ARM so it installs

* Thu Feb 02 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.2.rc2
- version upgrade

* Sat Jan 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.1.rc1
- version upgrade

* Wed Jan 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.37-2
- Add initial support for wine on ARM

* Fri Jan 13 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.37-1
- version upgrade
- drop obsoleted patches

* Sat Dec 31 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.36-1
- version upgrade

* Mon Dec 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.35-1
- version upgrade

* Thu Dec 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.34-1
- version upgrade

* Sun Nov 20 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.33-1
- version upgrade(rhbz#755192)

* Sat Nov 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.32-1
- version upgrade (rhbz#745434)

* Fri Nov 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-2
- pull in correct wine-alsa arch in the pa meta package (rhbz#737431)

* Sun Oct 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-1
- version upgrade

* Mon Oct 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.30-1
- version upgrade

* Sat Sep 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.29-1
- version upgrade

* Sun Sep 11 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.28-1
- version upgrade
- require -alsa from -pulseaudio package for new sound api

* Mon Aug 29 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.27-1
- version upgrade
- fix epel build (rhbz#733802)

* Tue Aug 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-3
- drop pulse configure option
- fix f16 build (dbus/hal configure options)

* Mon Aug 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-2
- drop pulse patches
- make pulseaudio package meta and require alsa pa plugin
- update udisks patch

* Sun Aug 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-1
- version upgrade

* Fri Jul 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.25-1
- version upgrade
- remove -jack and -esd (retired upstream)
- rebase to Maarten Lankhorst's winepulse
- drop obsolete winepulse readme
- add udisks support from pending patches (winehq#21713, rhbz#712755)
- disable xinput2 (broken)

* Sun Jul 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.24-1
- version upgrade
- add sign as source10
- drop mshtml patch (upstream)

* Sun Jun 26 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.23-1
- version upgrade
- winepulse upgrade (0.40)
- fix gcc optimization problem (rhbz#710352, winehq#27375)

* Tue Jun 21 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-2
- workaround gcc optimization problem (rhbz#710352)

* Sun Jun 12 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-1
- version upgrade

* Sat May 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.21-1
- version upgrade

* Sun May 15 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.20-1
- version upgrade

* Sat Apr 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.19-1
- version upgrade (#701003)
- remove wine-oss
- disable hal (>=f16)

* Sat Apr 16 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.18-1
- version upgrade

* Thu Apr 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-3
- add fix for office installation (upstream #26650)

* Tue Apr 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-2
- cleanup spec file
- remove rpath via chrpath
- convert README files to utf8
- move SysV init script so sysvinit subpackage (>=f15)
- add some missing lsb keywords to init file
- create systemd subpackage and require it in the wine-desktop package (>=f15)
- disable embedded bitmaps in tahoma (#693180)
- provide readme how to disable wine-tahoma in fontconfig (#693180)

* Sat Apr 02 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-1
- version upgrade

* Fri Mar 18 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.16-1
- version upgrade
- cleanup unneeded patches
- drop some patches
- reenable smp build

* Thu Mar 17 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-3
- reenable fonts

* Sun Mar 13 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-2
- use svg files for icons (#684277)

* Tue Mar 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-1
- version upgrade

* Tue Mar 01 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-2
- prepare for wine-gecko

* Sat Feb 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-1
- version upgrade

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.13-1
- version upgrade
- update desktop files

* Mon Jan 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.12-1
- version upgrade

* Sun Jan 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.11-1
- version upgrade

* Tue Dec 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.10-1
- version upgrade

* Sat Dec 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.9-1
- version upgrade

* Sat Nov 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.8-1
- version upgrade
- require libXcursor (#655255)
- require wine-openal in wine meta package (#657144)

* Tue Nov 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-2
- cleanup cflags a bit

* Sat Nov 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-1
- version upgrade
- fix package description (#652718)
- compile with D_FORTIFY_SOURCE=0 for now to avoid breaking wine (#650875)

* Fri Oct 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.6-1
- version upgrade
- rebase winepulse configure patch
- add gstreamer BR for new gstreamer support
- add libtiff BR for new tiff support

* Mon Oct 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-1
- version upgrade

* Sun Oct 03 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-1
- version upgrade

* Wed Sep 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-2
- winepulse upgrade (0.39)

* Mon Sep 20 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-1
- version upgrade

* Wed Sep 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.2-1
- version upgrade

* Sat Aug 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.1-1
- version ugprade

* Sat Jul 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.0-1
- version upgrade

* Wed Jul 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-2
- fix segfault (#617968)
- enable openal-soft on el6

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-1
- final release

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.8.rc7
- improve font patch

* Sun Jul 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.7.rc7
- version upgrade
- make sure font packages include the license file in case they are installed
  standalone

* Sun Jul 04 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.6.rc6
- version upgrade
- use new winelogo from user32
- winepulse upgrade

* Sun Jun 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.5.rc5
- version upgrade
- require liberation-narrow-fonts

* Fri Jun 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.4.rc4
- version upgrade
- fixes winecfg on 64bit (#541986)
- require wine-common from -core to ensure man pages and wine.inf are present
  (#528335)

* Sun Jun 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.3.rc3
- version upgrade

* Mon May 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.2.rc2
- version upgrade

* Mon May 24 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.1.rc1
- upgrade to rc1
- add BR for ImageMagick and icoutils
- spec cleanup
- install available icon files (#594950)
- desktop package requires wine x86-32 because of wine/wine64 rename
- put system/small fonts in right place

* Wed May 19 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-5
- fix font issues

* Thu May 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-4
- fix install of 32bit only wine on x86_64 via install wine.i686

* Wed May 12 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-3
- move wine symlink to -wow for 32bit (#591690)

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-2
- fix manpage conflict between -common and -devel

* Sun May 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-1
- version upgrade (#580024)

* Sun Apr 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.43-1
- version upgrade

* Sun Apr 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.42-1
- version upgrade
- rework for wow64

* Mon Mar 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-3
- add support for mingw32-wine-gecko

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-2
- convert to font package guidelines
- add libv4l-devel BR

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-1
- version upgrade (#577587, #576607)
- winepulse upgrade (0.36)

* Sat Mar 06 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.40-1
- version upgrade

* Sun Feb 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.39-1
- version upgrade

* Tue Feb 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.38-1
- version upgrade
- winepulse upgrade (0.35)

* Mon Jan 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.36-1
- version upgrade (#554102)
- require -common in -desktop (#549190)

* Sat Dec 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.35-1
- version upgrade

* Fri Dec 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.34-1
- version upgrade (#546749)

* Mon Nov 16 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.33-1
- version upgrade
- winepulse update (.33)
- require gnutls (#538694)
- use separate WINEPREFIX on x86_64 per default (workaround for #533806)
- drop explicit xmessage require (#537610)

* Tue Oct 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.32-1
- version upgrade (#531358)
- update winepulse

* Mon Sep 28 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.30-1
- version upgrade
- openal support
- drop steam regression patch

* Sun Sep 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-3
- patch for steam regression (upstream #19916)
- update winepulse winecfg patch

* Thu Sep 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-2
- rebuild for new gcc (#505862)

* Wed Sep 02 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-1
- version upgrade

* Mon Aug 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.28-1
- version upgrade
- make 32bit and 64bit version parallel installable

* Sun Aug 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.27-1
- version upgrade
- WinePulse 0.30

* Thu Aug 06 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-2
- build 32bit wine on x86_64 and prepare for 64bit parallel build (#487651)
- fix subpackage problems (#485410,#508766,#508944,#514967)
- fix nss dependencies on x86_64 (#508412)

* Sat Jul 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-1
- version upgrade
- WinePulse 0.29
- require Xrender isa for x86_64 (#510947)

* Thu Jul 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.25-1
- version upgrade (#509648)

* Mon Jun 29 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-3
- pull in nss correctly on x86_64

* Sun Jun 21 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-2
- adjust wine-menu to follow wine behavior (wine-wine instead of Wine)
  (fixes #479649, #495953)
- fix wine help desktop entry (#495953, #507154)
- add some more wine application desktop entries (#495953)
- split alsa/oss support into wine-alsa/wine-oss
- drop nas require from wine meta package
- fix dns resolution (#492700)

* Fri Jun 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-1
- version upgrade
- WinePulse 0.28
- drop meta package requires for jack and esd (#492983)

* Wed Jun 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.23-1
- version upgrade (#491321)
- rediff pulseaudio patch (Michael Cronenworth)

* Wed May 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-2
- fix uninstaller (#500479)

* Tue May 12 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-1
- version upgrade

* Mon Apr 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.20-1
- version upgrade

* Mon Mar 30 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.18-1
- version upgrade (#490672, #491321)
- winepulse update

* Sun Mar 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net> - 1.1.15-3
— Make sure F11 font packages have been built with F11 fontforge

* Tue Feb 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-2
- switch from i386 to ix86

* Sun Feb 15 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-1
- version upgrade
- new pulse patches

* Sat Jan 31 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.14-1
- version upgrade

* Sat Jan 17 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.13-1
- version upgrade
- fix gcc compile problems (#440139, #461720)

* Mon Jan 05 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.12-1
- version upgrade

* Sat Dec 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.10-1
- version upgrade
- add native pulseaudio driver from winehq bugzilla (#10495)
  fixes #474435, #344281

* Mon Nov 24 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-2
- fix #469907

* Sun Nov 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-1
- version upgrade

* Sun Oct 26 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.7-1
- version upgrade

* Thu Oct 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.6-1
- version upgrade
- fix multiarch problems (#466892,#467480)

* Sat Sep 20 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.5-1
- version upgrade

* Fri Sep 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.4-1
- version upgrade
- drop wine-prefixfonts.patch (#460745)

* Fri Aug 29 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.3-1
- version upgrade

* Sun Jul 27 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.2-1
- version upgrade (#455960, #456831)
- require freetype (#452417)
- disable wineprefixcreate patch for now

* Fri Jul 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.1-1
- version upgrade

* Tue Jun 17 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-1
- version upgrade (#446311,#417161)
- fix wine.desktop mime types (#448338)
- add desktop package including desktop files and binary handler (#441310)
- pull in some wine alsa/pulseaudio patches (#344281)

* Mon Jun 16 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.5.rc5
- version upgrade

* Fri Jun 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.4.rc4
- version upgrade

* Sun Jun 01 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.3.rc3
- version upgrade

* Fri May 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.2.rc2
- version upgrade
- add compile workaround for fedora 9/rawhide (#440139)

* Sat May 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.1.rc1
- version upgrade to rc1

* Mon May 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.61-1
- version upgrade

* Fri Apr 18 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.60-1
- version upgrade

* Sat Apr 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.59-1
- version upgrade

* Sat Mar 22 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.58-1
- version upgrade

* Tue Mar 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.57-1
- version upgrade

* Sat Feb 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.56-1
- version upgrade

* Sun Feb 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.55-1
- version upgrade

* Fri Jan 25 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.54-1
- version upgrade
- remove default pulseaudio workaround (#429420,#428745)
- improve pulseaudio readme

* Sun Jan 13 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-2
- add some missing BR

* Sat Jan 12 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-1
- version upgrade

* Sat Dec 29 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-2
- fix menu bug (#393641)

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-1
- version upgrade

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-3
- add -n Wine to pulseaudio workaround
- try to fix menu bug #393641

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-2
- add fix for #344281 pulseaudio workaround
- fix #253474: wine-jack should require jack-audio-connection-kit

* Sun Dec 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-1
- version upgrade

* Sat Dec 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.50-1
- version upgrade

* Tue Nov 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.49-1
- version upgrade

* Fri Oct 26 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.48-1
- version upgrade

* Sat Oct 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.47-1
- version upgrade

* Sun Oct 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.46-1
- version upgrade

* Sun Sep 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.45-1
- version upgrade

* Sat Aug 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.44-1
- version upgrade

* Sat Aug 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-2
- fix license
- fix #248999

* Sat Aug 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-1
- version upgrade
- fix init-script output (#252144)
- add lsb stuff (#247096)

* Sat Jul 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.42-1
- version upgrade

* Mon Jul 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.41-1
- version upgrade

* Tue Jul 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.40-1
- version upgrade

* Mon Jun 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-2
- fix desktop entries

* Sun Jun 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-1
- version upgrade
- convert to utf8 (#244046)
- fix mime entry (#243511)

* Wed Jun 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-3
- fix description

* Sun Jun 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-2
- allow full opt flags again
- set ExclusiveArch to i386 for koji to only build i386

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-1
- version upgrade (#242087)
- fix menu problem (#220723)
- fix BR
- clean up desktop file section

* Wed May 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.37-1
- version upgrade
- add BR for xcursor (#240648)
- add desktop entry for wineboot (#240683)
- add mime handler for msi files (#240682)
- minor cleanups

* Wed May 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-2
- fix BR (#238774)
- fix some typos

* Sat Apr 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-1
- version upgrade

* Mon Apr 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.35-1
- version upgrade (#234766)
- sources file comments (#235232)
- smpflags work again (mentioned by Marcin Zajączkowski)
- drop arts sound driver package, as it is no longer part of wine

* Sun Apr 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.34-1
- version upgrade

* Sat Mar 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.33-1
- version upgrade

* Sun Mar 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.32-1
- version upgrade

* Sat Feb 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.31-1
- version upgrade

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.30-1
- version upgrade

* Thu Jan 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.29-1
- version upgrade

* Mon Dec 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.27-1
- version upgrade (#220130)
- fix submenus (#216076)
- fix BR (#217338)

* Thu Nov 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.25-1
- version upgrade
- fix init script (#213230)
- fix twain subpackage content (#213396)
- create wine submenu (#205024)

* Sat Oct 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.24-1
- version upgrade

* Tue Oct 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.23-1
- version upgrade

* Sat Sep 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.22-1
- version upgrade

* Sun Sep 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.21-1
- version upgrade
- own datadir/wine (#206403)
- do not include huge changelogs (#204302)

* Mon Aug 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.20-1
- version upgrade

* Mon Aug 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.19-1
- version upgrade

* Thu Aug 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.18-1
- version upgrade

* Mon Jul 10 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.17-1
- version upgrade

* Thu Jun 29 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.16-1
- version upgrade
- rename wine to wine-core
- add meta package wine

* Fri Jun 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15-1
- version upgrade

* Tue May 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-1
- version upgrade

* Fri May 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-2
- enable dbus/hal support

* Mon May 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-1
- version upgrade

* Sat Apr 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.12-1
- fix rpath issues (#187429,#188905)
- version upgrade 

* Mon Apr 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.11-1
- version upgrade
- fix #187546

* Mon Mar 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-2
- bump for x86_64 tree inclusion \o/

* Thu Mar 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-1
- version upgrade
- drop ancient extra fonts

* Fri Mar 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.9-1
- version upgrade

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.8-1
- version upgrade

* Thu Feb 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-3
- fix up tarball

* Wed Feb 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-2
- fix up post/preun scriplets (#178954)

* Thu Feb 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-1
- version upgrade

* Thu Jan 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.6-1
- version upgrade
- drop wmf exploit patch (part of current version)

* Sun Jan 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-2
- fix for CVE-2005-4560

* Fri Jan 06 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-1
- version upgrade
- fix #177089 (winemine desktop entry should be in Game not in System)
- fix cflags for compile
- test new BR

* Wed Jan 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>     
0.9.4-5                                                                 
- fix #176834 

* Mon Jan 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-4
- add dist

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-3
- use ExclusiveArch instead of ExcludeArch

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-2
- own font directory
- fix devel summary
- add ExcludeArch x86_64 for now

* Sat Dec 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-1
- version upgrade
- changed wine.init perissions to 0644
- added autoconf BR

* Mon Dec 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.3-1
- version upgrade

* Thu Nov 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.2-1
- version upgrade

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de
0.9.1-3
- fix typo in winefile desktop file
- drop in ld config instead of editing ld.so.conf

* Sun Nov 13 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-2
- add fontforge BR and include generated fonts...

* Sat Nov 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-1
- version upgrade
- move uninstaller and winecfg into wine main package...
- drop wine suite

* Sat Oct 29 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-3
- s/libwine/wine/

* Thu Oct 27 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-2
- remerge some subpackages which should be defaults

* Tue Oct 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-1
- upgrade to new version
- start splitting

* Mon Oct 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0-1.20050930
- add fedora readme
- switch to new (old) versioning sheme

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-3
- add desktop files
- revisit summary and description
- consistant use of %%{buildroot}

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-2
- some more spec tuneups...

* Sat Oct 01 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-1
- version upgrade

* Sun Sep 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050925-1
- upgrade to current cvs

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050830-1
- version upgrade

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050524-2
- fedorarized version

* Mon May 30 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050524-1fc3
- Update to 20050524
- Remove pdf documentation build as it's no more included in the main archive
- Workaround for generic.ppd installation

* Tue Apr 19 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050419-1fc3
- Update to 20050419

* Thu Mar 10 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050310-1fc3
- Update to 20050310

* Sat Feb 12 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050211-1fc3
- Update to 20050211

* Tue Jan 11 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050111-1fc3
- Update to 20050111

* Wed Dec 1 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041201-1fc3
- Recompile for FC3
- Update to 20041201
- Small reorganization:
    - use the generic ICU static libs name;
    - no more wine group;
    - use Wine's generated stdole32.tlb file;
    - use Wine's generated fonts.

* Wed Oct 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041019-1fc2
- Update to 20041019

* Wed Sep 15 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040914-1fc2
- Update to 20040914

* Sat Aug 14 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040813-1fc2
- Update to 20040813

* Sat Jul 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040716-1fc2
- Update to 20040716

* Fri Jun 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc2
- Recompile for FC2
- Backport from current CVS some fixes to the preloader to prevent
  a segfault on startup
- Include a currently uncommitted patch from Alexandre Julliard regarding
  further issues with the preloader

* Sun Jun 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc1
- Update to 20040615
- Use of wineprefixcreate instead of old RedHat patches

* Wed May 5 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040505-1fc1
- Update to 20040505

* Fri Apr 9 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040408-1fc1
- Update to 20040408
- Change the handling of paths to DOS drives in the installation process

* Wed Mar 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040309-1fc1
- Update to 20040309
- Replaced winedefault.reg by wine.inf

* Wed Feb 18 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040213-1fc1
- Update to 20040213
- Moved Wine dlls back to %%{_libdir}/wine rather than %%{_libdir}/wine/wine

* Sun Jan 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040121-fc1
- Update to 20040121

* Sat Dec 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031212-fc1
- Update to 20031212

* Wed Nov 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031118-fc1
- Update to 20031118

* Thu Oct 16 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031016-1rh9
- Update to 20031016

* Tue Sep 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030911-1rh9
- Fix of include location
- Better separation of run-time and development files
- Update to 20030911

* Wed Aug 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030813-1rh9
- Update to 20030813

* Wed Jul 09 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030709-1rh9
- Update to 20030709

* Wed Jun 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030618-1rh9
- Change the default C drive to ~/.wine/c, copied from /usr/share/wine
  if non-existant (Thanks to Rudolf Kastl)
- Updated to 20030618

* Tue May 20 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1rh9
- Adapted for RH9

* Thu May 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1
- Add libraries definition files to devel package
- Update to 20030508

* Tue Apr 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030408-1
- Update to 20030408

* Tue Mar 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030318-1
- Update to 20030318

* Thu Mar 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-2
- Fix the symlinks in wine-c.

* Wed Feb 19 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-1
- Update to 20030129
- Various fixes in RPM build process

* Fri Jan 17 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030115-1
- Update to 20030115
- fix to build problem

* Thu Nov  7 2002 Vincent Béron <vberon@mecano.gme.usherb.ca> 20021031-1
- Update to 20021031
- Tweaks here and there

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 20020605-2
- fix docs (#72923)

* Wed Jul 10 2002 Karsten Hopp <karsten@redhat.de> 20020605-1
- update
- remove obsolete part of redhat patch
- redo destdir patch
- redo kde patch
- redo defaultversion patch
- fix 'my_perl unknown' error
- work around name conflict with textutils 'expand'

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020327-1
- Fix wineshelllink (#61761)
- Fix up initscript (#53625)
- Clean up spec file
- Default to emulating Windoze ME rather than 3.1, nobody uses 3.1
  applications anymore
- Auto-generate default config if none exists (#61920)

* Mon Mar 04 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020304-1
- Assign gid 66 (closest to 666 [Microsoft number] we can get for a
  system account ;) )
- Don't use glibc private functions (__libc_fork)
- Update

* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020226-1
- Fix bug #60250
- Update

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020221-1
- Update
- Don't try to launch winesetup in winelauncher, we aren't shipping it
  (#59621)

* Sun Jan 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020127-1
- Update
- Fix build in current environment

* Wed Aug 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010822-1
- Make sure the package can be cleanly uninstalled (#52007)
- Add build dependencies

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010726-1
- Fix -devel package group (#49989)
- remove internal CVS files
- chkconfig deletion should be in %%preun, not %%postun
- rename initscript ("Starting windows:" at startup does look off)

* Thu May 03 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010503-1
- Update
- generate HTML documentation rather than shipping plain docbook text
  (#38453)

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Update registry to mount "/" as drive "Z:", fixes winedbg (needs to be
  accessible from 'doze drives)
- Don't create KDE 1.x style desktop entries in wineshelllink
- Be more tolerant on failing stuff in %%post

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update

* Thu Feb 15 2001 Tim Powers <timp@redhat.com>
- fixed time.h build problems

* Wed Jan 31 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add a patch to handle .exe and .com file permissions the way we want them

* Thu Jan 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Restore wine's ability to use a global config file, it was removed
  in CVS for whatever reason
- Move libraries to %%{_libdir}/wine to prevent conflicts with libuser
  (Bug #24202)
- Move include files to /usr/include/wine to prevent it from messing with
  some autoconf scripts (some broken scripts assume they're running on windoze
  if /usr/include/windows.h exists...)

* Tue Dec 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix %%pre and %%postun scripts
- --enable-opengl, glibc 2.2 should be safe
- Update CVS

* Mon Nov 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update CVS
- Add a new (user) group wine that can write to the "C: drive"
  %%{_datadir}/wine-c
- Fix up winedbg installation (registry entries)
- Add "Program Files/Common Files" subdirectory to the "C: drive", it's
  referenced in the registry

* Wed Oct 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update

* Mon Aug 7 2000 Tim Powers <timp@redhat.com>
- rebuilt with new DGA

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- fix compilation with gcc 2.96

* Fri Jul 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move init script back
- new version
- move man pages to FHS locations

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move initscript
- new snapshot

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Start the initscript on startup

* Mon May  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- New version
- new feature: You can now launch wine by just running a windows .exe file
  (./some.exe or just click on it in kfm, gmc and the likes)
- some spec file modifications

* Sun Feb 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- newer version
- Improve the system.ini file - all multimedia stuff should work now.

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- enable and fix up the urlmon/wininet patch
- add: autoexec.bat, config.sys, windows/win.ini windows/system.ini
  windows/Profiles/Administrator
- allow i[456]86 arches
- add some system.ini configuration

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update current
- add urlmon and wininet patches from Corel (don't apply them for now though)
- create empty shell*dll and winsock*dll files (as mentioned in the HOWTO)

* Mon Jan 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current (lots of important fixes)
- Fix up the default wine.conf file (We really don't want it to look
  for CD-ROMs in /cdrom!)
- create a "root filesystem" with everything required to run wine without
  windows in %%{_datadir}/wine-c (drive c:)
- add RedHat file in /usr/doc/wine-%%{version} explaining the new directory
  layout
- wine-devel requires wine

* Tue Dec 14 1999 Preston Brown <pbrown@redhat.com>
- updated source for Powertools 6.2
- better files list

* Fri Jul 23 1999 Tim Powers <timp@redhat.com>
- updated source
- built for 6.1

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated package and spec file

* Mon Oct 26 1998 Preston Brown <pbrown@redhat.com>
- updated to 10/25/98 version.  There is really no point in keeping the
- older one, it is full of bugs and the newer one has fewer.
- commented out building of texinfo manual, it is horrendously broken.

* Mon Oct 12 1998 Michael Maher <mike@redhat.com>
- built package for 5.2
- pressured by QA, not updating.

* Fri May 22 1998 Cristian Gafton <gafton@redhat.com>
- repackaged for PowerTools
