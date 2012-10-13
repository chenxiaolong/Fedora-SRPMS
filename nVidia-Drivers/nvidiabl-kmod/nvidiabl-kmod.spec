%define buildforkernels akmod

Name:		nvidiabl-kmod

Version:	0.73
Release:	1%{?dist}.1
Summary:	Kernel modules to adject the backlight on laptops with nVidia graphics cards

Group:		System Environment/Kernel

License:	GPL+
URL:		https://github.com/guillaumezin/nvidiabl
Source0:	https://github.com/downloads/guillaumezin/nvidiabl/nvidiabl-%{version}-source-only.dkms.tar.gz

# Patch to allow compiling for kernel versions other than the one currently
# running
Patch0:		0001-Modify-Makefile-for-Fedora-kmod-packaging.patch

# nVidia graphics cards are only present on systems with x86 architectures
ExclusiveArch:	i686 x86_64

BuildRequires:	%{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu}}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}


%description
a little Linux driver based on Andy Wingo's work
(http://wingolog.org/pub/nvbacklight-0.1.tar.bz2) and MacTel Team
(https://launchpad.net/~mactel-support) that enables the control of laptop
backlight connected to NVIDIA chip using the /sys/class/backlight interface.


%package common
# kmodtool generates a template that requires a -common package
Summary:	nvidiabl kernel module - Common files
Group:		System Environment/Kernel
BuildArch:	noarch


%description common
a little Linux driver based on Andy Wingo's work
(http://wingolog.org/pub/nvbacklight-0.1.tar.bz2) and MacTel Team
(https://launchpad.net/~mactel-support) that enables the control of laptop
backlight connected to NVIDIA chip using the /sys/class/backlight interface.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pushd dkms_source_tree
%patch0 -p1 -b .fixmake
popd

for kernel_version in %{?kernel_versions}; do
  cp -a dkms_source_tree _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" \
    M="$(pwd)/_kmod_build_${kernel_version%%___*}"
done


%install
rm -rf $RPM_BUILD_ROOT

for kernel_version in %{?kernel_versions}; do
  install -Dm755 _kmod_build_${kernel_version%%___*}/nvidiabl.ko \
    $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/nvidiabl.ko
done
%{?akmod_install}


%files common
%defattr(-,root,root,-)
%doc dkms_source_tree/README


%changelog
* Tue Mar 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.73-1.1
- Initial release
- Version 0.73
