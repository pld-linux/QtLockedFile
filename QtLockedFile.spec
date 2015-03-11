#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

# last commit to qtlockedfile subdir in
# https://qt.gitorious.org/qt-solutions/qt-solutions/
%define	commit	17b56547d6e0d9a06603231fe2384474f9144829
Summary:	QFile extension with advisory locking functions
Name:		QtLockedFile
Version:	2.4
Release:	3
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
# git clone git@gitorious.org:qt-solutions/qt-solutions.git
# git checkout %{commit}
# tar -cjf QtLockedFile-%{version}.tar.bz2 -C qt-solutions/qtlockedfile .
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	8d0525b7f3dc92ee1464c6a538832535
Source1:	qtlockedfile.prf
Patch0:		qtlockedfile-dont-build-example.patch
Patch1:		qtlockedfile-use-current-version.patch
URL:		http://doc.qt.digia.com/solutions/4/qtlockedfile/qtlockedfile.html
BuildRequires:	libstdc++-devel
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	qt5-qmake >= 5.4
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt4dir	%{_datadir}/qt4
%define		qt5dir	%{_libdir}/qt5

%description
This class extends the QFile class with inter-process file locking
capabilities. If an application requires that several processes should
access the same file, QtLockedFile can be used to easily ensure that
only one process at a time is writing to the file, and that no process
is writing to it while others are reading it.

%package devel
Summary:	Development files for QtLockedFile library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use QtLockedFile.

%package -n Qt5LockedFile
Summary:	QFile extension with advisory locking functions
Group:		Libraries

%description -n Qt5LockedFile
This class extends the QFile class with inter-process file locking
capabilities. If an application requires that several processes should
access the same file, QtLockedFile can be used to easily ensure that
only one process at a time is writing to the file, and that no process
is writing to it while others are reading it.

%package -n Qt5LockedFile-devel
Summary:	Development files for Qt5LockedFile library
Group:		Development/Libraries
Requires:	Qt5LockedFile = %{version}-%{release}

%description -n Qt5LockedFile-devel
This package contains libraries and header files for developing
applications that use Qt5LockedFile.

%prep
%setup -qc
%patch0 -p1
%patch1 -p0

set -- *
install -d build-qt{4,5}
cp -al "$@" build-qt4
cp -al "$@" build-qt5

%build
%if %{with qt4}
cd build-qt4
# Does not use GNU configure
./configure -library
qmake-qt4
%{__make}
cd ..
%endif

%if %{with qt5}
cd build-qt5
./configure -library
qmake-qt5
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
cd build-qt4
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt4/QtSolutions,%{qt4dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*-%{version}.so.1.0
cp -p src/qtlockedfile.h src/QtLockedFile $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt4dir}/mkspecs/features
cd ..
%endif

%if %{with qt5}
cd build-qt5
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt5/QtSolutions,%{qt5dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*-%{version}.so.1.0
cp -p src/qtlockedfile.h src/QtLockedFile $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt5dir}/mkspecs/features
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n Qt5LockedFile -p /sbin/ldconfig
%postun	-n Qt5LockedFile -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_LockedFile-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_LockedFile-%{version}.so.1

%files devel
%defattr(644,root,root,755)
%doc doc example
%{_libdir}/libQtSolutions_LockedFile-%{version}.so
# XXX shared dir
%dir %{_includedir}/qt4/QtSolutions
%{_includedir}/qt4/QtSolutions/QtLockedFile
%{_includedir}/qt4/QtSolutions/qtlockedfile.h
%{qt4dir}/mkspecs/features/qtlockedfile.prf
%endif

%if %{with qt5}
%files -n Qt5LockedFile
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_libdir}/libQt5Solutions_LockedFile-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Solutions_LockedFile-%{version}.so.1

%files -n Qt5LockedFile-devel
%defattr(644,root,root,755)
%doc doc example
%{_libdir}/libQt5Solutions_LockedFile-%{version}.so
# XXX shared dir
%dir %{_includedir}/qt5/QtSolutions
%{_includedir}/qt5/QtSolutions/QtLockedFile
%{_includedir}/qt5/QtSolutions/qtlockedfile.h
%{qt5dir}/mkspecs/features/qtlockedfile.prf
%endif
