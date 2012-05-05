Name:           perl-Term-ExtendedColor
Version:        0.224
Release:        1%{?dist}
Summary:        Color screen output using extended escape sequences

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Term-ExtendedColor/
Source0:        http://search.cpan.org/CPAN/authors/id/W/WO/WOLDRICH/Term-ExtendedColor-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Color screen output using extended escape sequences


%prep
%setup -q -n Term-ExtendedColor-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*
%{_bindir}/color_matrix
%{_bindir}/colored_dmesg
%{_bindir}/show_all_colors
%{_bindir}/uncolor


%changelog
* Sat May 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.224-1
- Initial release
