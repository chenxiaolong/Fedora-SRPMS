Name:		winusb
Version:	1.0.3
Release:	3%{?dist}
Summary:	A tool to create a bootable Windows installer on a USB drive

Group:		Applications/System
License:	GPLv2+
URL:		http://en.congelli.eu/prog_info_winusb.html
Source0:	http://fr.congelli.eu/directdl/winusb/winusb-%{version}.tar.gz

# Use pkexec instead of gksudo
Patch0:		use_pkexec.patch
# grub-install -> grub2-install
Patch1:		fix_grub-install_path.patch

BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	wxGTK-devel
Requires:	ntfsprogs
Requires:	grub2
Requires:	parted


%description
This package contains two programs:
 - winusbgui: a graphical tool that creates a Windows installer on a USB drive
   using an ISO image or a DVD.
 - winusb: a command line version of the tool.

Supported images (any version):
  Windows Vista
  Windows 7
  Windows 8
  Windows PE


%prep
%setup -q
%patch0 -p1 -b .pkexec
%patch1 -p1 -b .grub


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/winusbgui.desktop

%find_lang trad
%find_lang wxstd


%files -f trad.lang -f wxstd.lang
%defattr(-,root,root,-)
%doc AUTHORS README
%{_bindir}/winusb
%{_bindir}/winusbgui
%{_datadir}/applications/winusbgui.desktop
%{_mandir}/man1/winusb.1.gz
%{_mandir}/man1/winusbgui.1.gz
%{_datadir}/pixmaps/winusbgui-icon.png
%{_datadir}/winusb/data/



%changelog
* Wed Feb 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.3-3
- Add patch that fixes grub-install -> grub2-install

* Wed Feb 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.3-2
- Add patch to use pkexec instead of gksudo

* Wed Feb 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.3-1
- Initial release
- Version 1.0.3
