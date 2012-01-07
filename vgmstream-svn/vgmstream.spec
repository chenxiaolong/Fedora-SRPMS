%define _svn_rev @SVN_REV@

Name:		vgmstream-svn
Version:	0
Release:	1.%{_svn_rev}svn%{?dist}
Summary:	A library for playing streamed audio from video games

Group:		Applications/Multimedia
License:	ISC
URL:		http://hcs64.com/vgmstream.html
Source0:	vgmstream-%{_svn_rev}svn.tar.xz
Patch0:		disable_audacious_plugin.patch

Conflicts:	vgmstream
BuildRequires:	libmpg123-devel
BuildRequires:	libvorbis-devel
BuildRequires:	dos2unix


%description
vgmstream is a library for playing a wide variety of streamed audio formats
used in video games. It currently comes with source for Winamp, Audacious, and
foobar2000 plugins, and a command line decoder that outputs PCM .wav. 


%prep
%setup -q -n vgmstream-%{_svn_rev}svn
%patch0 -p1


%build
./bootstrap
%configure
pushd test
make %{?_smp_mflags}
popd
dos2unix readme.txt COPYING


%install
rm -rf $RPM_BUILD_ROOT
install -Dm755 test/test $RPM_BUILD_ROOT%{_bindir}/vgmstream


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING readme.txt
%{_bindir}/vgmstream


%changelog
* Fri Jan 6 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0-1
- SVN Package initial release
