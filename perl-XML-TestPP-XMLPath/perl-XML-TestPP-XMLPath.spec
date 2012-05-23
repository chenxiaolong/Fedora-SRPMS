Name:		perl-XML-TestPP-XMLPath
Version:	0.63
Release:	1%{?dist}
Summary:	A pure PERL module to compliment the pure PERL XML::TreePP module

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://www.codepin.org/project/perlmod/XML-TreePP-XMLPath/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RG/RGLAUE/XML-TreePP-XMLPath-0.63.tgz

BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
A pure PERL module to compliment the pure PERL XML::TreePP module. XMLPath may
be similar to XPath, and it does attempt to conform to the XPath standard when
possible, but it is far from being fully XPath compliant. Its purpose is to
implement an XPath-like accessor methodology to nodes in a XML::TreePP parsed
XML Document. In contrast, XPath is an accessor methodology to nodes in an
unparsed XML Document.


%prep
%setup -q -n XML-TreePP-XMLPath-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%files
%defattr(-,root,root,-)
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed May 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.63-1
- Initial release
