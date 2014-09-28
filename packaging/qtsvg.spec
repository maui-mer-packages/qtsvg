Name:       qt5-qtsvg
Summary:    Qt scripting module
Version:    5.0.2
Release:    1%{?dist}
Group:      Qt/Qt
License:    LGPLv2.1 with exception or GPLv3
URL:        http://qt.nokia.com
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtxml-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qmake
BuildRequires:  fdupes

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the SVG module


%package devel
Summary:    Qt SVG - development files
Group:      Qt/Qt
Requires:   %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the SVG module development files

%package plugin-imageformat-svg
Summary:    Qt SVG image format plugin
Group:      Qt/Qt
Requires:   %{name} = %{version}-%{release}

%description plugin-imageformat-svg
This package contains the SVG image format plugin

%prep
%setup -q -n %{name}-%{version}/upstream

%build
export QTDIR=/usr/share/qt5
touch .git
# Can't build without QtWidgets, see https://bugs.kde.org/show_bug.cgi?id=336028
# also this might be the cause why Hawaii doesn't show any icon
#%qmake5 QT.widgets.name= DEFINES+=QT_NO_WIDGETS
%qmake5
make %{_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;
# these manage to really royally screw up cmake
find %{buildroot}%{_libdir} -type f -name "*_*Plugin.cmake" \
-exec rm {} \;
#
%fdupes %{buildroot}/%{_includedir}


%post
/sbin/ldconfig
%postun
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libQt5Svg.so.5
%{_libdir}/libQt5Svg.so.5.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libQt5Svg.so
%{_libdir}/libQt5Svg.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5/*
%{_datadir}/qt5/mkspecs/
%{_libdir}/cmake/

%files plugin-imageformat-svg
%defattr(-,root,root,-)
%{_libdir}/qt5/plugins/imageformats/lib*svg.so
%{_libdir}/qt5/plugins/iconengines/*.so
