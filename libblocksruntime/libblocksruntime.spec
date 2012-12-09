# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%undefine _missing_build_ids_terminate_build

# I can't get version 0.2 to work yet

Name:		libblocksruntime
Version:	0.1
Release:	1%{?dist}
Summary:	Blocks Runtime Library

Group:		System Environment/Libraries
# Not sure about the license
License:	Freely redistributable without restriction
URL:		http://sourceforge.net/projects/blocksruntime/
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/libblocksruntime_%{version}.orig.tar.gz
#Source0:	%{name}-%{version}.tar.xz
# The tarball is generated with this script
Source1:	create-tarball-from-svn.sh

BuildRequires:	clang

%description
Blocks are a proposed extension to the C, Objective C, and C++ languages
developed by Apple to support the Grand Central Dispatch concurrency engine.


%package devel
Summary:	Development files for libblocksruntime
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

%description devel
Blocks are a proposed extension to the C, Objective C, and C++ languages
developed by Apple to support the Grand Central Dispatch concurrency engine.


%prep
%setup -q -n libBlocksRuntime-%{version}


%build
export CC=clang
export CFLAGS="%{optflags} -fPIC"
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/libBlocksRuntime.so.0.0


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/libBlocksRuntime.so.*


%files devel
%{_includedir}/Block.h
%{_includedir}/Block_private.h
%{_libdir}/libBlocksRuntime.so


%changelog
* Sun Dec 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1-1
- Initial release
- Version 0.1
