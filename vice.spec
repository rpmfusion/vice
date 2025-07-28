Name:           vice
Version:        3.9
Release:        4%{?dist}
Summary:        Emulator for a variety of Commodore 8bit machines
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://vice-emu.sourceforge.net/
Source0:        http://downloads.sourceforge.net/vice-emu/%{name}-%{version}.tar.gz
Source1:        x64.appdata.xml
Source2:        x128.metainfo.xml
Source3:        xcbm-ii.metainfo.xml
Source4:        xpet.metainfo.xml
Source5:        xplus4.metainfo.xml
Source6:        xvic.metainfo.xml
Patch0:         vice-cflags-ldflags-mixup.patch
# Open HTML docs in GTK3 version
Patch1:         vice-gtk3-help.patch

BuildRequires:  gcc-c++
BuildRequires:  automake
BuildRequires:  gtk3-devel
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_image-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libGL-devel
BuildRequires:  glew-devel
BuildRequires:  giflib-devel
BuildRequires:  libpng-devel
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
BuildRequires:  libcurl-devel
BuildRequires:  pciutils-devel
BuildRequires:  libevdev-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  perl
BuildRequires:  gettext
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
BuildRequires:  xa
BuildRequires:  dos2unix
BuildRequires:  xdg-utils
BuildRequires:  desktop-file-utils
BuildRequires:  xorg-x11-font-utils
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
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    x64
Vice Commodore 64 Emulator.


%package        x128
Summary:        Vice Commodore 128 Emulator
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    x128
Vice Commodore 128 Emulator.


%package        xcbm-ii
Summary:        Vice CBM-II (C610) Emulator
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    xcbm-ii
Vice CBM-II (C610) Emulator.


%package        xpet
Summary:        Vice Commodore PET Emulator
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    xpet
Vice Commodore PET Emulator.


%package        xplus4
Summary:        Vice Commodore Plus-4 Emulator
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    xplus4
Vice Commodore Plus-4 Emulator.


%package        xvic
Summary:        Vice Commodore VIC-20 Emulator
Provides:       %{name}-engine = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    xvic
Vice Commodore VIC-20 Emulator.


%prep
%autosetup -p1
sed -i 's/\r//' `find -name "*.h"`
sed -i 's/\r//' `find -name "*.c"`
sed -i 's/\r//' `find -name "*.cc"`
./autogen.sh

# Fix desktop file generation
sed -i "s/\([a-zA-Z0-9]*\)_[0-9]*\.svg/\1/" \
  src/arch/gtk3/data/unix/Makefile.am


%build
# The build fails with linking errors when enabling LTO.
# The build fails because of the .a archives from ARCH_LIBS being passed on the
# cmdline twice. Fixing this leads to errors about undefined symbols because
# the various .a archives from ARCH_LIBS have interdependencies in 2 directions,
# so there is no working order in which they can be passed which resolves all
# symbols in one go. Passing ARCH_LIBS twice, as the upstream Makefile does
# works around this, but this breaks LTO. So lets just disable LTO for now.
%define _lto_cflags %{nil}

# The old FFMPEG support was deprecated and is disabled by default. New
# experimental code was added that will work with external ffmpeg executable
# instead.
COMMON_FLAGS="--enable-x64 --enable-ethernet --disable-arch --enable-external-ffmpeg --enable-html-docs --with-libieee1284 --with-lame --with-mpg123 --with-flac --with-vorbis --with-gif --with-libcurl"

# Some of the code uses GNU / XOPEN libc extensions
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE=1"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE=1"

# Build SDL version
%configure --enable-sdl2ui $COMMON_FLAGS
%make_build
# Rename / save SDL binaries
for i in src/x*; do
   mv $i $i.sdl
done

# Reset source tree for building GTK version
make distclean

# Build GTK version
%configure --enable-gtk3ui --enable-desktop-files $COMMON_FLAGS
%make_build


%install
# Avoid the Makefiles .desktop file install as that installs them into
# $HOME/.local/share/applications
%make_install XDG_DESKTOP_MENU=/usr/bin/true
# Manual install SDL version
for i in src/x*.sdl; do
  install -p -m 755 $i $RPM_BUILD_ROOT%{_bindir}
done
pushd data
  for i in */sdl_sym.vkm; do
    cp -a --parents $i $RPM_BUILD_ROOT%{_datadir}/%{name}
  done
popd

