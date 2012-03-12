Name:		deepin-scrot
Version:	0.1
Release:	1%{?dist}
Summary:	Deepin Screenshot Tool

Group:		User Interface/X
License:	LGPLv3+
URL:		https://github.com/manateelazycat/deepin-scrot

Source0:	%{name}-%{version}.tar.xz

# Run ./get-source-from-git.sh to create a tarball from git (upstream does not
# provide a tarball, but does have git tags for the versions).
Source1:	get-source-from-git.sh

# Fix path to themes
Patch0:		0001-Fix-theme-path-for-Fedora-packaging.patch

BuildArch:	noarch

BuildRequires:	python >= 2.6.6
Requires:	GConf2
Requires:	python-xlib


%description
Provide a quite easy-to-use screenshot tool. Features:
  * Global hotkey to trigger screenshot tool
  * Take screenshot of a selected area
  * Easy to add text and line drawings onto the screenshot


%prep
%setup -q
%patch0 -p1 -b .themepath


%build
# No building necessary


%install
rm -rf $RPM_BUILD_ROOT

# Install main python files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -m644 src/* $RPM_BUILD_ROOT%{_datadir}/%{name}/

# Create launcher script
install -dm755 $RPM_BUILD_ROOT%{_bindir}/
cat > $RPM_BUILD_ROOT%{_bindir}/%{name} << EOF
#!/bin/bash
cd %{_datadir}/%{name}
python2 deepinScrot.py $@
EOF
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# Install themes
install -dm755 $RPM_BUILD_ROOT%{_datadir}/%{name}/theme/
pushd theme
find . -type f -exec install -Dm644 {} \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/theme/{} \;
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README ChangeLog AUTHORS
%{_bindir}/%{name}
%{_datadir}/%{name}/*.py*
%{_datadir}/%{name}/theme/*/*.png


%changelog
* Mon Mar 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1-1
- Initial release
- Version 0.1
