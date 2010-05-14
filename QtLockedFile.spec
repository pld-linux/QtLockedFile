Summary:	QFile extension with advisory locking functions
Name:		QtLockedFile
Version:	2.4
Release:	1
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtlockedfile
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtlockedfile-%{version}_1-opensource.tar.gz
# Source0-md5:	ac8f848f59038a414f3ab4f4cc08e99c
Source1:	qtlockedfile.prf
Patch0:		qtlockedfile-dont-build-example.patch
# Remove unnecessary linkage to libQtGui
Patch1:		qtlockedfile-dont-link-qtgui.patch
BuildRequires:	QtCore-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_qt4_datadir	%{_datadir}/qt4

%description
This class extends the QFile class with inter-process file locking
capabilities. If an application requires that several processes should
access the same file, QtLockedFile can be used to easily ensure that
only one process at a time is writing to the file, and that no process
is writing to it while others are reading it.

%package	devel
Summary:	Development files for QtLockedFile library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-build
Requires:	qt4-qmake

%description	devel
This package contains libraries and header files for developing
applications that use QtLockedFile.

%prep
%setup -q -n qtlockedfile-%{version}_1-opensource
%patch0 -p1
%patch1 -p1


%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# libraries
install -d $RPM_BUILD_ROOT%{_libdir}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}

rm $RPM_BUILD_ROOT%{_libdir}/lib*-%{version}.so.1.0

# headers
install -d $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -a \
    src/qtlockedfile.h \
    src/QtLockedFile \
    $RPM_BUILD_ROOT%{_includedir}/QtSolutions

install -d $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_LockedFile-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_LockedFile-%{version}.so.1

%files devel
%defattr(644,root,root,755)
%doc doc example
%{_libdir}/libQtSolutions_LockedFile-%{version}.so
# XXX shared dir with QtSingleApplication
%dir %{_includedir}/QtSolutions
%{_includedir}/QtSolutions/QtLockedFile
%{_includedir}/QtSolutions/qtlockedfile.h
%{_qt4_datadir}/mkspecs/features/qtlockedfile.prf