# for use of the -data package with libsidplay bases sid players
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sidplayfp
for i in basic chargen kernal; do
  ln -s ../vice/C64/$i $RPM_BUILD_ROOT%{_datadir}/sidplayfp/$i
done

# Install HTML docs
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/html
cp -a doc/html/{fonts/,images/,vice_*.html,*.css} \
  $RPM_BUILD_ROOT%{_pkgdocdir}/html

# Patch desktop files
sed -i 's!Exec=/usr/bin/!Exec=!' \
   src/arch/gtk3/data/unix/vice-org-*.desktop
sed -i 's!Icon=/usr/share/vice/common/!Icon=!' \
   src/arch/gtk3/data/unix/vice-org-*.desktop

# Install desktop files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
for i in src/arch/gtk3/data/unix/vice-org-*.desktop; do
  desktop-file-install \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    $i
done

# Install icons
for c in C128 C64 CBM2 DTV PET Plus4 SCPU SID VIC20; do
  for i in 16 24 32 48 64 256 ; do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -p -m 644 data/common/${c}_${i}.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/${c}.png
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
  install -p -m 0644 data/common/${c}_1024.svg \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/${c}.svg
  done
done

# Install AppData files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
for i in x64 x128 xcbm-ii xpet xplus4 xvic; do
  install -p -m 0644 $RPM_SOURCE_DIR/$i.*.xml \
    $RPM_BUILD_ROOT%{_datadir}/appdata
  appstream-util validate-relax --nonet \
    $RPM_BUILD_ROOT%{_datadir}/appdata/$i.*.xml
done


%files

%files common
%doc %{_pkgdocdir}
%license COPYING
%{_bindir}/c1541
%{_bindir}/cartconv
%{_bindir}/petcat
%{_bindir}/vsid
%{_datadir}/applications/vice-org-vsid.desktop
%{_datadir}/icons/hicolor/*/apps/SID.*

%files x64
%{_bindir}/x64*
%{_bindir}/xscpu64*
%{_datadir}/appdata/x64.appdata.xml
%{_datadir}/applications/vice-org-x64*.desktop
%{_datadir}/applications/vice-org-xscpu64.desktop
%{_datadir}/icons/hicolor/*/apps/C64.*
%{_datadir}/icons/hicolor/*/apps/DTV.*
%{_datadir}/icons/hicolor/*/apps/SCPU.*

%files x128
%{_bindir}/x128*
%{_datadir}/appdata/x128.metainfo.xml
%{_datadir}/applications/vice-org-x128.desktop
%{_datadir}/icons/hicolor/*/apps/C128.*

%files xcbm-ii
%{_bindir}/xcbm*
%{_datadir}/appdata/xcbm-ii.metainfo.xml
%{_datadir}/applications/vice-org-xcbm*.desktop
%{_datadir}/icons/hicolor/*/apps/CBM2.*

%files xpet
%{_bindir}/xpet*
%{_datadir}/appdata/xpet.metainfo.xml
%{_datadir}/applications/vice-org-xpet.desktop
%{_datadir}/icons/hicolor/*/apps/PET.*

%files xplus4
%{_bindir}/xplus4*
%{_datadir}/appdata/xplus4.metainfo.xml
%{_datadir}/applications/vice-org-xplus4.desktop
%{_datadir}/icons/hicolor/*/apps/Plus4.*

%files xvic
%{_bindir}/xvic*
%{_datadir}/appdata/xvic.metainfo.xml
%{_datadir}/applications/vice-org-xvic.desktop
%{_datadir}/icons/hicolor/*/apps/VIC20.*

%files data
%{_datadir}/%{name}
%{_datadir}/sidplayfp


%changelog
* Mon Jul 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 30 2025 Leigh Scott <leigh123linux@gmail.com> - 3.9-3
- Rebuild for new flac .so version

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 25 2024 Andrea Musuruane <musuruan@gmail.com> - 3.9-1
- New upstream release 3.9

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 08 2023 Leigh Scott <leigh123linux@gmail.com> - 3.6.1-4
- Rebuild for new flac

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 17 2022 Hans de Goede <j.w.r.degoede@gmail.com> - 3.6.1-2
- Renable ffmpeg recording support using compat-ffmpeg4
- Enable GIF and libcurl support

* Mon Feb 14 2022 Andrea Musuruane <musuruan@gmail.com> - 3.6.1-1
- New upstream release 3.6.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 22 2020 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4-1
- New upstream release 3.4
- Fix Fedora 33 FTBFS
- Remove obsolete gtk-icon-cache and install-info scriptlets

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
