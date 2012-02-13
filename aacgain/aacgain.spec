%define medibuntu_ver 0.0medibuntu1

Name:		aacgain
Version:	1.9
Release:	1.%{medibuntu_ver}%{?dist}
Summary:	Normalize volume of digital music files

Group:		Applications/Multimedia
License:	GPLv2
URL:		http://altosdesign.com/aacgain/
# Use Medibuntu's source. Upstream's source code tarballs can't be found
Source0:	http://packages.medibuntu.org/pool/free/a/aacgain/%{name}_%{version}.orig.tar.gz
# Medibuntu's packaging includes a man page
Source1:	http://packages.medibuntu.org/pool/free/a/aacgain/%{name}_%{version}-%{medibuntu_ver}.diff.gz


%description
AACGain normalizes the volume of digital music files using the Replay Gain
algorithm. It works by modifying the global_gain fields in the mp4 samples.
Free-form metadata tags are added to the file to save undo information,
making the normalization process reversable. It supports AAC
(mp4/m4a/QuickTime) audio files in addition to mp3 files.

AACGain uses the same command-line user interface as mp3gain


%prep
%setup -q

zcat %{SOURCE1} | patch -Np1


%build
pushd mp4v2
%configure
popd

pushd faad2
%configure
popd

%configure

make -C mp4v2 %{?_smp_mflags}
make -C faad2 %{?_smp_mflags}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install man page
install -dm755 "$RPM_BUILD_ROOT%{_mandir}/man1/"
install -m644 debian/%{name}.1 "$RPM_BUILD_ROOT%{_mandir}/man1/"


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz


%changelog
* Sun Feb 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.9-1.0.0medibuntu1
- Initial release
- Version 1.9
