#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	ctypesgen
Summary:	A pure-python wrapper generator for ctypes
Summary(pl.UTF-8):	Generator wrapperów dla ctypes napisany w czystym Pythonie
Name:		python3-%{module}
Version:	1.1.1
Release:	1
License:	BSD
Group:		Libraries/Python
# only wheels on https://pypi.org/simple/ctypesgen so get from github
#Source0Download: https://github.com/davidjamesca/ctypesgen/releases
Source0:	https://github.com/ctypesgen/ctypesgen/releases/download/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	0533e8850bf754e056ac51f926b8cf94
Patch0:		python-%{module}-x32.patch
URL:		https://github.com/davidjamesca/ctypesgen
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-toml
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project automatically generates ctypes wrappers for header files
written in C.

%description -l pl.UTF-8
Ten program automatycznie generuje wrappery ctypes dla plików
nagłówkowych w C.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

find -name '*.orig' | xargs %{__rm}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -v -x --showlocals tests/testsuite.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/ctypesgen{,-3}
ln -s ctypesgen-3 $RPM_BUILD_ROOT%{_bindir}/ctypesgen

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.md todo.txt
%attr(755,root,root) %{_bindir}/ctypesgen
%attr(755,root,root) %{_bindir}/ctypesgen-3
%{py3_sitescriptdir}/ctypesgen
%{py3_sitescriptdir}/ctypesgen-%{version}-py*.egg-info
