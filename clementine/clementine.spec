Name:           clementine
Version:        1.0.0
Release:        1%{dist}
Summary:        A music player and library organiser

Group:          Applications/Multimedia
License:        GPLv3
URL:            http://clementine-player.org/
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  glew-devel
BuildRequires:  gloox-devel
BuildRequires:  gmock-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  gtest-devel
BuildRequires:  libcdio-devel
BuildRequires:  libechonest-devel
BuildRequires:  libgpod-devel
BuildRequires:  libimobiledevice-devel
BuildRequires:  liblastfm-devel
BuildRequires:  libmtp-devel
BuildRequires:  libnotify-devel
BuildRequires:  libplist-devel
BuildRequires:  libprojectM-devel
BuildRequires:  libqxt-devel
BuildRequires:  notification-daemon
BuildRequires:  protobuf-devel
BuildRequires:  qca2-devel
BuildRequires:  qjson-devel
BuildRequires:  qt4-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtlockedfile-devel
BuildRequires:  qtsinglecoreapplication-devel
BuildRequires:  qtsingleapplication-devel
BuildRequires:  sqlite-devel
BuildRequires:  taglib-devel
BuildRequires:  usbmuxd-devel

# Spotify support
BuildRequires:  libspotify-devel

%description
Clementine is a modern music player and library organiser.
It is inspired by Amarok 1.4, focusing on a fast and easy-to-use interface for
searching and playing your music.

Features include:
  * Search and play your local music library
  * Listen to internet radio from Last.fm, SomaFM, Magnatune, Jamendo and
     Icecast
  * Create smart playlists and dynamic playlists
  * Tabbed playlists, import and export M3U, XSPF, PLS and ASX
  * Visualisations from projectM
  * Lyrics and artist biographies and photos
  * Transcode music into MP3, Ogg Vorbis, Ogg Speex, FLAC or AAC
  * Edit tags on MP3 and OGG files, organise your music
  * Download missing album cover art from Last.fm
  * Cross-platform - works on Windows, Mac OS X and Linux
  * Native desktop notifications on Linux (libnotify) and Mac OS X (Growl)
  * Remote control using a Wii Remote, MPRIS or the command-line
  * Copy music to your iPod, iPhone, MTP or mass-storage USB player
  * Queue manager


%prep
%setup -q


%build
# Do not remove 3rd party libraries from the 3rdparty/ directory or CMake will
# fail to configure.
cd bin
%{cmake} .. \
  -DENABLE_BREAKPAD=ON \
  -DENABLE_PLASMARUNNER=ON \
  -DINSTALL_UBUNTU_ICONS=ON \
  -DSTATIC_SQLITE=OFF \
  -DUSE_SYSTEM_PROJECTM=ON \
  -DUSE_SYSTEM_QTSINGLEAPPLICATION=ON \
  -DUSE_SYSTEM_QXT=ON
  # Support for remotes is currently broken
  #-DENABLE_REMOTE=ON
CFLAGS="${CFLAGS} -fPIC" make %{?_smp_mflags}


%install
cd bin

# Gigantic sed line I originally wrote for the clementine-git package in the
# Arch Linux AUR, but also works here. It fixes the spotify binary installation.
sed -i -e '/"\/.*version[[:digit:]]*[-]*[[:digit:]]*bit/ s//"${CMAKE_INSTALL_PREFIX}\/bin/' -e '/clementine-spotifyblob/ s/$ENV{DESTDIR}//g' spotifyblob/blob/cmake_install.cmake

make install DESTDIR=$RPM_BUILD_ROOT

# Make spotify blob executable
chmod +x $RPM_BUILD_ROOT/usr/bin/blob

# Fix trailing space in the desktop file
sed -i 's/\(\[Pause Shortcut Group\]\) /\1/' $RPM_BUILD_ROOT%{_datadir}/applications/clementine.desktop

# Desktop file validation will fail because of the Unity quicklist groups
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/clementine.desktop || true


%clean
cd bin
make clean


%files
%defattr(-,root,root,-)
%doc Changelog COPYING
%{_bindir}/clementine
%{_bindir}/blob
%{_bindir}/clementine-spotifyblob
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/
%{_datadir}/icons/ubuntu-mono-dark/
%{_datadir}/icons/ubuntu-mono-light/


%changelog
* Tue Jan 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0.0-1
- Initial release
- Upstream version 1.0.0
- Based off of spec file generated by the Clementine CMakeLists.txt
- Based off of official Fedora spec file
