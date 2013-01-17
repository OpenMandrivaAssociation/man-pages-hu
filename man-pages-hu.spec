%define LNG hu
%define name man-pages-%LNG
%define version 0.2.2
%define release 18

Summary: Hungarian manual pages
Name: %{name}
Version: %{version}
Release: %{release}
License: Distributable
Group: System/Internationalization
URL: http://www.kde.hu/mlp/man/
Source: http://www.kde.hu/mlp/man/man_hu_2001_01_05.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG, man => 1.5j-8mdk
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
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%{_mandir{/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-15mdv2011.0
+ Revision: 666369
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-14mdv2011.0
+ Revision: 609321
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-13mdv2011.0
+ Revision: 609303
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.2.2-11mdv2009.1
+ Revision: 351574
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.2.2-10mdv2009.0
+ Revision: 223174
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.2.2-9mdv2008.1
+ Revision: 152938
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat May 26 2007 Adam Williamson <awilliamson@mandriva.org> 0.2.2-7mdv2008.0
+ Revision: 31260
- rebuild for new era; drop /var/catman (wildly obsolete)


* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.2.2-6mdk
- rebuild

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.2-5mdk
- build release

* Wed May 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.2-4mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - remove old makewhatis.hu since default makewhatis is now able to parse
      non english man pages
    - use new std makewhatis to build whatis in spec and in cron entry 
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes
    - default description

* Thu Mar 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.2-3mdk
- fix permission on /usr/share/man/hu/*
- provides manpages-%%LANG
- don't overwrite crontab if user altered it

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 0.2.2-2mdk
- Use %%_tmppath for BuildRoot

* Mon Feb 19 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.2.2-1mdk
- updated by Andras Timar <timar@linux-mandrake.com>

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.0-1mdk
- BM

* Sun Jul 09 2000 Tímár András <timar@linux-mandrake.com> 0.2.0-1mdk
- new release

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.0-4mdk
- use mandir macro in order to be ok when switching to /usr/share/man as
  following FHS.

* Tue Mar 28 2000 Denis Havlik <denis@mandrakesoft.com> 0.1.0-3mdk
- convert to new group scheme
- add "Prereq: sed grep man"

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved makewhatis.hu from /usr/local/sbin to /usr/sbin

* Mon Oct 11 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- first rpm for Mandrake

