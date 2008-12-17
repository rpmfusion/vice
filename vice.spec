Name:           vice
Version:        2.0
Release:        2%{?dist}
Summary:        Emulator for a variety of Commodore 8bit machines
Group:          Applications/Emulators
License:        GPL
URL:            http://www.viceteam.org/
Source0:        http://www.zimmers.net/anonftp/pub/cbm/crossplatform/emulators/VICE/vice-%{version}.tar.gz
Source1:        x128.desktop
Source2:        x64.desktop
Source3:        xcbm-ii.desktop
Source4:        xpet.desktop
Source5:        xplus4.desktop
Source6:        xvic.desktop
Source7:        vice-miniicons.tar.bz2
Source8:        vice-normalicons.tar.bz2
Source9:        vice-largeicons.tar.bz2
Patch1:         vice-1.19-datadir.patch
Patch2:         vice-htmlview.patch
Patch3:         vice-tmpnam.patch
Patch4:         vice-1.20-monitor-crash.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libXt-devel libXext-devel libXxf86vm-devel libXxf86dga-devel
BuildRequires:  giflib-devel libjpeg-devel libgnomeui-devel ffmpeg-devel
BuildRequires:  ncurses-devel readline-devel SDL-devel alsa-lib-devel
BuildRequires:  bison flex gettext info desktop-file-utils xorg-x11-font-utils
Requires:       hicolor-icon-theme xdg-utils

%description
An emulator for a variety of Commodore 8bit machines, including the C16, C64,
C128, VIC-20, PET (all models, except SuperPET 9000), Plus-4, CBM-II
(aka C610)


%prep
%setup -q
%patch1 -p1 -z .datadir
%patch2 -p1 -z .htmlview
%patch3 -p1 -z .tmpnam
%patch4 -p1 -z .mon
for i in man/*.1 doc/*.info*; do
   iconv -f ISO-8859-1 -t UTF8 $i > $i.tmp
   mv $i.tmp $i
done
# not really needed, make sure these don't get used:
rm -f src/lib/*/*.c src/lib/*/*.h


%build
%configure --enable-gnomeui --enable-fullscreen --with-sdl
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT VICEDIR=%{_datadir}/%{name}
%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# vice installs its docs under /usr/share/vice/doc, we install them ourselves
# with %doc, so nuke vice's install and create a symlink for the help function
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc
ln -s ../doc/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
for i in x128.desktop x64.desktop xcbm-ii.desktop xpet.desktop xplus4.desktop \
    xvic.desktop; do
  desktop-file-install --vendor dribble           \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    $RPM_SOURCE_DIR/$i
done
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
cd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
tar xvfj %{SOURCE7}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
cd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
tar xvfj %{SOURCE8}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
cd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
tar xvfj %{SOURCE9}
# remove "icon" from the icons name they are already in the icons dir.
cd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor
for i in */apps/*icon.png; do mv $i `echo $i|sed s/icon//`; done


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog FEEDBACK README doc/mon.txt doc/iec-bus.txt
%doc doc/html/*.html doc/html/images/* doc/html/plain/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/dribble-*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_infodir}/%{name}.info*
%{_mandir}/man1/*.1.gz


%changelog
* Wed Dec 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.0-2
- Replace htmlview requires with xdg-utils, as we have use xdg-open now

* Fri Aug  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.0-1
- New upstream release 2.0

* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.22-2
- Release bump for rpmfusion

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.22-1
- New upstream release 1.22

* Wed Apr 25 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.21-3%{?dist}
- Further fixes to the xrand code to fix more crashes on exit (drb bz 87)

* Sun Apr 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.21-2%{?dist}
- Fix vice crashing with the latest libX11 update (dribble bz 91)
- Fix vice crashing on exit due to corrupted mem

* Sat Mar 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.21-1%{?dist}
- New upstream release 1.21
- Fixup .desktop file categories for games-menus usage

* Thu Mar  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.20-3%{?dist}
- Fix dribble bug 76

* Sun Oct  1 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.20-2%{?dist}
- Add a patch from upstream which fixes the black buttons / menu problem on FC5

* Sat Sep 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.20-1%{?dist}
- New upstream release 1.20

* Fri Jun 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.19-4%{?dist}
- add Patch3, which replaces tmpnam with tempnam and creates the tmpfiles
  in a user owned dir fixing a tempfile security vulnerability.

* Fri Jun 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.19-3%{?dist}
- change --vendor fedora to --vendor dribble when installing .desktop files
- add %%{?dist} to release field in changelog
- add Patch2, which calls htmlview instead of netscape when accessing help.
- make BuildRequires conditonally Require modular or monolithic X using
  %%{?fedora} to fix building on FC-4.

* Wed Jun 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.19-2
- convert manual and info pages to UTF8

* Tue Jun 20 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.19-1
- Initial Release, loosely based on the vice package by Ian Chapman
  <ian.chapman@amiga-hardware.com>, the icons are from Mandrakes package.
