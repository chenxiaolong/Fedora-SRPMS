#SVN versions
%define _svn_rev REPLACESVN
%define _umplayer_ver REPLACEVER

#Some distribution specific stuff
%if %{defined fedora}
  #Qt tools in fedora are named a little differently
  %define _qt4_lrelease lrelease-qt4
%else
  %define _qt4_qmake qmake
  %define _qt4_lrelease lrelease
%endif

Name:           umplayer
Version:        %{_umplayer_ver}
Release:        1.r%{_svn_rev}svn%{?dist}
Summary:        UMPlayer plays everything (frontend for MPlayer)

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://umplayer.com/
Source0:        umplayer-%{version}_svn_r%{_svn_rev}.tar.bz2

BuildRequires:  hicolor-icon-theme
BuildRequires:  gettext

#Fedora build dependencies
%if %{defined fedora}
BuildRequires:  qt-devel
BuildRequires:  desktop-file-utils
%endif
#openSuSE build dependencies
%if %{defined suse_version}
BuildRequires:  libqt4-devel
BuildRequires:  update-desktop-files
%endif

Requires:       mplayer


%description
UMPlayer is the media player that fills all your needs. With dozens of advanced
features and built-in codecs it can handle any media format, and can play Audio
CDs, DVDs, (S)VCDs, TV / Radio cards, YouTube™ and SHOUTcast™ streams and even
incomplete or damaged media files.

One of the most interesting features of UMPlayer: it remembers the settings of
all files you play. So you start to watch a movie but you have to leave...
don't worry, when you open that movie again it will resume at the same point
you left it, and with the same settings: audio track, subtitles, volume...


#Themes subpackage
%package themes
Summary:        Themes for UMPlayer
Requires:       %{name}

Provides:       umplayer-theme-Black umplayer-theme-Gonzo umplayer-theme-Mac umplayer-theme-Modern umplayer-theme-Vista

%description themes
This package contains the Black, Gonzo, Mac, Modern, and Vista themes for
UMPlayer.


#Translations subpackage
%package lang
%if %{defined suse_version}
#Comply with openSuSE standards for *-lang descriptions
Summary:        Languages for package umplayer
%else
Summary:        Translations for UMPlayer
%endif
Requires:       %{name}

%description lang
This package contains translations for many languages of UMPlayer.


%prep
%setup -q -n %{name}-%{version}_svn_r%{_svn_rev}

#CLRF to Unix line endings
%{__sed} -i 's/\r//g' *.txt

#Convert file to UTF-8 encoding
iconv -f Latin1 -t UTF-8 -o Changelog.new Changelog
mv Changelog.new Changelog

#Compile with %{?_smp_mflags}
sed -i '/cd src.*make/s|$| %{?_use_mflags}|' Makefile

#Documentation path in Fedora
%if %{defined fedora}
  sed -i 's|^\(DOC_PATH=\).*$|\1%{_docdir}/%{name}-%{version}|' Makefile
%endif


%build
make %{?_smp_mflags} QMAKE=%{_qt4_qmake} LRELEASE=%{_qt4_lrelease} PREFIX=%{_prefix}


%install
rm -rf %{buildroot}
make QMAKE=%{_qt4_qmake} LRELEASE=%{_qt4_lrelease} PREFIX=%{_prefix} DESTDIR=%{buildroot} install

#openSuSE packaging of *.desktop files
%if %{defined suse_version}
  for i in %{name} %{name}_enqueue; do
    %suse_update_desktop_file -r "${i}"
  done
%endif

#Fedora packaging of *.desktop files
%if %{defined fedora}
  for i in %{name} %{name}_enqueue; do
    desktop-file-install --delete-original --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/${i}.desktop
  done
%endif

#Translations (%{find_lang} doesn't work)

#Program translations
touch %{name}.lang

for i in $(find "%{buildroot}%{_datadir}/%{name}/translations/" -name '*.qm'); do
  i=${i%.*}
  i=${i##*/}
  i=${i#*_}
  [ ${i} == "en_US" ] && continue
  echo "%lang(${i}) %{_datadir}/%{name}/translations/%{name}_${i}.qm" >> "%{name}.lang"
done

#Documentation translations
#List all directories
%if %{defined fedora}
for i in $(find "%{buildroot}%{_docdir}/%{name}-%{version}/" -maxdepth 1 -type d ! -wholename '*/'); do
%else
for i in $(find "%{buildroot}%{_docdir}/%{name}/" -maxdepth 1 -type d ! -wholename '*/'); do
%endif
  [ "${i##*/}" == "en" ] && continue
  echo "%lang(${i##*/}) %{_docdir}/%{name}-%{version}/${i##*/}/" >> "%{name}.lang"
done

%files
%defattr(-,root,root,-)

#Documentation
%if %{defined fedora}
%{_docdir}/%{name}-%{version}/en/
%{_docdir}/%{name}-%{version}/*.txt
%{_docdir}/%{name}-%{version}/Changelog
%else
%{_docdir}/%{name}/en/
%{_docdir}/%{name}/*.txt
%{_docdir}/%{name}/Changelog
%endif
%{_mandir}/man1/%{name}.1.gz

#Binaries
%{_bindir}/%{name}

#Desktop files and icons
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}_enqueue.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

#Application files
%{_datadir}/%{name}/shortcuts/

#Configuration (why isn't this in /etc?)
%config(noreplace) %{_datadir}/%{name}/input.conf

#Default english locale
%lang(en_US) %{_datadir}/%{name}/translations/%{name}_en_US.qm


%files themes
%defattr(-,root,root,-)
%{_datadir}/%{name}/themes/Black/
%{_datadir}/%{name}/themes/Gonzo/
%{_datadir}/%{name}/themes/Mac/
%{_datadir}/%{name}/themes/Modern/
%{_datadir}/%{name}/themes/Vista/


%files lang -f %{name}.lang
%defattr(-,root,root,-)


%post
touch --no-create %{_datadir}/icons/hicolor
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || true;
update-desktop-database &> /dev/null || true;


%postun
#If uninstalling
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || true;
  update-desktop-database &> /dev/null || true;
fi


%changelog
* Tue Dec 6 2011 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.97-1.r180svn.fc16
- Rewrite spec file so it can compile and package UMPlayer
