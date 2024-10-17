%define LNG hu

Summary:	Hungarian manual pages
Name:		man-pages-%{LNG}
Version:	0.2.2
Release:	31
License:	Distributable
Group:		System/Internationalization
URL:		https://www.kde.hu/mlp/man/
Source:		http://www.kde.hu/mlp/man/man_hu_2001_01_05.tar.bz2
BuildRequires:	man => 1.5j-8mdk
Requires:	locales-%LNG, man => 1.5j-8mdk
Autoreq:	false
BuildArch:	noarch
Conflicts:	filesystem < 3.0-17

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Hungarian.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd,
                nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -q -n usr
#%setup -n manpages-%LNG
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/man{1,2,3,4,5,6,7,8,9,n}

find man/hu -type f -name "*.gz" -exec gunzip {} \;

for i in 1 2 3 5 7 8; do
	cp -adpvrf man/hu/man$i %{buildroot}/%_mandir/%LNG/
done

LANG=%LNG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_bindir}/mandb %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
#%doc CHANGES README COPYRIGHT
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/index.db*
#%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
