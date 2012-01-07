Name:		i2p
Version:	0.8.12
Release:	1%{?dist}
Summary:	Load-balanced unspoofable packet switching network

Group:		System Environment/Daemons
License:	Public Domain and BSD and GPLv3 with exceptions and MIT
URL:		http://www.i2p2.de/
Source0:	http://mirror.i2p2.de/i2psource_%{version}.tar.bz2
Source1:	http://dist.codehaus.org/jetty/jetty-5.1.x/jetty-5.1.15.tgz
Source2:	i2prouter.service

BuildRequires:	ant > 1.7.0
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	gettext
BuildRequires:	gmp-devel
BuildRequires:	dos2unix


%description
I2P is an anonymizing network, offering a simple layer that identity-sensitive
applications can use to securely communicate. All data is wrapped with several
layers of encryption, and the network is both distributed and dynamic, with no
trusted parties.


%package router
Summary:	Load-balanced unspoofable packet switching network
Group:		System Environment/Daemons

BuildArch:	noarch

Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
Requires:	java-service-wrapper
Requires:	libjbigi-java


%description router
I2P is an anonymizing network, offering a simple layer that identity-sensitive
applications can use to securely communicate. All data is wrapped with several
layers of encryption, and the network is both distributed and dynamic, with no
trusted parties.


%package -n libjbigi-java
Summary:	Java Big Integer library
Group:		System Environment/Libraries
URL:		http://www.i2p2.de/jbigi


%description -n libjbigi-java
libjbigi is a math library that is part of the I2P installation.  Use of this
library greatly enhances the efficiency of cryptographic algorithms, such as
the ones used by I2P. You can expect to see a 5-7x speed improvement on certain
tasks, such as elGamal encryption/decryption.

This Package contains the libjbigi JNI library (and on x86 platforms, jcpuid).


%package javadoc
Summary:	Documentation for I2P
Group:		Documentation

BuildArch:	noarch


%description javadoc
I2P is an anonymizing network, offering a simple layer that identity-sensitive
applications can use to securely communicate. All data is wrapped with several
layers of encryption, and the network is both distributed and dynamic, with no
trusted parties.

This package contains the Javadoc files.


%prep
%setup -q


%build
# Build i2p
# Copy jetty to appropriate directory
cp %{SOURCE1} apps/jetty/
# Locale must be set to UTF-8 for javadoc to be generated
LANG=en_US.UTF-8 TZ=UTC ant preppkg javadoc
echo 'router.updateDisabled=true' > pkg-temp/router.config
mv pkg-temp/runplain.sh pkg-temp/i2prouter-nowrapper

# Build jbigi
pushd core/c/jbigi
sed -i 's/..\/..\///g' mbuild_jbigi.sh
JAVA_HOME=/usr/lib/jvm/java ./mbuild_jbigi.sh dynamic
popd

# Build jcpuid
pushd core/c/jcpuid
JAVA_HOME=/usr/lib/jvm/java ./build.sh
popd


%install
rm -rf $RPM_BUILD_ROOT

# Binaries
install -dm755 $RPM_BUILD_ROOT%{_bindir}/
  install -m755 pkg-temp/eepget $RPM_BUILD_ROOT%{_bindir}/
  install -m755 pkg-temp/i2prouter $RPM_BUILD_ROOT%{_bindir}/
  install -m755 pkg-temp/i2prouter-nowrapper $RPM_BUILD_ROOT%{_bindir}/

