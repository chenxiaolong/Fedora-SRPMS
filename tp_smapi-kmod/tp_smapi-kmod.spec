%define buildforkernels akmod

Name:		tp_smapi-kmod

Version:	0.41
Release:	1%{?dist}.1
Summary:	Lenovo/IBM ThinkPad hardware functions kernel module

Group:		System Environment/Kernel

License:	GPL+
# Original development page: http://tpctl.sf.net/
URL:		https://github.com/evgeni/tp_smapi
Source0:	https://github.com/downloads/evgeni/tp_smapi/tp_smapi-%{version}.tar.gz

# Debian patch for the Makefile to allow compilation for kernel versions other
# than the one currently running.
Patch0:		99_Makefile-for-Debian.patch

# Lenovo and IBM laptops only have x86 architectures
ExclusiveArch:	i686 x86_64

BuildRequires:	%{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu}}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}


%description
ThinkPad laptops include a proprietary interface called SMAPI BIOS
(System Management Application Program Interface) which provides some
hardware control functionality that is not accessible by other means.

This driver exposes some features of the SMAPI BIOS through a sysfs
interface. It is suitable for newer models, on which SMAPI is invoked
through IO port writes.

WARNING:
This driver uses undocumented features and direct hardware access.
It thus cannot be guaranteed to work, and may cause arbitrary damage
(especially on models it wasn't tested on).


%package common
# kmodtool generates a template that requires a -common package
Summary:	Lenovo/IBM ThinkPad hardware functions kernel module - Common files
Group:		System Environment/Kernel
BuildArch:	noarch


%description common
ThinkPad laptops include a proprietary interface called SMAPI BIOS
(System Management Application Program Interface) which provides some
hardware control functionality that is not accessible by other means.

This driver exposes some features of the SMAPI BIOS through a sysfs
interface. It is suitable for newer models, on which SMAPI is invoked
through IO port writes.

WARNING:
This driver uses undocumented features and direct hardware access.
It thus cannot be guaranteed to work, and may cause arbitrary damage
(especially on models it wasn't tested on).


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pushd tp_smapi-%{version}
%patch0 -p1 -b .fixmake
popd

for kernel_version in %{?kernel_versions}; do
  cp -a tp_smapi-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" \
    M="$(pwd)/_kmod_build_${kernel_version%%___*}"
done


%install
rm -rf $RPM_BUILD_ROOT

for kernel_version in %{?kernel_versions}; do
  for i in tp_smapi thinkpad_ec hdaps; do
    install -Dm755 _kmod_build_${kernel_version%%___*}/${i}.ko \
      $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/${i}.ko
  done
done
%{?akmod_install}


%files common
%defattr(-,root,root,-)
%doc tp_smapi-%{version}/{CHANGES,README,TODO}


%changelog
* Mon Mar 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.41-1.1
- Initial release
- Version 0.41
