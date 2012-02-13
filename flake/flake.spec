Name:		flake
Version:	0.11
Release:	1%{?dist}
Summary:	An open-source FLAC audio encoder

Group:		Applications/Multimedia
License:	LGPLv2
URL:		http://flake-enc.sourceforge.net/
Source0:	http://downloads.sourceforge.net/flake-enc/%{name}-%{version}.tar.bz2

BuildRequires:	ffmpeg-devel

%description
The Flake encoder project was started as a way for me to learn more about
lossless audio encoding. I chose the FLAC format because it is open and
well-documented. Although the FLAC reference encoder is also free and
open-source, my goal was to implement the standard from scratch as an
independent project. Flake is licensed under the GNU LGPL.

Once Flake progressed to a usable state, I submitted the encoder to be included
as part of FFmpeg. It was included and improved upon by other FFmpeg developers.
Since then, I have added more features to Flake and improved the encoding speed.
I plan to add some of these features into FFmpeg as the encoder progresses.

There are both benefits and drawbacks to using Flake as a FLAC encoder
alternative. In its current state, Flake gives, on average, slightly better
compression than the FLAC reference encoder and is about twice as fast. However,
it does not currently implement all the advanced features such as tagging,
cuesheets, 24-bit audio, embedded pictures, and ogg encapsulation. I hope to add
these to Flake in future releases.


%package devel
Summary:	Development headers for flake


%description devel
This package includes the source headers and static library for flake.


%prep
%setup -q


%build
./configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --disable-strip
# Parallel build does not work
make -j1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{name}


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.a


%changelog
* Sun Feb 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.11-1
- Initial release
- Version 0.11