# Libraries
install -dm755 $RPM_BUILD_ROOT%{_libdir}/
install -dm755 $RPM_BUILD_ROOT%{_jnidir}/i2p/
  install -m644 pkg-temp/lib/*.jar $RPM_BUILD_ROOT%{_jnidir}/i2p/
  install -m755 core/c/jbigi/libjbigi.so $RPM_BUILD_ROOT%{_libdir}/
  install -m755 core/c/jcpuid/lib/freenet/support/CPUInformation/libjcpuid-*-linux.so $RPM_BUILD_ROOT%{_libdir}/libjcpuid.so

# Data files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/i2p/
  pushd pkg-temp
  find certificates/ -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/i2p/{} \;
  find eepsite/ -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/i2p/{} \;
  find geoip/ -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/i2p/{} \;
  find webapps/ -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/i2p/{} \;
  popd
  install -m644 pkg-temp/blocklist.txt $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/hosts.txt $RPM_BUILD_ROOT%{_datadir}/i2p/
  
# Man pages
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
  install -m644 pkg-temp/man/i2prouter.1 $RPM_BUILD_ROOT%{_mandir}/man1/
  install -m644 pkg-temp/man/eepget.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Configuration files
  install -m644 pkg-temp/clients.config $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/i2psnark.config $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/i2ptunnel.config $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/systray.config $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/wrapper.config $RPM_BUILD_ROOT%{_datadir}/i2p/
  install -m644 pkg-temp/router.config $RPM_BUILD_ROOT%{_datadir}/i2p/

# Configuration file symlinks
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/blocklist.txt $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/clients.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/hosts.txt $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/i2psnark.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/i2ptunnel.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/eepsite/jetty.xml $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/router.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/systray.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/
  ln -s %{_datadir}/i2p/webapps.config $RPM_BUILD_ROOT%{_sysconfdir}/i2p/

# Example scripts
mkdir pkg-temp/examples/
cp -rv pkg-temp/scripts/ pkg-temp/examples/

# Symlink the jar libraries
ln -s %{_libdir}/java/i2p $RPM_BUILD_ROOT%{_datadir}/i2p/lib

# Fix paths
sed -i \
  -e 's|\%INSTALL_PATH|%{_datadir}/i2p|g' \
  -e 's|\%SYSTEM_java_io_tmpdir|/tmp|g' \
  $RPM_BUILD_ROOT%{_bindir}/i2prouter \
  $RPM_BUILD_ROOT%{_bindir}/i2prouter-nowrapper \
  $RPM_BUILD_ROOT%{_bindir}/eepget \
  $RPM_BUILD_ROOT%{_datadir}/i2p/wrapper.config

# Fix line endings
pushd pkg-temp/licenses/
dos2unix *
popd
pushd pkg-temp/docs/
find -type f ! -empty -exec dos2unix {} \;
popd

# Install systemd service
install -dm755 $RPM_BUILD_ROOT%{_unitdir}
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}


%pre
getent group i2p >/dev/null || groupadd --system i2p
getent passwd i2p >/dev/null || useradd --system --gid i2p -d /dev/null -s /sbin/nologin -c "Account used by the i2p package to run the daemon" i2p


%post
if [ $1 -eq 1 ]; then
  # Initial installation
  /bin/systemctl daemon-reload >/dev/null 2>&1 || ;
fi


%preun
if [ $1 -eq 0 ]; then
  # Remove, not upgrade
  /bin/systemctl --no-reload disable i2prouter.service >/dev/null 2>&1 || ;
  /bin/systemctl stop i2prouter.service >/dev/null 2>&1 || ;
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || ;
if [ $1 -ge 1 ]; then
  # Upgrade, not remove
  /bin/systemctl try-restart i2prouter.service >/dev/null 2>&1 || ;
fi


%post -n libjbigi-java -p /sbin/ldconfig


%postun -n libjbigi-java -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT
ant distclean
rm apps/jetty/jetty-*.tgz
rm core/c/jbigi/*.[s]o


%files router
%defattr(-,root,root,-)
%doc pkg-temp/LICENSE.txt
%doc pkg-temp/history.txt
%doc pkg-temp/licenses/
%doc pkg-temp/examples/
%{_sysconfdir}/i2p/
%{_bindir}/i2prouter
%{_bindir}/i2prouter-nowrapper
%{_bindir}/eepget
%{_mandir}/man1/i2prouter.1.gz
%{_mandir}/man1/eepget.1.gz
%attr(755,i2p,i2p) %{_datadir}/i2p/
%{_jnidir}/i2p/
%{_unitdir}/i2prouter.service


%files javadoc
%defattr(-,root,root,-)
%doc build/javadoc/
%doc pkg-temp/docs/


%files -n libjbigi-java
%defattr(-,root,root,-)
%{_libdir}/libjbigi.so
%{_libdir}/libjcpuid.so


%changelog
* Fri Jan 6 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> 0.8.11-1
- Initial release
- Version 0.8.11
