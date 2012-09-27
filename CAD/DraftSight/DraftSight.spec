# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Use bundled system libraries, so do not provide or require them.
%filter_from_provides /libQt.*\.so/d
%filter_from_requires /libQt.*\.so/d
%filter_from_provides /libfreetype.so/d
%filter_from_requires /libfreetype.so/d
%filter_from_provides /libphonon.so/d
%filter_from_requires /libphonon.so/d
%filter_setup

# Skip Rpath checks
%global __arch_install_post %{nil}

Name:		DraftSight
Version:	V1R2.1
Release:	1%{?dist}
Summary:	Professional-grade free CAD software

Group:		Applications/Productivity
License:	Redistributable, no modification permitted
URL:		http://www.3ds.com/products/draftsight/overview/
Source0:	http://dl-ak.solidworks.com/nonsecure/draftsight/%{version}/draftSight.rpm

BuildRequires:	desktop-file-utils

Requires:	hicolor-icon-theme

BuildArch:	i686

%description
DraftSight lets professional CAD users, students and educators create, edit and
view DWG files.


%prep
%setup -q -T -c


%install
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0} | cpio -idmv
popd

# Place MIME types in correct directory
install -dm755 $RPM_BUILD_ROOT%{_datadir}/mime/packages/
for i in dassault-systemes_draftsight-dwg.xml \
         dassault-systemes_draftsight-dwt.xml \
         dassault-systemes_draftsight-dxf.xml; do
  mv \
    $RPM_BUILD_ROOT/opt/dassault-systemes/draftsight/mime/${i} \
    $RPM_BUILD_ROOT%{_datadir}/mime/packages/
done

# Put desktop file in correct directory
install -dm755 $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  $RPM_BUILD_ROOT/opt/dassault-systemes/draftsight/mime/dassault-systemes_draftsight.desktop

# Put icons in correct directory
pushd $RPM_BUILD_ROOT/opt/dassault-systemes/draftsight/mime/pixmaps/
  find . -type f -exec \
    install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{} ';'
popd

find $RPM_BUILD_ROOT/opt/dassault-systemes/draftsight/mime/pixmaps/ \
  -type f -name '*.png' -delete
find $RPM_BUILD_ROOT/opt/dassault-systemes/draftsight/mime/pixmaps/ \
  -type d -empty -delete


%post
update-mime-database %{_datadir}/mime/ &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
update-mime-database %{_datadir}/mime/ &>/dev/null || :
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files
%{_bindir}/draftsight
/opt/dassault-systemes/
%{_datadir}/applications/dassault-systemes_draftsight.desktop
%{_datadir}/icons/hicolor/*/dassault-systemes_draftsight.png
%{_datadir}/icons/hicolor/*/dassault-systemes_draftsight-dwg.png
%{_datadir}/icons/hicolor/*/dassault-systemes_draftsight-dwt.png
%{_datadir}/icons/hicolor/*/dassault-systemes_draftsight-dxf.png
%{_datadir}/mime/packages/dassault-systemes_draftsight-dwg.xml
%{_datadir}/mime/packages/dassault-systemes_draftsight-dwt.xml
%{_datadir}/mime/packages/dassault-systemes_draftsight-dxf.xml
%{_localstatedir}/opt/dassault-systemes/


%changelog
* Wed Sep 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - V1R2.1
- Initial release
- Version V1R2.1
