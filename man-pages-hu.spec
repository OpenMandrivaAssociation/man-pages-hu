%define LANG hu
%define name man-pages-%LANG
%define version 0.2.2
%define release %mkrel 10

Summary: Hungarian manual pages
Name: %{name}
Version: %{version}
Release: %{release}
License: Distributable
Group: System/Internationalization
URL: http://www.kde.hu/mlp/man/
Source: http://www.kde.hu/mlp/man/man_hu_2001_01_05.tar.bz2
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
Autoreq: false
BuildArch: noarch

%description 
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Hungarian.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)                      
        Section 2:  System calls                                    
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd,
                nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -q -n usr
#%setup -n manpages-%LANG
%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LANG/man{1,2,3,4,5,6,7,8,9,n}

find man/hu -type f -name "*.gz" -exec gunzip {} \;

for i in 1 2 3 5 7 8; do
	cp -adpvrf man/hu/man$i $RPM_BUILD_ROOT/%_mandir/%LANG/
done

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
#%doc CHANGES README COPYRIGHT
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
/%_mandir/%LANG/man*
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

