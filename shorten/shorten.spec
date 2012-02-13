Name:		shorten
Version:	3.6.1
Release:	1%{?dist}
Summary:	A fast, low complexity waveform coder (audio compressor)

Group:		Applications/Multimedia
# shorten is fully redistributable and modifiable as long as it's not sold
License:	Freely redistributable without restriction
URL:		http://etree.org/shnutils/shorten/
Source0:	http://etree.org/shnutils/shorten/dist/src/%{name}-%{version}.tar.gz


%description
shorten is a fast, low complexity waveform coder (i.e. audio compressor),
originally written by Tony Robinson at SoftSound. It can operate in both lossy
and lossless modes.

shorten reduces the size of waveform files (such as audio) using  Huffman
coding of prediction residuals and optional additional quantisation.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/shorten
%{_mandir}/man1/%{name}.1.gz


%changelog
* Sun Feb 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-1
- Initial release
- Version 3.6.1
