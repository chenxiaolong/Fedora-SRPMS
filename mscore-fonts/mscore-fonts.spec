%global fontname mscore

Name:		mscore-fonts
Version:	1.0
Release:	1%{?dist}
Summary:	Installer for the Microsoft TrueType core fonts

Group:		User Interface/X
# This spec file is licensed under the GPL, but the fonts are non-distributable
License:	GPLv3+
URL:		http://corefonts.sourceforge.net/
Source0:	corefonts.sha512sums

BuildArch:	noarch

BuildRequires:	cabextract
BuildRequires:	wget
BuildRequires:	fontpackages-devel
Requires:	fontpackages-filesystem

# Description taken from Ubuntu's ttf-mscorefonts-installer package
%description
This package contains the following Microsoft TrueType core fonts:
 * Andale Mono
 * Arial Black
 * Arial (Bold, Italic, Bold Italic)
 * Comic Sans MS (Bold)
 * Courier New (Bold, Italic, Bold Italic)
 * Georgia (Bold, Italic, Bold Italic)
 * Impact
 * Times New Roman (Bold, Italic, Bold Italic)
 * Trebuchet (Bold, Italic, Bold Italic)
 * Verdana (Bold, Italic, Bold Italic)
 * Webdings

%prep
# -T = No extract
# -c = Create and change to directory
%setup -q -T -c

URL='http://downloads.sourceforge.net/corefonts'
FONTS=('andale32.exe'
       'arial32.exe'
       'arialb32.exe'
       'comic32.exe'
       'courie32.exe'
       'georgi32.exe'
       'impact32.exe'
       'times32.exe'
       'trebuc32.exe'
       'verdan32.exe'
       'webdin32.exe'
       'wd97vwr32.exe')
for font in ${FONTS[@]}; do
  if [ ! -f "${font}" ]; then
    wget "${URL}/${font}"
  fi
done
if ! sha512sum -c %{SOURCE0}; then
  echo "sha512sums did not match!"
  exit 1
fi


%build
cabextract --lowercase *.exe
cabextract --lowercase viewer1.cab
# Remove non-ttf files and remove them
find . -type f ! -name '*.ttf' -delete


%install
rm -rf $RPM_BUILD_ROOT
install -dm755 "$RPM_BUILD_ROOT/%{_fontdir}/"
install -m644 *.ttf "$RPM_BUILD_ROOT/%{_fontdir}/"


%_font_pkg *.ttf


%changelog
* Sat Feb 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.0-1
- Initial release
