%define	major 10
%define	libname %mklibname pki %{major}
%define devname %mklibname pki -d

Summary:	OpenCA PKI development library
Name:		libpki
Version:	0.6.7
Release:	1
License:	GPLv2
URL:		http://www.openca.org/projects/libpki
Group:		System/Libraries
Source0:	libpki-%{version}.tar.gz
Patch1:		libpki-0.3.0-etc_issue_fix.diff
Patch2:		libpki-0.4.1-strfmt.diff
Patch3:		libpki-0.4.1-fix-link.patch

BuildRequires:	libtool-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel

%description
OpenCA Labs' Easy to use PKI library.

%package	tools
Summary:	Shared libpki library
Group:		System/Libraries

%description	tools
This package contains various tools using the shared PKI library.

%package -n	%{libname}
Summary:	Shared libpki library
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared PKI library.

%package -n	%{devname}
Summary:	Header files, libraries and development documentation for libpki
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	pki-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for the PKI library.


%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p0

# fix strange perms
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%build
mkdir -p m4
rm -f configure
autoreconf -fi
%configure2_5x \
	--disable-static

%make LDFLAGS="%ldflags"

%install
%makeinstall_std

# lib64 fix
perl -pi -e "s|/usr/lib\b|%{_libdir}|g" %{buildroot}%{_bindir}/libpki-config \
    %{buildroot}%{_libdir}/pkgconfig/libpki.pc

# cleanup
rm -rf %{buildroot}%{_datadir}/libpki

%files tools
%{_bindir}/pki-cert
%{_bindir}/pki-crl
%{_bindir}/pki-query
%{_bindir}/pki-request
%{_bindir}/pki-tool
%{_bindir}/pki-xpair
%{_bindir}/url-tool

%files -n %{libname}
%doc AUTHORS ChangeLog NEWS README
%dir %{_sysconfdir}/libpki
%dir %{_sysconfdir}/libpki/hsm.d
%dir %{_sysconfdir}/libpki/store.d
%dir %{_sysconfdir}/libpki/profile.d
%dir %{_sysconfdir}/libpki/token.d
%config(noreplace) %{_sysconfdir}/pki.conf
%config(noreplace) %{_sysconfdir}/libpki/*.xml
%config(noreplace) %{_sysconfdir}/libpki/hsm.d/*.xml
%config(noreplace) %{_sysconfdir}/libpki/store.d/*.xml
%config(noreplace) %{_sysconfdir}/libpki/profile.d/*.xml
%config(noreplace) %{_sysconfdir}/libpki/token.d/*.xml
%{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%{_includedir}/libpki
%{_bindir}/libpki-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpki.pc

