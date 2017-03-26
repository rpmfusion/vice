Name:           vice
Version:        2.4.28
Release:        2%{?dist}
Summary:        Emulator for a variety of Commodore 8bit machines
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://vice-emu.sourceforge.net/
Source0:        http://downloads.sourceforge.net/vice-emu/%{name}-%{version}.tar.gz
Source1:        x128.desktop
Source2:        x64.desktop
Source3:        xcbm-ii.desktop
Source4:        xpet.desktop
Source5:        xplus4.desktop
Source6:        xvic.desktop
Source7:        vice-miniicons.tar.bz2
Source8:        vice-normalicons.tar.bz2
Source9:        vice-largeicons.tar.bz2
Source10:       x64.appdata.xml
Source11:       x128.metainfo.xml
Source12:       xcbm-ii.metainfo.xml
Source13:       xpet.metainfo.xml
Source14:       xplus4.metainfo.xml
Source15:       xvic.metainfo.xml
Patch1:         vice-2.4.24-datadir.patch
Patch2:         vice-htmlview.patch
Patch3:         vice-norpath.patch
Patch4:         vice-2.4.28-sdl-build-fix.patch
BuildRequires:  libXt-devel libXext-devel libXxf86vm-devel libXxf86dga-devel
BuildRequires:  libXrandr-devel
BuildRequires:  giflib-devel libjpeg-devel libpng-devel
BuildRequires:  libgnomeui-devel gtkglext-devel vte-devel
BuildRequires:  ffmpeg-devel lame-devel
BuildRequires:  readline-devel SDL-devel alsa-lib-devel pulseaudio-libs-devel
BuildRequires:  libieee1284-devel libpcap-devel
BuildRequires:  bison flex gettext info desktop-file-utils xorg-x11-font-utils
BuildRequires:  libappstream-glib
Requires:       %{name}-x64 = %{version}-%{release}
Requires:       %{name}-x128 = %{version}-%{release}
Requires:       %{name}-xcbm-ii = %{version}-%{release}
Requires:       %{name}-xpet = %{version}-%{release}
Requires:       %{name}-xplus4 = %{version}-%{release}
Requires:       %{name}-xvic = %{version}-%{release}

%description
An emulator for a variety of Commodore 8bit machines, including the C16, C64,
C128, VIC-20, PET (all models, except SuperPET 9000), Plus-4, CBM-II
(aka C610)


%package        common
Summary:        Common files for %{name}
Requires:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    common
Common files for %{name}.


%package        data
Summary:        Data files for %{name}
Provides:       sidplayfp-data = %{version}-%{release}
BuildArch:      noarch

%description    data
Data files for %{name}. These can also be used together with libsidplayfp
based sid music players.


%package        x64
Summary:        Vice Commodore 64 Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    x64
Vice Commodore 64 Emulator.


%package        x128
Summary:        Vice Commodore 128 Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    x128
Vice Commodore 128 Emulator.


%package        xcbm-ii
Summary:        Vice CBM-II (C610) Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    xcbm-ii
Vice CBM-II (C610) Emulator.


%package        xpet
Summary:        Vice Commodore PET Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    xpet
Vice Commodore PET Emulator.


%package        xplus4
Summary:        Vice Commodore Plus-4 Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    xplus4
Vice Commodore Plus-4 Emulator.


%package        xvic
Summary:        Vice Commodore VIC-20 Emulator
Provides:       %{name}-engine
Requires:       %{name}-common = %{version}-%{release}

%description    xvic
Vice Commodore VIC-20 Emulator.


%prep
%setup -c -q
pushd %{name}-%{version}
sed -i 's/\r//' `find -name "*.h"`
sed -i 's/\r//' `find -name "*.c"`
sed -i 's/\r//' `find -name "*.cc"`
%patch1 -p1 -z .datadir
%patch2 -p1 -z .htmlview
%patch3 -p1 -z .norpath
%patch4 -p1 -z .norpath
for i in man/*.1 doc/*.info* README AUTHORS; do
   iconv -f ISO-8859-1 -t UTF8 $i > $i.tmp
   touch -r $i $i.tmp
   mv $i.tmp $i
done
popd

mv %{name}-%{version} %{name}-%{version}.gtk
cp -a %{name}-%{version}.gtk %{name}-%{version}.sdl


%build
COMMON_FLAGS="--enable-ethernet --enable-parsid --without-oss --disable-arch"

# workaround needed to fix incorrect toolchain check in configure script
export toolchain_check=no
export CC=gcc
export CXX=g++

pushd %{name}-%{version}.gtk
  %configure --enable-gnomeui --enable-fullscreen $COMMON_FLAGS
  # Ensure the system versions of these are used
  rm -r src/lib/lib* src/lib/ffmpeg
  make %{?_smp_mflags}
popd

pushd %{name}-%{version}.sdl
  %configure --enable-sdlui $COMMON_FLAGS
  # Ensure the system versions of these are used
  rm -r src/lib/lib* src/lib/ffmpeg
  make %{?_smp_mflags}
popd


%install
pushd %{name}-%{version}.gtk
%make_install VICEDIR=%{_datadir}/%{name}
popd

pushd %{name}-%{version}.sdl
  pushd src
    for i in x*; do
      install -p -m 755 $i $RPM_BUILD_ROOT%{_bindir}/$i.sdl
    done
  popd
  pushd data
    for i in */sdl_sym.vkm; do
      cp -a --parents $i $RPM_BUILD_ROOT%{_datadir}/%{name}
    done
  popd
