Name:		rscw
Version:	0.1a
Release:	1%{?dist}
Summary:	Receive CW through the soundcard

# IDK, Morse Code is related to sound, right?
Group:		Applications/Multimedia
License:	Freely redistributable without restriction
URL:		http://wwwhome.cs.utwente.nl/~ptdeboer/ham/rscw/
Source0:	http://wwwhome.cs.utwente.nl/~ptdeboer/ham/rscw/rscw-%{version}.tgz
Patch0:		avoid_variable_conflicts.patch
Patch1:		strlen_undefined.patch

BuildRequires:	fftw2-devel
Requires:	gtk+-devel

%description
RSCW is a Linux/Unix program for decoding morse signals using the computer's
sound card. It has been written/optimized for digging weak signals out of the
noise. However, it can only handle signals with perfect timing, which in
practice means machine-sent signals. Furthermore, the user must specify the
speed (words per minute); the program cannot (yet) determine this automatically
from the received signal. As a final inconvenience, RSCW introduces quite a bit
of delay: the decoding lags the reception by about 2 seconds. As a consequence,
RSCW is not a general-purpose morse decoder that can replace a skilled operator
in say a contest. However, it is quite useful for e.g. the automatic reception
of telemetry from amateur-radio satellites.


%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1 -b .var_conflict
%patch1 -p1 -b .strlen_undef


%build
CFLAGS="$RPM_OPT_FLAGS"
CXXFLAGS="$RPM_OPT_FLAGS"
LDFLAGS="%__global_ldflags"

# The Makefile is too hardcoded
#make %{?_smp_mflags}

gcc rscw.c -o rscw -lfftw -lrfftw -lm
gcc rscwx.c -o rscwx $(gtk-config --cflags --libs)
gcc noisycw.c -o noisycw -lm
gcc rs12tlmdec.c -o rs12tlmdec


%install
rm -rf $RPM_BUILD_ROOT
install -dm755 $RPM_BUILD_ROOT%{_bindir}/
install -m755 rscw rscwx noisycw rs12tlmdec $RPM_BUILD_ROOT%{_bindir}/


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/rscw
%{_bindir}/rscwx
%{_bindir}/noisycw
%{_bindir}/rs12tlmdec


%changelog
* Thu May 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1a-1
- Initial release
