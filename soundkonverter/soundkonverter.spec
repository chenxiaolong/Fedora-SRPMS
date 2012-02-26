Name:		soundkonverter
Version:	1.3.2
Release:	2%{?dist}
Summary:	A frontend to various audio converters

Group:		Applications/Multimedia
License:	GPLv2
URL:		http://kde-apps.org/content/show.php?content=29024
Source0:	http://kde-apps.org/CONTENT/content-files/29024-%{name}-%{version}.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	cdparanoia-devel
BuildRequires:	kdemultimedia-devel
BuildRequires:	taglib-devel
BuildRequires:	gettext

# As per Kevin Kofler's suggestion, hard require the packages needed from the
# repository.
# From Fedora:
Requires:	cdparanoia
Requires:	flac
Requires:	fluidsynth
Requires:	libmpcdec
Requires:	mppenc
Requires:	speex
Requires:	timidity++
Requires:	vorbis-tools
Requires:	vorbisgain
Requires:	wavpack
# From RPMFusion
Requires:	faac
Requires:	ffmpeg
Requires:	lame
Requires:	mac
Requires:	mp3gain
Requires:	mplayer
Requires:	twolame

%description
soundKonverter is a frontend to various audio converters.

The key features are:
- Audio conversion
- Replay Gain calculation
- CD ripping

soundKonverter has nothing to do with the soundconverter project, the very
similar name is just an unfortunate coincident.


%prep
%setup -q


%build
%cmake_kde4
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Fix and validate desktop file
sed -i -e '/Encoding/d' -e 's/CD;//' \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde4/%{name}.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/kde4/%{name}.desktop

%find_lang %{name}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGELOG README TODO

# Binaries
%{_bindir}/%{name}

# Libraries
%{_libdir}/lib%{name}core.so

# Plugins
%{_libdir}/kde4/%{name}_codec_aften.so
%{_libdir}/kde4/%{name}_codec_faac.so
%{_libdir}/kde4/%{name}_codec_ffmpeg.so
%{_libdir}/kde4/%{name}_codec_flac.so
%{_libdir}/kde4/%{name}_codec_flake.so
%{_libdir}/kde4/%{name}_codec_fluidsynth.so
%{_libdir}/kde4/%{name}_codec_lame.so
%{_libdir}/kde4/%{name}_codec_mac.so
%{_libdir}/kde4/%{name}_codec_mplayer.so
%{_libdir}/kde4/%{name}_codec_musepack.so
%{_libdir}/kde4/%{name}_codec_neroaac.so
%{_libdir}/kde4/%{name}_codec_shorten.so
%{_libdir}/kde4/%{name}_codec_speex.so
%{_libdir}/kde4/%{name}_codec_timidity.so
%{_libdir}/kde4/%{name}_codec_twolame.so
%{_libdir}/kde4/%{name}_codec_vorbistools.so
%{_libdir}/kde4/%{name}_codec_wavpack.so
%{_libdir}/kde4/%{name}_replaygain_aacgain.so
%{_libdir}/kde4/%{name}_replaygain_metaflac.so
%{_libdir}/kde4/%{name}_replaygain_mp3gain.so
%{_libdir}/kde4/%{name}_replaygain_musepackgain.so
%{_libdir}/kde4/%{name}_replaygain_vorbisgain.so
%{_libdir}/kde4/%{name}_replaygain_wvgain.so
%{_libdir}/kde4/%{name}_ripper_cdparanoia.so

# Desktop file
%{_datadir}/applications/kde4/%{name}.desktop

# Icons
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}-replaygain.png

# KDE 4 actions
%{_datadir}/kde4/apps/solid/actions/%{name}-rip-audiocd.desktop

# Data files
%{_datadir}/kde4/apps/%{name}/%{name}ui.rc
%{_datadir}/kde4/apps/%{name}/images/nocover.png

# KDE 4 services
%{_datadir}/kde4/services/%{name}_codec_aften.desktop
%{_datadir}/kde4/services/%{name}_codec_faac.desktop
%{_datadir}/kde4/services/%{name}_codec_ffmpeg.desktop
%{_datadir}/kde4/services/%{name}_codec_flac.desktop
%{_datadir}/kde4/services/%{name}_codec_flake.desktop
%{_datadir}/kde4/services/%{name}_codec_fluidsynth.desktop
%{_datadir}/kde4/services/%{name}_codec_lame.desktop
%{_datadir}/kde4/services/%{name}_codec_mac.desktop
%{_datadir}/kde4/services/%{name}_codec_mplayer.desktop
%{_datadir}/kde4/services/%{name}_codec_musepack.desktop
%{_datadir}/kde4/services/%{name}_codec_neroaac.desktop
%{_datadir}/kde4/services/%{name}_codec_shorten.desktop
%{_datadir}/kde4/services/%{name}_codec_speex.desktop
%{_datadir}/kde4/services/%{name}_codec_timidity.desktop
%{_datadir}/kde4/services/%{name}_codec_twolame.desktop
%{_datadir}/kde4/services/%{name}_codec_vorbistools.desktop
%{_datadir}/kde4/services/%{name}_codec_wavpack.desktop
%{_datadir}/kde4/services/%{name}_replaygain_aacgain.desktop
%{_datadir}/kde4/services/%{name}_replaygain_metaflac.desktop
%{_datadir}/kde4/services/%{name}_replaygain_mp3gain.desktop
%{_datadir}/kde4/services/%{name}_replaygain_musepackgain.desktop
%{_datadir}/kde4/services/%{name}_replaygain_vorbisgain.desktop
%{_datadir}/kde4/services/%{name}_replaygain_wvgain.desktop
%{_datadir}/kde4/services/%{name}_ripper_cdparanoia.desktop

# KDE 4 service types
%{_datadir}/kde4/servicetypes/%{name}_codecplugin.desktop
%{_datadir}/kde4/servicetypes/%{name}_replaygainplugin.desktop
%{_datadir}/kde4/servicetypes/%{name}_ripperplugin.desktop


%changelog
* Sun Feb 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3.1-2
- Fix description (remove list of patent-encumbered packages)
- Hard require the codecs needed for the plugins

* Sun Feb 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.3.1-1
- Initial release
- Version 1.3.1
