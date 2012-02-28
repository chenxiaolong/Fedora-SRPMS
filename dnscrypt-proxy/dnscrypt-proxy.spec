Name:		dnscrypt-proxy
Version:	0.9.1
Release:	2%{?dist}
Summary:	A tool for securing communications between a client and a DNS resolver

Group:		Applications/Communications
License:	Freely redistributable without restriction
URL:		http://www.opendns.com/technology/dnscrypt
Source0:	https://github.com/downloads/opendns/%{name}/%{name}-%{version}.tar.gz
Source1:	dnscrypt-proxy.sysconfig
Source2:	dnscrypt-proxy.service

BuildRequires:	systemd-units

Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units


%description
DNSCrypt is a slight variation on DNSCurve.

DNSCurve improves the confidentiality and integrity of DNS requests using
high-speed high-security elliptic-curve cryptography. Best of all, DNSCurve
has very low overhead and adds virtually no latency to queries.

DNSCurve aims at securing the entire chain down to authoritative servers.
However, it only works with authoritative servers that explicitly support the
protocol. And unfortunately, DNSCurve hasn't received much adoption yet.

The DNSCrypt protocol is very similar to DNSCurve, but focuses on securing
communications between a client and its first-level resolver. While not
providing end-to-end security, it protects the local network (which is often
the weakest link in the chain) against man-in-the-middle attacks. It also
provides some confidentiality to DNS queries.

The DNSCrypt daemon acts as a DNS proxy between a regular client, like a DNS
cache or an operating system stub resolver, and a DNSCrypt-aware resolver,
like OpenDNS.


%prep
%setup -q


%build
# Fix rpmlint executable-stack error
LDFLAGS="%{__global_ldflags} -Wl,-z,noexecstack"

%configure
make %{?_smp_mflags}


%check
pushd src/libnacl
make %{?_smp_mflags} test
popd


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install sysconfig file
install -Dm644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

# Install systemd service
install -Dm644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service


%post
if [ ${1} -eq 1 ]; then
  # Initial installation
  /bin/systemctl daemon-reload &>/dev/null || :
fi


%preun
if [ ${1} -eq 0 ]; then
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable %{name}.service &>/dev/null || :
  /bin/systemctl stop %{name}.service &>/dev/null || :
fi


%postun
/bin/systemctl daemon-reload &>/dev/null || :
if [ ${1} -gt 1 ]; then
  # Package upgrade, not removal
  /bin/systemctl try-restart %{name}.service &>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.markdown TECHNOTES THANKS
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service


%changelog
* Tue Feb 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.1-2
- Fix rpmlint executable-stack error

* Tue Feb 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.1-1
- Initial release
- Version 0.9.1
