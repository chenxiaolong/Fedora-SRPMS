%define debug_package %{nil}

Name:		rEFInd
Version:	0.2.4
Release:	1%{?dist}
Summary:	EFI boot manager for UEFI and Apple EFI systems (Rod Smith's fork of rEFIt)

Group:		System Environment/Base
License:	GPLv3 and BSD
URL:		http://www.rodsbooks.com/refind/index.html
Source0:	http://downloads.sourceforge.net/project/refind/%{version}/refind-src-%{version}.zip
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gnu-efi
Requires:	dosfstools
Requires:	efibootmgr

# Fedora doesn't support 32 bit (U)EFI anyway
ExclusiveArch:	x86_64


%description
Like rEFIt, rEFInd is a boot manager, meaning that it presents a menu of
options to the user when the computer first starts up, as shown below. rEFInd
is not a boot loader, which is a program that loads an OS kernel and hands off
control to it. Many popular boot managers, such as the Grand Unified Bootloader
(GRUB), are also boot loaders, which can blur the distinction in many users'
minds. rEFInd, though, relies on a separate boot loader to finish the handoff
to an OS; it just presents a pretty menu and gives you options for how to
proceed prior to booting an OS. All EFI-capable OSes include boot loaders, so
this limitation isn't a problem.


%prep
%setup -q -n refind-%{version}


%build
make %{?_smp_mflags} GNUEFILIB=%{_libdir} EFILIB=%{_libdir} EFICRT0=%{_libdir}/gnuefi


%install
rm -rf $RPM_BUILD_ROOT

install -dm755 $RPM_BUILD_ROOT/boot/efi/EFI/rEFInd/
install -m644 refind/refind.efi $RPM_BUILD_ROOT/boot/efi/EFI/rEFInd/rEFInd-x64.efi

# Install Icons
install -dm755 $RPM_BUILD_ROOT/boot/efi/EFI/rEFInd/icons/
install -m644 icons/* $RPM_BUILD_ROOT/boot/efi/EFI/rEFInd/icons/

# Install Example Configuration File
install -m644 refind.conf-sample $RPM_BUILD_ROOT/boot/efi/EFI/rEFInd/rEFInd.conf


%files
%defattr(-,root,root,-)
%doc CREDITS.txt LICENSE.txt NEWS.txt README.txt docs/refind/ docs/Styles/
/boot/efi/EFI/rEFInd/
%config(noreplace) /boot/efi/EFI/rEFInd/rEFInd.conf


%changelog
* Sun Apr 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.4-1
- Initial release
