Name:		cdu
Version:	0.37
Release:	1%{?dist}
Summary:	Perl script that colorizes the du utility

Group:		Applications/Text
License:	CPLv2
URL:		http://arsunik.free.fr/prog/cdu.html
Source0:	http://arsunik.free.fr/pkg/cdu-%{version}.tar.gz

Patch0:		fix_manpage_directory.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	perl


%description
cdu (for Color du) is a perl script which call du and display a pretty
histogram with optional colors which allow to imediatly see the directories
which take disk space.


%prep
%setup -q
%patch0 -p1


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/usr


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/cdu
%{_mandir}/man1/cdu.1.gz


%changelog
* Fri May 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.37-1
- Initial release
