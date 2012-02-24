Name:		VirtualGL
Version:	2.3
Release:	5%{?dist}
Summary:	A toolkit for displaying OpenGL applications to thin clients

Group:		User Interface/X
License:	wxWidgets
URL:		http://www.virtualgl.org/
Source0:	http://downloads.sourceforge.net/project/virtualgl/VirtualGL/%{version}/VirtualGL-%{version}.tar.gz

BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	turbojpeg-devel
BuildRequires:	cmake

Requires:	lib%{name}%{?_isa} = %{version}-%{release}
Requires(pre):	shadow-utils


%description
VirtualGL is a toolkit that allows most Unix/Linux OpenGL applications to be
remotely displayed with hardware 3D acceleration to thin clients, regardless
of whether the clients have 3D capabilities, and regardless of the size of the
3D data being rendered or the speed of the network.

Using the vglrun script, the VirtualGL "faker" is loaded into an OpenGL
application at run time.  The faker then intercepts a handful of GLX calls,
which it reroutes to the server's X display (the "3D X Server", which
presumably has a 3D accelerator attached.)  The GLX commands are also
dynamically modified such that all rendering is redirected into a Pbuffer
instead of a window.  As each frame is rendered by the application, the faker
reads back the pixels from the 3D accelerator and sends them to the
"2D X Server" for compositing into the appropriate X Window.

VirtualGL can be used to give hardware-accelerated 3D capabilities to VNC or
other X proxies that either lack OpenGL support or provide it through software
rendering.  In a LAN environment, VGL can also be used with its built-in
high-performance image transport, which sends the rendered 3D images to a
remote client (vglclient) for compositing on a remote X server.  VirtualGL
also supports image transport plugins, allowing the rendered 3D images to be
sent or captured using other mechanisms.

VirtualGL is based upon ideas presented in various academic papers on
this topic, including "A Generic Solution for Hardware-Accelerated Remote
Visualization" (Stegmaier, Magallon, Ertl 2002) and "A Framework for
Interactive Hardware Accelerated Remote 3D-Visualization" (Engel, Sommer,
Ertl 2000.)


%package -n lib%{name}
Summary:	VirtualGL library
Group:		System Environment/Libraries


%description -n lib%{name}
The lib%{name} package contains the libraries for %{name}.


%package -n lib%{name}-devel
Summary:	Headers for the VirtualGL library
Group:		Development/Libraries
Requires:	lib%{name}%{?_isa} = %{version}-%{release}


%description -n lib%{name}-devel
The lib%{name}-devel package contains the source header files for %{name}.


%prep
%setup -q


%build
mkdir build
cd build
# Why not use the regular CMake variables??
%cmake .. \
  -DTJPEG_INCLUDE_DIR=%{_includedir} \
  -DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.so \
  -DVGL_DOCDIR=%{_docdir}/%{name}-%{version} \
  -DVGL_LIBDIR=%{_libdir} \
  -DVGL_FAKELIBDIR=%{_libdir}/%{name}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# Rename glxinfo binary to make it not conflict with the one from glx-utils
mv $RPM_BUILD_ROOT%{_bindir}/glxinfo{,_vgl}

# /bin/sh is not a symlink to /bin/bash
sed -i '1 s/sh/bash/' $RPM_BUILD_ROOT%{_bindir}/vglserver_config


%clean
rm -rf $RPM_BUILD_ROOT


%pre -n %{name}
# Create vglusers group as a system group
getent group vglusers >/dev/null || groupadd -r vglusers


%preun -n %{name}
# Make sure that VirtualGL is unconfigured or stuff might break
%{_bindir}/vglserver_config -unconfig &>/dev/null || :


%post -n lib%{name}-devel -p /sbin/ldconfig


%postun -n lib%{name}-devel -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
# Documentation
%{_docdir}/%{name}-%{version}
# Binaries
%{_bindir}/cpustat
%{_bindir}/glxinfo_vgl
%{_bindir}/glxspheres
%{_bindir}/nettest
%{_bindir}/tcbench
%{_bindir}/vglclient
%{_bindir}/vglconfig
%{_bindir}/vglconnect
%{_bindir}/vglgenkey
%{_bindir}/vgllogin
%{_bindir}/vglrun
%{_bindir}/vglserver_config


%files -n lib%{name}
%defattr(-,root,root,-)
# Libraries
%{_libdir}/libdlfaker.so
%{_libdir}/libgefaker.so
%{_libdir}/librrfaker.so
# Fake GL Library
%{_libdir}/%{name}/libGL.so


%files -n lib%{name}-devel
%defattr(-,root,root,-)
# Source headers
%{_includedir}/rr.h
%{_includedir}/rrtransport.h


%changelog
* Fri Feb 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3-5
- Do not install documentation in multilib packages

* Mon Feb 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3-4
- Unconfigure VirtualGL before package removal
- vglusers should be a system group

* Mon Feb 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3-3
- Fix /bin/sh -> /bin/bash in vglserver_config

* Mon Feb 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3-2
- Create the vglusers group

* Fri Jan 25 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.3-1
- Initial release
