# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE1}

Name:		steam
Version:	1.0.0.14
Release:	1%{?dist}
Summary:	Installer for the Beta of the Steam software distribution service

Group:		Amusements/Games
License:	Redistributable, no modification permitted
URL:		http://www.steampowered.com/
Source0:	http://media.steampowered.com/client/installer/steam.deb
Source1:	add-requires.sh

Patch0:		0001_Remove_Ubuntu_specific_stuff.patch

ExclusiveArch:	i686

BuildRequires:	desktop-file-utils

Requires:	hicolor-icon-theme

%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized
savegame and screenshot functionality, and many social features.

By using the software, you agree to the license specified in:
  %{_docdir}/steam-%{version}/copyright


%prep
%setup -q -T -c

ar x %{SOURCE0}

tar zxvf control.tar.gz
DEB_VERSION=$(sed -n 's/Version:[ \t]*\(.*\)/\1/p' control)
if [ "x${DEB_VERSION}" != "x%{version}" ]; then
  echo "The package version in the spec file needs to be updated:"
  echo "  DEB file version:  ${DEB_VERSION}"
  echo "  spec file version: %{version}"
  exit 1
fi

ARCHIVE=$(sed -n 's/^ARCHIVE="\(.*\)"$/\1/p' %{SOURCE1})
if ! tar ztvf data.tar.gz | grep -q ${ARCHIVE}; then
  echo "The add-requires.sh script needs to be updated"
  exit 1
fi

# Workaround when building on OBS
[ ! -x %{SOURCE1} ] && chmod +x %{SOURCE1}


%install
tar zxvf data.tar.gz -C $RPM_BUILD_ROOT

# desktop-file-validate does not support Unity quicklists yet
#desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/steam.desktop

pushd $RPM_BUILD_ROOT%{_bindir}/
patch -p0 --suffix .remove-ubuntu-specific -i %{PATCH0}
popd

mv $RPM_BUILD_ROOT%{_docdir}/steam{,-%{version}}/

# Specific to Ubuntu's update manager
rm $RPM_BUILD_ROOT%{_libdir}/steam/steam-install-notify


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :


%files
%doc %{_docdir}/steam-%{version}/
%{_bindir}/steam
%dir %{_libdir}/steam/
%{_libdir}/steam/bootstraplinux_ubuntu12_32.tar.xz
%{_datadir}/applications/steam.desktop
%{_datadir}/icons/hicolor/*/apps/steam.png
%{_datadir}/pixmaps/steam.xpm
%{_mandir}/man6/steam.6.gz


%changelog
* Wed Nov 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.0.14-1
- Initial release
- Version 1.0.0.14
