Name:		neroaac
Version:	1.5.1
Release:	1%{?dist}
Summary:	Nero AAC reference quality MPEG-4 and 3GPP audio codec

Group:		Applications/Multimedia
# The license of the spec file is GPL, but the Nero AAC Codec is non
# distributable.
License:	GPLv3+

URL:		http://www.nero.com/eng/technologies-aac-codec.html
Source0:	http://ftp6.nero.com/tools/NeroAACCodec-%{version}.zip

# This is 32 bit proprietary software
ExclusiveArch:	i686


%description
* Compression ratios ranging from Ultra High (58 CDs fit on one!) to High-End
  Audio (2.5:1), for absolutely perfect audiophile encodings
* Crystal-clear, award-winning sound quality at every compression ratio and
  bit rate!
* Support for embedded album art including covers, booklets, and lyrics
* Store an entire audio album in a single .mp4 file with all the features of an
  Audio CD embedded inside, but at a fraction of the space!
* Reference quality MPEG-4 audio codec
* Fully compatible with the latest version of the state-of-the-art MPEG-4 audio
  standard (LC-AAC, HE-AAC and HE-AAC v2)


%prep
%setup -q -c


%build
# Proprietary; no build necessary

# Convert CRLF line endings to Unix line endings
dos2unix changelog.txt license.txt readme.txt


%install
rm -rf $RPM_BUILD_ROOT
install -dm755 "$RPM_BUILD_ROOT%{_bindir}/"
install linux/neroAac{Dec,Enc,Tag} "$RPM_BUILD_ROOT%{_bindir}/"


%files
%defattr(-,root,root,-)
%doc changelog.txt license.txt readme.txt NeroAAC_tut.pdf
%{_bindir}/neroAacDec
%{_bindir}/neroAacEnc
%{_bindir}/neroAacTag


%changelog
* Sun Feb 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.5.1-1
- Initial release
- Version 1.5.1
