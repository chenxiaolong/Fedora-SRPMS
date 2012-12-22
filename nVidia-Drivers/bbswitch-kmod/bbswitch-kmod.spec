# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define buildforkernels akmod

Name:		bbswitch-kmod
Version:	0.5
Release:	1%{?dist}
Summary:	A Kernel Module to power on or off the dedicated nVidia card

Group:		System Environment/Kernel
License:	GPLv3+
URL:		https://github.com/Bumblebee-Project/bbswitch
Source0:	https://github.com/downloads/Bumblebee-Project/bbswitch/bbswitch-%{version}.tar.gz

BuildRequires:	%{_bindir}/kmodtool

# nVidia graphics cards are only present on the x86 architectures
ExclusiveArch:	%{ix86} x86_64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu}}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}

%description
bbswitch is a kernel module which automatically detects the required ACPI calls
for two kinds of Optimus laptops. It has been verified to work with "real"
Optimus and "legacy" Optimus laptops. The machines on which these tests has
performed are:

* Clevo B7130 - GT 425M ("real" Optimus, Lekensteyns laptop)
* Dell Vostro 3500 - GT 310M ("legacy" Optimus, Samsagax' laptop)

(note: there is no need to add more supported laptops here as the universal
calls should work for every laptop model supporting either Optimus calls)

It's preferred over manually hacking with the acpi_call module because it can
detect the correct handle preceding _DSM and has some built-in safeguards:

* You're not allowed to disable a card if a driver (nouveau, nvidia) is loaded.
* Before suspend, the card is automatically enabled. When resuming, it's
  disabled again if that was the case before suspending. Hibernation should
  work, but it not tested.


%package common
# kmodtool generates a template that requires a -common subpackage
Summary:	bbswitch kernel module - Common Files
Group:		System Environment/Kernel

BuildArch:	noarch

%description common
This package contains some files (README. changelog, etc) that can't go in the
kernel module package.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

for kernel_version in %{?kernel_versions} ; do
  cp -a bbswitch-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
for kernel_version in %{?kernel_versions}; do
  install -Dm755 _kmod_build_${kernel_version%%___*}/bbswitch.ko \
     $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/bbswitch.ko
done
%{?akmod_install}


%files common
%doc bbswitch-%{version}/NEWS
%doc bbswitch-%{version}/README.md


%changelog
* Fri Dec 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5-1
- Version 0.5

* Fri Oct 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4.2-1
- Initial release
- Version 0.4.2
