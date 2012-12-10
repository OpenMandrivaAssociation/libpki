%define	major	67
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
%patch3 -p0

# fix strange perms
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
mkdir -p m4
rm -f configure
autoreconf -fi

%build
export LDFLAGS="$LDFLAGS %ldflags -llber"
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std
mv %{buildroot}%{_prefix}/etc %{buildroot}/%{_sysconfdir}

# lib64 fix
perl -pi -e "s|/usr/lib\b|%{_libdir}|g" %{buildroot}%{_bindir}/libpki-config \
    %{buildroot}%{_libdir}/pkgconfig/libpki.pc

# cleanup
rm -rf %{buildroot}%{_datadir}/libpki

%files tools
%{_bindir}/pki-cert
%{_bindir}/pki-crl
%{_bindir}/pki-derenc
%{_bindir}/pki-lirt
%{_bindir}/pki-query
%{_bindir}/pki-request
%{_bindir}/pki-siginfo
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



%changelog
* Wed Jun 13 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.6.7-1
+ Revision: 805520
- new version 0.6.7

* Thu Feb 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.4-1
+ Revision: 638131
- 0.6.4
- fix the format string errors

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2011.0
+ Revision: 600410
- 0.6.1

* Sun Sep 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-1mdv2011.0
+ Revision: 576107
- 0.5.1

* Mon Apr 19 2010 Funda Wang <fwang@mandriva.org> 0.4.1-2mdv2010.1
+ Revision: 536668
- build with correct flags

* Sun Apr 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-1mdv2010.1
+ Revision: 531310
- fix build
- 0.4.1

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-2mdv2010.1
+ Revision: 507487
- rebuild

* Fri Jan 29 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2010.1
+ Revision: 498080
- fix build
- import libpki


* Thu Jan 28 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2010.0
- initial Mandriva package