popd

%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# for some reason make install drops a .txt and .pdf in the infodir ... ?
rm -f $RPM_BUILD_ROOT%{_infodir}/%{name}.txt*
rm -f $RPM_BUILD_ROOT%{_infodir}/%{name}.pdf*
# vice installs its docs under /usr/share/vice/doc, we install them ourselves
# with %%doc, so nuke vice's install and create a symlink for the help function
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc
ln -s ../doc/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc
# for use of the -data package with libsidplay bases sid players
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sidplayfp
for i in basic chargen kernal; do
  ln -s ../vice/C64/$i $RPM_BUILD_ROOT%{_datadir}/sidplayfp/$i
done

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
for i in x64 x128 xcbm-ii xpet xplus4 xvic; do
  desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    $RPM_SOURCE_DIR/$i.desktop
  install -p -m 0644 $RPM_SOURCE_DIR/$i.*.xml $RPM_BUILD_ROOT%{_datadir}/appdata
  appstream-util validate-relax --nonet \
    $RPM_BUILD_ROOT%{_datadir}/appdata/$i.*.xml
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
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor
for i in */apps/*icon.png; do mv $i `echo $i|sed s/icon//`; done
popd


%post common
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%preun common
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun common
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans common
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files

%files common -f %{name}.lang
%doc %{name}-%{version}.gtk/AUTHORS %{name}-%{version}.gtk/ChangeLog
%doc %{name}-%{version}.gtk/FEEDBACK %{name}-%{version}.gtk/README
%doc %{name}-%{version}.gtk/doc/iec-bus.txt
%doc %{name}-%{version}.gtk/doc/html/*.html
%doc %{name}-%{version}.gtk/doc/html/images
%{_bindir}/c1541
%{_bindir}/cartconv
%{_bindir}/petcat
%{_bindir}/vsid
%{_datadir}/icons/hicolor/*/apps/*.png
%{_infodir}/%{name}.info*
%{_mandir}/man1/*.1.gz

%files x64
%{_bindir}/x64*
%{_bindir}/xscpu64*
%{_datadir}/appdata/x64.appdata.xml
%{_datadir}/applications/x64.desktop

%files x128
%{_bindir}/x128*
%{_datadir}/appdata/x128.metainfo.xml
%{_datadir}/applications/x128.desktop

%files xcbm-ii
%{_bindir}/xcbm*
%{_datadir}/appdata/xcbm-ii.metainfo.xml
%{_datadir}/applications/xcbm-ii.desktop

%files xpet
%{_bindir}/xpet*
%{_datadir}/appdata/xpet.metainfo.xml
%{_datadir}/applications/xpet.desktop

%files xplus4
%{_bindir}/xplus4*
%{_datadir}/appdata/xplus4.metainfo.xml
%{_datadir}/applications/xplus4.desktop

%files xvic
%{_bindir}/xvic*
%{_datadir}/appdata/xvic.metainfo.xml
%{_datadir}/applications/xvic.desktop

%files data
%{_datadir}/%{name}
%{_datadir}/sidplayfp


%changelog
* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 27 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4.28-1
- New upstream release 2.4.28

* Mon Feb 22 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4.24-3
- Actually create the vice meta-package so that upgrades work

* Wed Feb 17 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4.24-2
- Split out all the different emulators into separate sub-packages,
  make "vice" a meta packages which simply installs all of them
- Add appdata

* Mon Feb  1 2016 Roland Hermans <rolandh@users.sourceforge.net> - 2.4.24-1
- Patches and updates for VICE 2.4.24 on Fedora 23 (rf#3961)

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Apr 13 2013 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.4-3
- Split out the data files into a vice-data subpackage, so that they can be
  used together with libsidplayfp bases sid players

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.4-2
- Add missing vte-devel BuildRequires

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.4-1
- New upstream release 2.4 (rf#2610)
- Fixes xvic sound (rf#2578)
- Fixes fullscreen issues (rf#2352)

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.9-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.9-1
- New upstream release 2.3.9

* Tue Jun 22 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-1
- New upstream release 2.2
- Also build the new SDL version, the SDL binaries are available with a
  .sdl extension, for example x64.sdl

* Wed Apr  1 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1-3
- Fix building with gcc 4.4

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1-2
- rebuild for new F11 features

* Sat Dec 27 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1-1
- New upstream release 2.1

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
