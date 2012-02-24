Name:		dolphin-emu
Version:	3.0
Release:	1%{?dist}
Summary:	A Gamecube / Wii / Triforce Emulator

Group:		Applications/Emulators
License:	GPLv2 and BSD
URL:		https://dolphin-emu.googlecode.com/
# Run ./get-source-from-git.sh to create a tarball from git (upstream does not
# provide a tarball, but does have git tags for the versions).
Source0:	dolphin-emu-%{version}.tar.xz

# Manual page written by Glenn Rice for Ubuntu
Source1:	dolphin-emu.1

# Desktop file
Source2:	dolphin-emu.desktop

# Include the bash script mentioned above so that it gets included in the SRPM
Source3:	get-source-from-git.sh

# Dolphin only runs on Intel x86 archictures
ExclusiveArch:	x86_64 i686

BuildRequires:	alsa-lib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	Cg
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	glew-devel
BuildRequires:	libao-devel
BuildRequires:	libXrandr-devel
BuildRequires:	lzo-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	openal-soft-devel
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	SDL-devel
BuildRequires:	SFML-devel
BuildRequires:	SOIL-devel
BuildRequires:	wxGTK-devel
BuildRequires:	zlib-devel


%description
Dolphin is a Gamecube, Wii and Triforce (the arcade machine based on the
Gamecube) emulator which supports many extra features and abilities not present
on the original consoles. Gamecube and Wii compatibility is okay - one can
expect "mainstream" titles to be running in some form or another; lesser known
titles can be hit or miss. Triforce compatibility is currently limited to one
game - others require more of the Triforce-specific peripheral devices to be
emulated.

Features
* Supports DOL/ELF, Gamecube + Wii disc images / physical backup discs, Wii
  system menu / channels, and WADs.
* Debuggers for PowerPC, DSP, and graphics processors
* Interpreters and recompilers for each processor
* OpenGL, DirectX, and software renderers with graphical enhancements and
  debugging features.
* Action Replay Simulator / Gecko Code Interpreter
* Gamecube Memory Card Manager
* Real and emulated Wiimote support
* Gamepad support (including Xbox 360 pad)
* Experimental NetPlay
* Save states


%prep
%setup -q


%build
# Building inside source tree is generally not a good idea
mkdir Build && cd Build

# Optimizations (do not use when redistributing RPM; it may not run on other
# computers)
#CXXFLAGS="-O3 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=native -march=native"
#CFLAGS="-O3 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=native -march=native"
#LDFLAGS="-Wl,-z,relro,-O3"

# BUILD_SHARED_LIBS breaks the CMake build for some reason...
%cmake .. \
  -DBUILD_SHARED_LIBS:BOOL=OFF

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd Build
make install DESTDIR=$RPM_BUILD_ROOT

# Find translations
%find_lang %{name}

# Install manual page
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/

# Install desktop file
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications/ %{SOURCE2}

# Install icon
install -dm755 $RPM_BUILD_ROOT%{_datadir}/pixmaps/
install -m644 ../Source/Core/DolphinWX/resources/Dolphin.xpm \
  $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.xpm

# Remove empty file (done in git commit: b251880d8b3887e6d4119559c5efa1fd39a075b2)
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/user/GameConfig/WBEEJV.ini


%clean
rm -rf $RPM_BUILD_ROOT


%files -f Build/%{name}.lang
%defattr(-,root,root,-)
%doc Readme.txt
# Main binary
%{_bindir}/%{name}
# Game configurations, data files, etc.
%{_datadir}/%{name}/
# Manual page
%{_mandir}/man1/%{name}.1.gz
# Desktop file
%{_datadir}/applications/%{name}.desktop
# Icon
%{_datadir}/pixmaps/%{name}.xpm


%changelog
* Thu Feb 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0-1
- Initial release
- Version 3.0
