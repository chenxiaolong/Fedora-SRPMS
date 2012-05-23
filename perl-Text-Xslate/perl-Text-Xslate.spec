Name:		perl-Text-Xslate
Version:	1.5012
Release:	1%{?dist}
Summary:	Scalable template engine for Perl5

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://xslate.org/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Text-Xslate-%{version}.tar.gz

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl-parent
BuildRequires:	perl(Any::Moose)
BuildRequires:	perl(File::Copy::Recursive)
BuildRequires:	perl(Devel::StackTrace)
BuildRequires:	perl-CGI
# Pulls in a lot of dependencies
#BuildRequires:	perl-Plack
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Xslate is a template engine for Perl5 with the following features:
 * The fastest in CPAN - Up to 50~100 times faster than TT2!
 * Support of multiple template syntaxes - TT2 compatible syntax, for example
 * Easy to enhance - by importing subroutines and/or by calling object methods
 * Safe - Escapes HTML meta characters by default
 * Debuggable - Readable error messages with correct line numbers


%prep
%setup -q -n Text-Xslate-%{version}


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
%doc Changes HACKING README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*.3*
%{_bindir}/xslate
%{_mandir}/man1/xslate.1.gz


%changelog
* Wed May 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.5012-1
- Initial release
