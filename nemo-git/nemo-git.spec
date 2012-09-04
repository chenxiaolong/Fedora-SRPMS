# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Build with:
#   rpmbuild -bb nemo-git.spec --define "_git_date DATE" --define "_git_rev REV"

#define _git_date
#define _git_rev

# Based on Fedora 17's spec file for Nautilus

Name:		nemo
Version:	%{_git_date}
Release:	1.git%{_git_rev}%{?dist}
Summary:	File Manager for Cinnamon

Group:		User Interface/Desktops
License:	GPLv2+
URL:		https://github.com/linuxmint/nemo
Source0:	nemo-%{_git_date}-git%{_git_rev}.tar.xz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)

# The nemo binary links against the main .so file, rather than the versioned
# .so file, so rpm's soname dependency won't work.
Requires:	nemo-extensions = %{version}-%{release}

Requires:	gnome-icon-theme
Requires:	gsettings-desktop-schemas
Requires:	gvfs
Requires:	redhat-menus

%description
This package contains Linux Mint's fork of the Nautilus file manager.


%package extensions
Summary:	Nemo extensions library
License:	LGPLv2+
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description extensions
This package provides the libraries used by Nemo extensions.


%package devel
Summary:	Support for developing Nemo extensions
License:	LGPLv2+
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description devel
This package provides libraries and header files for developing Nemo
extensions.


%prep
%setup -q -n nemo-%{_git_date}

autoreconf -vfi


%build
%configure --disable-update-mimedb

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang nemo


%post
/sbin/ldconfig
update-mime-database %{_datadir}/mime/ &>/dev/null || :

%postun
/sbin/ldconfig
update-mime-database %{_datadir}/mime/ &>/dev/null || :

if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolors/ &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :


%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig


%files -f nemo.lang
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS TODO
%{_bindir}/nemo
%{_bindir}/nemo-autorun-software
%{_bindir}/nemo-connect-server
%{_sysconfdir}/xdg/autostart/nemo-autostart.desktop
%dir %{_libdir}/nemo/
%dir %{_libdir}/nemo/extensions-3.0/
%{_libdir}/nemo/extensions-3.0/libnemo-sendto.so
%{_libexecdir}/nemo-convert-metadata
%{_datadir}/GConf/gsettings/nemo.convert
%{_datadir}/applications/nemo-autorun-software.desktop
%{_datadir}/applications/nemo.desktop
%{_datadir}/dbus-1/services/org.Nemo.service
%{_datadir}/dbus-1/services/org.freedesktop.NemoFileManager1.service
%{_datadir}/glib-2.0/schemas/org.nemo.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*png
%{_datadir}/icons/hicolor/scalable/apps/nemo.svg
%{_datadir}/mime/packages/nemo.xml
%dir %{_datadir}/nemo/
%{_datadir}/nemo/icons/
%{_datadir}/nemo/nemo-extras.placeholder
%{_datadir}/nemo/nemo-suggested.placeholder
%{_mandir}/man1/nemo-connect-server.1.gz
%{_mandir}/man1/nemo.1.gz


%files extensions
%{_libdir}/libnemo-extension.so.1
%{_libdir}/libnemo-extension.so.1.4.0
%{_libdir}/girepository-1.0/Nemo-3.0.typelib
%dir %{_libdir}/nemo/


%files devel
%dir %{_includedir}/nemo/
%dir %{_includedir}/nemo/libnemo-extension/
%{_includedir}/nemo/libnemo-extension/*.h
%{_libdir}/libnemo-extension.so
%{_libdir}/pkgconfig/libnemo-extension.pc
%{_datadir}/gir-1.0/Nemo-3.0.gir
%doc %{_datadir}/gtk-doc/html/libnemo-extension/


%changelog
