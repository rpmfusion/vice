%define _legacy_common_support 1

Name:           vice
Version:        3.4
Release:        3%{?dist}
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
Patch1:         vice-datadir.patch
Patch2:         vice-cflags-ldflags-mixup.patch
BuildRequires:  gtk3-devel
BuildRequires:  SDL2-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libGL-devel
BuildRequires:  glew-devel
BuildRequires:  giflib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  x264-devel
BuildRequires:  lame-devel
BuildRequires:  flac-devel
BuildRequires:  mpg123-devel
BuildRequires:  libvorbis-devel
BuildRequires:  readline-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libpcap-devel
BuildRequires:  libieee1284-devel
BuildRequires:  pciutils-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  perl
BuildRequires:  gettext
BuildRequires:  info
BuildRequires:  texinfo
BuildRequires:  xa
BuildRequires:  desktop-file-utils
BuildRequires:  xorg-x11-font-utils
BuildRequires:  libappstream-glib
BuildRequires:  gcc-c++ automake

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
%autosetup -p1
sed -i 's/\r//' `find -name "*.h"`
sed -i 's/\r//' `find -name "*.c"`
sed -i 's/\r//' `find -name "*.cc"`
for i in man/*.1 doc/*.info* README AUTHORS; do
   iconv -f ISO-8859-1 -t UTF8 $i > $i.tmp
   touch -r $i $i.tmp
   mv $i.tmp $i
done
# Avoid "make distclean" removing this, as we need it
mv doc/%{name}.pdf .
./autogen.sh


%build
# The build fails with linking errors when enabling LTO.
# The build fails because of the .a archives from ARCH_LIBS being passed on the
# cmdline twice. Fixing this leads to errors about undefined symbols because
# the various .a archives from ARCH_LIBS have interdependencies in 2 directions,
# so there is no working order in which they can be passed which resolves all
# symbols in one go. Passing ARCH_LIBS twice, as the upstream Makefile does
# works around this, but this breaks LTO. So lets just disable LTO for now.
%define _lto_cflags %{nil}

COMMON_FLAGS="--enable-ethernet --enable-parsid --enable-libieee1284 --without-oss --disable-arch --enable-external-ffmpeg"

# Some of the code uses GNU / XOPEN libc extensions
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE=1"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE=1"

# Build SDL version
%configure --enable-sdlui2 $COMMON_FLAGS
# Ensure the system versions of these are used
mkdir src/lib/bak
mv src/lib/lib* src/lib/ffmpeg src/lib/bak
%make_build
# Rename / save SDL binaries
for i in src/x*; do
   mv $i $i.sdl
done

# Reset source tree for building GTK version
mv src/lib/bak/* src/lib
make distclean

# Build GTK version
%configure --enable-native-gtk3ui $COMMON_FLAGS
# Ensure the system versions of these are used
rm -r src/lib/lib* src/lib/ffmpeg
%make_build


%install
%make_install VICEDIR=%{_datadir}/%{name}
# Manual install SDL version
for i in src/x*.sdl; do
  install -p -m 755 $i $RPM_BUILD_ROOT%{_bindir}
done
pushd data
  for i in */sdl_sym.vkm; do
    cp -a --parents $i $RPM_BUILD_ROOT%{_datadir}/%{name}
  done
popd

rm $RPM_BUILD_ROOT%{_infodir}/dir

# vice installs a bunch of docs under /usr/share/doc/vice which are not really
# end user oriented. Remove these.
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/*.txt
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/COPYING
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/GTK3-*.md
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/Lato-*

# Fixup wrongly installed images for the html-docs
mkdir $RPM_BUILD_ROOT%{_docdir}/%{name}/images
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/{*.png,*.gif,*.svg} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}/images

# For the manual entry in the help menu
install -p -m 644 %{name}.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}
ln -s ../doc/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

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


%files

%files common
%doc %{_docdir}/%{name}
%license COPYING
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
* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 22 2020 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4-1
- New upstream release 3.4
- Fix Fedora 33 FTBFS
- Remove obsolete gtk-icon-cache and instlal-info scriptlets

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Hans de Goede <j.w.r.degoede@gmail.com> - 3.2-1
- New upstream release 3.2 (rfbz #4950)
- Use new GTK3 UI instead of GTK2 (Bernie Innocenti)
- Use SDL2 instead of SDL for .sdl versions (Bernie Innocenti)

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct  22 2017 Roland Hermans <rolandh@users.sourceforge.net> - 3.1-1
- New upstream release 3.1 (rfbz #4528 #4429)

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

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
