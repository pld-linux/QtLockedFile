#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_with	qt5		# build Qt5

# last commit to qtlockedfile subdir in
# https://qt.gitorious.org/qt-solutions/qt-solutions/
%define	commit	17b56547d6e0d9a06603231fe2384474f9144829
Summary:	QFile extension with advisory locking functions
Name:		QtLockedFile
Version:	2.4
Release:	2
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
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_qt4_datadir	%{_datadir}/qt4
%define		_qt5_datadir	%{_datadir}/qt5

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
Requires:	qt4-build
Requires:	qt4-qmake

%description devel
This package contains libraries and header files for developing
applications that use QtLockedFile.

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
install -d $RPM_BUILD_ROOT{%{_libdir},%{_qt4_datadir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*-%{version}.so.1.0
install -d $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -p src/qtlockedfile.h src/QtLockedFile $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cd ..
%endif

%if %{with qt5}
cd build-qt5
install -d $RPM_BUILD_ROOT{%{_libdir},%{_qt5_datadir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*-%{version}.so.1.0
install -d $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -p src/qtlockedfile.h src/QtLockedFile $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_qt5_datadir}/mkspecs/features
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc README.TXT
#%doc LGPL_EXCEPTION.txt LICENSE.*
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
%endif

%if %{with qt5}
%files
%defattr(644,root,root,755)
%doc README.TXT
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
%{_qt5_datadir}/mkspecs/features/qtlockedfile.prf
%endif
