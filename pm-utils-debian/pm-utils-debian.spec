# A debuginfo package is pointless when there are no binaries
%define debug_package %{nil}

%define _debian_rel 9

Name:		pm-utils-debian
Summary:	Power management utilities and scripts for Fedora (with Debian's additions)
License:	GPLv2
Version:	1.4.1
Release:	12.%{_debian_rel}%{?dist}
Group:		System Environment/Base
URL:		http://pm-utils.freedesktop.org

BuildRequires:	xmlto
Requires:	pm-utils

Source0:	http://pm-utils.freedesktop.org/releases/pm-utils-%{version}.tar.gz
Source1:	http://ftp.de.debian.org/debian/pool/main/p/pm-utils/pm-utils_%{version}-%{_debian_rel}.debian.tar.gz

# Use append instead of write for init_logfile (#660329)
Patch0:		pm-utils-1.4.1-init-logfile-append.patch
# Fix typo in 55NetworkManager (#722759)
Patch1:		pm-utils-1.4.1-networkmanager-typo-fix.patch
# Add support for grub2 in 01grub hook
Patch2:		pm-utils-1.4.1-grub2.patch
# Fix hooks exit code logging
Patch3:		pm-utils-1.4.1-hook-exit-code-log.patch


%description
The pm-utils package contains utilities and scripts useful for tasks related
to power management.


%prep
%setup -q -n pm-utils-%{version}
%patch0 -p1 -b .init-logfile-append
%patch1 -p1 -b .network-manager-typo-fix.patch
%patch2 -p1 -b .grub2
%patch3 -p1 -b .hook-exit-code-log

# Apply Debian patches
tar zxvf "%{SOURCE1}"
# Do not apply these patches
  # Do not change service start/stop commands
    sed -i '/80-service.patch/d' debian/patches/series
  # Handled in Fedora's patches
    sed -i '/26-inhibit-on-right-status.patch/d' debian/patches/series
    sed -i '/02-logging-append.patch/d' debian/patches/series

for i in $(cat debian/series/patches | grep -v '#'); do
  patch -Np1 -i "debian/patches/${i}"
done

# For the doc macro in the files section
cp debian/changelog{,.debian}


%build
%configure
make %{?_smp_mflags}


%install
rm -rvf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove stuff in original pm-utils package
rm -v \
  $RPM_BUILD_ROOT%{_bindir}/on_ac_power \
  $RPM_BUILD_ROOT%{_bindir}/pm-is-supported \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/bin/pm-action \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/bin/pm-pmu \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/bin/pm-reset-swap \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/bin/service \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/defaults \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/functions \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/module.d/kernel \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/module.d/tuxonice \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/module.d/uswsusp \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/pm-functions \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/00logging \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/00powersave \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/01grub \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/49bluetooth \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/55NetworkManager \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/75modules \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/90clock \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/94cpufreq \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/95led \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/98video-quirk-db-handler \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/99video \
  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/pm-utils.pc \
  $RPM_BUILD_ROOT%{_sbindir}/pm-hibernate \
  $RPM_BUILD_ROOT%{_sbindir}/pm-powersave \
  $RPM_BUILD_ROOT%{_sbindir}/pm-suspend \
  $RPM_BUILD_ROOT%{_sbindir}/pm-suspend-hybrid \
  $RPM_BUILD_ROOT%{_docdir}/pm-utils/HOWTO.hooks \
  $RPM_BUILD_ROOT%{_docdir}/pm-utils/HOWTO.modules \
  $RPM_BUILD_ROOT%{_docdir}/pm-utils/README \
  $RPM_BUILD_ROOT%{_docdir}/pm-utils/README.debugging \
  $RPM_BUILD_ROOT%{_docdir}/pm-utils/README.distributions \
  $RPM_BUILD_ROOT%{_mandir}/man1/on_ac_power.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/pm-is-supported.1 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-action.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-hibernate.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-pmu.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-powersave.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-suspend-hybrid.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8/pm-suspend.8

# Remove deprecated hooks
rm -v $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/hal-cd-polling

# Remove unstable hooks
rm -v $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/harddrive

# Remove hooks that don't save power
rm -v \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/journal-commit \
  $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/readahead

# Install hooks that haven't been upstreamed yet
install -m755 debian/power.d/* $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/


%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS ChangeLog debian/changelog.debian
%{_libdir}/pm-utils/power.d/disable_wol
%{_libdir}/pm-utils/power.d/intel-audio-powersave
%{_libdir}/pm-utils/power.d/laptop-mode
%{_libdir}/pm-utils/power.d/pci_devices
%{_libdir}/pm-utils/power.d/pcie_aspm
%{_libdir}/pm-utils/power.d/sata_alpm
%{_libdir}/pm-utils/power.d/sched-powersave
%{_libdir}/pm-utils/power.d/usb_bluetooth
%{_libdir}/pm-utils/power.d/wireless
%{_libdir}/pm-utils/power.d/xfs_buffer


%changelog
* Thu Apr 05 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1.4.1-12.9
- Install Debian's additions to pm-utils
- Remove files that belong in pm-utils, so that the two packages can be
  installed simultaneously

* Mon Aug 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-12
- Added support for grub2 in 01grub hook (grub2 patch)
- Fixed hooks exit code logging (hook-exit-code-log patch)

* Wed Aug 17 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-11
- Rebuilt due to bug in rpm-4.9.1

* Tue Jul 19 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-10
- Fixed typo in 55NetworkManager
  Resolves: rhbz#722759

* Thu Jul 07 2011 Adam Jackson <ajax@redhat.com> 1.4.1-9
- Drop Requires: radeontool, not needed with KMS.

* Tue Jun 07 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-8
- restorecon now runs conditionaly
  Resolves: rhbz#710928

* Wed Mar 23 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-7
- Fixed typo, related to #663995

* Thu Mar 17 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-6
- Fixed AVC during suspend / hibernate (#663995)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Matthew Garrett <mjg@redhat.com> - 1.4.1-4
- Remove the powersave fragments (#667129, #667131, #667132)

* Tue Dec 07 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-3
- Used append instead of write for init_logfile (#660329)
- Fixed and ghosted /var/run/pm-utils (#656668)
- Added postun script to clean state storage
- Updated pm-utils-bugreport-info.sh, it requires root privileges for
  correct function, moved to sbin

* Thu Nov 18 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-2
- Remove HAL from pm-utils-bugreport-info.sh
- Add quirkdb

* Mon Oct 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.1-1
- New version
- Dropped pm-utils-99hd-apm-restore hook, similar functionality provided by
  harddrive script

* Fri Oct 08 2010 Adam Jackson <ajax@redhat.com> 1.3.1-2
- Drop the vbetool dependency, suspend is only supported on KMS drivers.

* Thu Sep 01 2010 Richard Hughes <rhughes@redhat.com> - 1.3.1-1
- New upstream version
- Drop the HAL dependancy.

* Sun Mar 21 2010 Richard Hughes <rhughes@redhat.com> - 1.3.0-1
- New upstream version

* Wed Feb 24 2010 Jiri Skala <jskala@redhat.com> - 1.2.6.1-1
- latest upstream version
- fixed typo in 98smart-kernel-video

* Thu Nov 12 2009 Richard Hughes <rhughes@redhat.com> - 1.2.6-1
- New upstream version
- Make KMS detection more accurate for several KMS drivers
- Fix several typos on the documentation.

* Wed Aug 05 2009 Till Maas <opensource@till.name> - 1.2.5-6
- filesystem subpackage contents are now provided by filesystem (Red Hat
  Bugzilla 515362) filesystem-2.4.28-1.fc12

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Till Maas <opensource@till.name> - 1.2.5-4
- Remove atd script
- create filesystem subpackage for hooks

* Fri Jul 17 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.5-3
- move atd script into pm-utils

* Thu Jun 25 2009 Till Maas <opensource@till.name> - 1.2.5-2
- add check for hdparm in hd-apm-restore

* Fri Apr 24 2009 Karsten Hopp <karsten@redhat.com> 1.2.5-1.1
- we don't have kbd and hdparm on s390(x), disable build requirements

* Tue Apr 14 2009 Richard Hughes <rhughes@redhat.com> - 1.2.5-1
- New upstream version
- If running on a system that is using KMS, we will refuse to handle any video
  quirks passed to us by HAL, and we will not chvt to an empty console.
- Fix a longstanding bug in tuning scheduler powersaving knobs on SMT systems.
  
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Richard Hughes <rhughes@redhat.com> - 1.2.4-1
- Update to 1.2.4
- Fixes a glitch in module unloading
- Numerous small usability and debugging improvements

* Mon Dec 08 2008 Richard Hughes <rhughes@redhat.com> - 1.2.3-1
- Update to 1.2.3
- Removed 55battery, 50ntpd, and 65alsa hooks

* Tue Nov 04 2008 Richard Hughes <rhughes@redhat.com> - 1.2.2.1-2
- Add a patch from airlied to disable quirks when radeon is being used with KMS.

* Mon Oct 13 2008 Richard Hughes <rhughes@redhat.com> - 1.2.2.1-1
- Update to 1.2.2.1
- Supports automatically pulling quirks from HAL and has the ability to save
  the last working set of quirks to an .fdi file.

* Thu Sep 11 2008 Richard Hughes <rhughes@redhat.com> - 1.2.0-1
- Update to 1.2.0
- The core hook-running machinery will now abort running hooks of one fails,
  and the front-end scripts will return a failure error code if hook-running
  was aborted.

* Mon Jun 22 2008 Richard Hughes <rhughes@redhat.com> - 1.1.2.3-1
- Update to 1.1.2.3

* Fri Jun 20 2008 Till Maas <opensource@till.name> - 1.1.2.2-2
- %%pre and %%post scriptlets should not be needed anymore, old
  config files should be already moved in every supported release
  and the selinux context for the logfile should be restored by
  rpm
- remove pcitulils BR, it was needed for vbetool, which is in a
  separate package now
- substitute %%{__rm} macros for uniform macro usage

* Mon May 29 2008 Richard Hughes <rhughes@redhat.com> - 1.1.2.2-1
- Update to 1.1.2.2

* Mon May 28 2008 Richard Hughes <rhughes@redhat.com> - 1.1.2.1-2
- Change BR from docbook-utils to xmlto

* Mon May 28 2008 Richard Hughes <rhughes@redhat.com> - 1.1.2.1-1
- Update to 1.1.2.1

* Mon May 12 2008 Richard Hughes <rhughes@redhat.com> - 1.1.1-2
- Add missing BR for docbook-utils

* Mon May 12 2008 Richard Hughes <rhughes@redhat.com> - 1.1.1-1
- Update to 1.1.1, and drop patches that no longer apply.

* Wed Apr 30 2008 Richard Hughes <rhughes@redhat.com> - 1.1.0-9
- Remove the usermode dep on the advice of Till Maas.

* Wed Apr 30 2008 Richard Hughes <rhughes@redhat.com> - 1.1.0-8
- Rip out all the consolehelper and PAM stuff - users are not meant to be
  running these tools directly and it's a massive change from upstream.

* Fri Apr 18 2008 Peter Jones <pjones@redhat.com> - 1.1.0-7
- Default to "shutdown" for hibernate unless it's unavailable.

* Tue Apr 15 2008 Jesse Keating <jkeating@redhat.com> - 1.1.0-6
- Don't error on post restorecon call (which can fail if selinux is disabled)

* Mon Apr 14 2008 Till Maas <opensource till name> - 1.1.0-5
- remove double %%dir %%{_libdir}/pm-utils
- update pm-utils-99hd-apm-restore to work with current pm-utils release
  Red Hat Bugzilla: #442294
- move config file for hd apm restore away from config.d, which is only used
  for pm-utils internal config anymore
- own /var/run/pm-utils/ and create storage/locks subdirs (may be
  needed for selinux)
- make sure an empty logfile is created after install (touch -a ...)
- sort %%files
- make Source0: an URL
- remove Conflicts: bluez utils, all supported Fedora releases ship
  already a newer version
- remove unused BR: hal-devel, dbus-devel, pkgconfig, docbook-utils

* Mon Apr  8 2008 Richard Hughes <rhughes@redhat.com> - 1.1.0-4
- Fix build on 64 bit machines - harder.

* Mon Apr  8 2008 Richard Hughes <rhughes@redhat.com> - 1.1.0-3
- Fix build on 64 bit machines.

* Mon Apr  8 2008 Richard Hughes <rhughes@redhat.com> - 1.1.0-2
- Actually do the build.

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Add devel subpackage for the pc file

* Thu Apr 03 2008 Adam Jackson <ajax@redhat.com> 0.99.4-16
- x86_64 is not a macro, don't %%ifarch on it.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99.4-15
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Till Maas <opensource till name> - 0.99.4-14
- add pm-utils-bugreport-info.sh script to collect information for bugreports
- require Hal (RH #428452)

* Wed Jan 09 2008 Till Maas <opensource till name> - 0.99.4-13
- update README to describe the current beheaviour of pm-utils

* Tue Jan 08 2008 Till Maas <opensource till name> - 0.99.4-12
- remove ExclusiveArch, because it contains all supported archs
  (in case an arch schould be excluded, please use ExcludeArch)
- improve readability of usermode setup
- remove pm-restart pm-shutdown from usermode setup, because
  there are no such binaries
- list more files in %%files explicit to make it obvious when
  there are changes in the distributed package
- add .conf suffix to oldconfig files

* Tue Jan 08 2008 Till Maas <opensource till name> - 0.99.4-11
- make it possible to specify the hibernate mode (RH #375701)

* Wed Jan 02 2008 Till Maas <opensource till name> - 0.99.4-10
- enhance hd-apm-restore and add a config file
- fix source-definition for hd-apm-restore
- add hook suffix for hook script

* Wed Jan 02 2008 Till Maas <opensource till name> - 0.99.4-9
- restore hd apm level (RH #382061)
- Add hdparm requires for new hook

* Mon Dec 31 2007 Till Maas <opensource till name> - 0.99.4-8
- Add documentation to %%doc

* Sun Dec 30 2007 Till Maas <opensource till name> - 0.99.4-7
- fix some bugs (RH #302401)

* Tue Nov 27 2007 Dennis Gilmore <dennis@ausil.us> - 0.99.4-6
- add sparc archs to ExclusiveArch list

* Wed Oct 10 2007 Till Maas <opensource till name> - 0.99.4-5
- Require vbetool only for x86 archs (RH #325741)
- add missing BR for docbook-utils

* Thu Sep 20 2007 Till Maas <opensource till name> - 0.99.4-4
- fix manpage cut and paste mistake (RH #286201)

* Thu Sep 20 2007 Till Maas <opensource till name> - 0.99.4-3
- remove unused patch (vidhooks)
- add patch to keep logfile (RH #237840 (f7), #238068 (devel)), 
  to keep selinux context
- simplify spec
- restore selinux context of logfile in %%post 
- use rpmmacros more often

* Tue Sep 11 2007 Till Maas <opensource till name> - 0.99.4-2
- Require vbetool not on ppc and ppc64

* Mon Sep 10 2007 Peter Jones <pjones@redhat.com> - 0.99.4-1
- Merge new upstream
- remove pm/power.d/laptop-tools
- add --quirk-reset-brightness (needed for the Fujitsu Lifebook S7110)

* Sat Sep 08 2007 Till Maas <opensource till name> - 0.99.3-12
- Adjust %%files to own /etc/pm/ and /usr/lib/pm-utils/ (#233906)
- remove (C|CXX|F)FLAGS definitions, they are already in %%configure
- remove Core in Summary tag
- add URL for pm-utils
- add %%{?arm} to ExclusiveArch (#245463)
- remove vbetool and require it (it is a separate package now)
- remove radeontool and require it (it is a separate package now)
- Update License Tag
- cleanup buildrequires
- clear %%setup

* Mon Aug 27 2007 Adam Jackson <ajax@redhat.com> 0.99.3-11
- Install (not just build) vbetool and radeontool on x86_64 too
- Explicitly list files under %%_sbindir, so they don't drop away again
- Light spec cleanups

* Thu Aug 16 2007 Phil Knirsch <pknirsch@redhat.com> - 0.99.3-10
- License verification and update

* Wed Jul 18 2007 Phil Knirsch <pknirsch@redhat.com> - 0.99.3-9
- Fixed description to be distribution independant (#247366)

* Thu Jun 07 2007 Peter Jones <pjones@redhat.com> - 0.99.3-8
- Bump release and rebuild for newer buildsystem code

* Tue Jun 05 2007 Phil Knirsch <pknirsch@redhat.com> - 0.99.3-7
- Bump release and rebuild

* Tue May 29 2007 Phil Knirsch <pknirsch@redhat.com> - 0.99.3-6
- Fixed missing builds for vbetool and radeontool for some archs (#241469)
- Fixed typo in functions where wrong variable was used (#241633)

* Wed May 16 2007 Peter Jones <pjones@redhat.com> - 0.99.3-5
- ... and create the directory the logfile goes in.

* Wed May 16 2007 Peter Jones <pjones@redhat.com> - 0.99.3-4
- Bump release to appease Koji.

* Wed May 16 2007 Peter Jones <pjones@redhat.com> - 0.99.3-3
- Create logfile in %%post and %%gost it.

* Wed Apr 25 2007 Peter Jones <pjones@redhat.com> - 0.99.3-2
- Get rid of bogus redirect on "vbetool post"
- add zlib linkage for vbetool and radeontool

* Mon Mar 26 2007 Peter Jones <pjones@redhat.com> - 0.99.3-1
- update to 0.99.3
- configure manually in the spec to avoid %%_lib as lib64

* Tue Mar 13 2007 Peter Jones <pjones@redhat.com> - 0.99.2-1
- update to 0.99.2

* Fri Feb  2 2007 Peter Jones <pjones@redhat.com> - 0.99.1-1
- Fix setsysfont hook to actually hit tty0, not the pty of the current task.

* Tue Jan 30 2007 Jeremy Katz <katzj@redhat.com> - 0.19.1-6
- build so that hooks run properly on resume; fix syntax error in 
  functions-intel (pjones)

* Fri Jan 26 2007 Phil Knirsch <pknirsch@redhat.com> - 0.19.1-5
- Fixed problem with changes in 10NetworkManager hook (#224556)

* Wed Jan 24 2007 Phil Knirsch <pknirsch@redhat.com> - 0.19.1-4
- Start/stop correct services in 10NetworkManager hook (#215253)
- Fixed check for /sys/power/disk and /sys/power/state (#214407)
- Added proper error messages in case /sys/power/disk or /sys/power/state are
  missing (#215386)
- Removed service calls and module load/unload for bluetooth hook (#213387)
- Added hook file to restore the sysfont after resume (#215391)
- Added the possibility to disable hibernate and suspend completely via the
  config file (#216459)
- Symlinked the config file to /etc/sysconfig/power-management (#216459)
- Fixed pm-powersave permission check bug (#222819)
- Small specfile cleanups

* Sun Oct  1 2006 Peter Jones <pjones@redhat.com> - 0.19.1-3
- Disable bluetooth suspend/reusme hook by default; the kernel modules seem
  to support this correctly these days.

* Thu Sep 28 2006 Peter Jones <pjones@redhat.com> - 0.19.1-2
- Ignore emacs backup files in config directories (#185979)

* Tue Aug  8 2006 Peter Jones <pjones@redhat.com> - 0.19.1-1
- Hopefully fix Centrino ThinkPad suspend+resume
- Hopefully fix Intel Mac Mini/MacBook suspend+resume

* Mon Jul 31 2006 Jeremy Katz <katzj@redhat.com> - 0.19-3
- doing the vbestate save/restore on intel video with the modesetting 
  intel xorg driver is broken.  so don't do it.

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.19-2
- requier a newer version of D-Bus and rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.19-1.1
- rebuild

* Tue Jun 13 2006 Peter Jones <pjones@redhat.com> - 0.19-1
- update from CVS
- move pam and consolehelper stuff here.
- move video hooks here since HAL isn't ready

* Tue Apr 25 2006 Peter Jones <pjones@redhat.com> - 0.18-1
- Make it work cross-distro

* Mon Apr 17 2006 Peter Jones <pjones@redhat.com> - 0.17-1
- add more helper functions
- rework things that were forking an extra subshell
- fix the suspend lock
- work around bluetooth/usb suspend wackiness

* Fri Mar 17 2006 Peter Jones <pjones@redhat.com> - 0.16-1
- rework the difference between hibernate and suspend; get rid of PM_MODE
- add 00clear script
- move default_resume_kernel from "functions" to 01grub's hibernate section

* Sat Mar 11 2006 Peter Jones <pjones@redhat.com> - 0.15-1
- fix hibernate check in a way that doesn't break "sleep".

* Fri Mar 10 2006 Peter Jones <pjones@redhat.com> - 0.14-1
- fix hibernate check in /etc/pm/hooks/20video

* Fri Mar 03 2006 Phil Knirsch <pknirsch@redhat.com> - 0.13-1
- Revert last changes for ATI graphics chips as they seem to cause more
  problems than they solved.

* Wed Mar 01 2006 Phil Knirsch <pknirsch@redhat.com> - 0.12-1
- Use vbetool post instead of vbetool dpms on for ATI cards.

* Tue Feb 28 2006 Jeremy Katz <katzj@redhat.com>
- allow building on all x86 arches (#183175)

* Tue Feb 28 2006 Jeremy Katz <katzj@redhat.com> - 0.11-1
- fix display on resume with nvidia graphics
- add infrastructure to tell what pm-util is running; don't resume 
  video on return from hibernate as the BIOS has already re-initialized it

* Fri Feb 24 2006 Phil Knirsch <pknirsch@redhat.com> - 0.10-1
- Added missing pciutils-devel BuildRequires (#182566) 
- Fixed missing vbestata save/restore calls for video suspend/resume (#182167, 
  #169494)
- Renamed hook scripts to allow local pre and post inserts (#179421)
- Added support for blinking led lights on Thinkpad Laptops during suspend
  (#179420)
- Added pm-powersave script for powersaving via HAL (#169054)
- Added symlinks for pm-shutdown and pm-restart (#165953)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.09-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.09-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Jeremy Katz <katzj@redhat.com> - 0.09-1
- Remove button module on suspend
- Set default kernel in grub to current one when hibernating 
  so that resume works

* Thu Dec 22 2005 Peter Jones <pjones@redhat.com> - 0.08-1
- Fix scripts for new pciutils

* Fri Dec  9 2005 Dave Jones <davej@redhat.com>
- Update to latest vbetool (0.5-1)
  Now also built on x86-64 too.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.07-3
- rebuild for the new dbus

* Wed Nov 30 2005 Peter Jones <pjones@redhat.com> - 0.07-2
- restart ntpd in the background
- switch terminals early so we don't wake the screen back up

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> - 0.06-3
- nix that, wait for the kernel to settle down

* Wed Nov 16 2005 Bill Nottingham <notting@redhat.com> - 0.06-2
- fix LRMI usage in vbetool

* Thu Nov 10 2005 Peter Jones <pjones@redhat.com> - 0.06-1
- kill acpi_video_cmd calls in functions-ati
- fix lcd_on in functions-ati

* Fri Sep 30 2005 Bill Nottingham <notting@redhat.com> - 0.05-1
- check for presence of various tools/files before using them (#169560, #196562)

* Fri Aug 12 2005 Jeremy Katz <katzj@redhat.com> - 0.04-1
- add pm-hibernate

* Tue Jul 05 2005 Bill Nottingham <notting@redhat.com> - 0.03-1
- fix path to video functions in video hook

* Mon Jul 04 2005 Bill Nottingham <notting@redhat.com> - 0.02-1
- add a pm-suspend (#155613)

* Wed Apr 13 2005 Bill Nottingham <notting@redhat.com> - 0.01-1
- initial version - package up vbetool, radeontool, new on_ac_power
