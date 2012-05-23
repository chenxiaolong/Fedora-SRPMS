Name:		perl-Data-MessagePack
Version:	0.41
Release:	1%{?dist}
Summary:        MessagePack serialising/deserialising

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Data-MessagePack/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Data-MessagePack-%{version}.tar.gz

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::LeakTrace)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
MessagePack is a binary-based efficient object serialization format. It
enables to exchange structured objects between many languages like JSON.
But unlike JSON, it is very fast and small.


%prep
%setup -q -n Data-MessagePack-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*.3*


%changelog
* Wed May 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.41-1
- Initial release
