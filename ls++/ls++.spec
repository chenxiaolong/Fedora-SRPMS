%define tag_commit c670f04

Name:           ls++
Version:        0.340
Release:        1%{?dist}
Summary:        Colorized ls on steroids

Group:          Development/Libraries
License:        GPLv2
URL:            https://github.com/trapd00r/ls--
# Debian's Github redirection website is awesome!
Source0:        http://githubredir.debian.net/github/trapd00r/ls--/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
ls++ - colorized ls on steroids


%prep
%setup -q -n trapd00r-ls---%{tag_commit}
cp ls++.conf ls++.example.conf


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
%doc README.md ls++.example.conf
%{_mandir}/man1/ls++.conf.1.gz
%{_mandir}/man1/ls++.1.gz
%{_bindir}/ls++


%changelog
* Sat May 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.340-1
- Initial release
