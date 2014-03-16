Name:		piwik
Version:	2.1.0
Release:	1%{?dist}
Summary:    Free Web Analytics Software	

Group:		Applications/Internet
License:	GPLv3+ and Public Domain and BSD and (MIT or GPLv2) and (MIT or GPL) and MIT and (BSD or GPLv2) and LGPL and GPL and LGPLv3+ and (MIT or GPLv3) and CC-BY and LGPLv2.1
URL:	    https://piwik.org/	
Source0:	https://builds.piwik.org/%{name}-%{version}.tar.gz
Source1:	%{name}-nginx.conf
Source2:	%{name}-httpd.conf

BuildArch:  noarch

Requires:	%{name}-webserver mysql php-mysql php-gd php-mbstring php-xml

%description
Piwik is the leading open source web analytics platform that gives you valuable
insights into your website’s visitors, your marketing campaigns and much more,
so you can optimize your strategy and online experience of your visitors.


%package nginx
Summary:    Nginx integration for Piwik

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

Requires:   php-fpm nginx

%description nginx
%{summary}


%package httpd
Summary:    Httpd integration for Piwik

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

Requires:   php

%description httpd
%{summary}


%prep
%setup -q -n %{name}


%build
# Nothing to build


%install
install -dm 755 %{buildroot}%{_datadir}/%{name}

cp -ad composer.json %{buildroot}%{_datadir}/%{name}
cp -ad composer.lock %{buildroot}%{_datadir}/%{name}
cp -ad console %{buildroot}%{_datadir}/%{name}
cp -ad core %{buildroot}%{_datadir}/%{name}
cp -ad index.php %{buildroot}%{_datadir}/%{name}
cp -ad js %{buildroot}%{_datadir}/%{name}
cp -ad lang %{buildroot}%{_datadir}/%{name}
cp -ad LEGALNOTICE %{buildroot}%{_datadir}/%{name}
cp -ad libs %{buildroot}%{_datadir}/%{name}
cp -ad misc %{buildroot}%{_datadir}/%{name}
cp -ad piwik.js %{buildroot}%{_datadir}/%{name}
cp -ad piwik.php %{buildroot}%{_datadir}/%{name}
cp -ad plugins %{buildroot}%{_datadir}/%{name}
cp -ad README.md %{buildroot}%{_datadir}/%{name}
cp -ad tests %{buildroot}%{_datadir}/%{name}
cp -ad vendor %{buildroot}%{_datadir}/%{name}

# Create configdir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -ad config/global.ini.php %{buildroot}%{_sysconfdir}/%{name}
cp -ad config/manifest.inc.php %{buildroot}%{_sysconfdir}/%{name}

# Create tmpdir
install -dm 750 %{buildroot}%{_datadir}/%{name}/tmp

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

# nginx config
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf

# Apache httpd config
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf


%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/global.ini.php' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/manifest.inc.php' 2>/dev/null || :
restorecon -R %{_sysconfdir}/%{name} || :
semanage fcontext -a -t httpd_tmp_t '%{_datadir}/%{name}/tmp(/.*)?' 2>/dev/null || :
restorecon -R %{_datadir}/%{name}/tmp || :

%postun
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/global.ini.php' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/manifest.inc.php' 2>/dev/null || :
semanage fcontext -d -t httpd_tmp_t '%{_datadir}/%{name}/tmp(/.*)?' 2>/dev/null || :
fi

%post nginx
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif

%postun nginx
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif
fi

%post httpd
%if 0%{?fedora} || 0%{?rhel} > 6
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
/sbin/service httpd reload > /dev/null 2>&1 || :
%endif

%postun httpd
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
  /sbin/service httpd reload > /dev/null 2>&1 || :
%endif
fi


%files
%doc README.md LEGALNOTICE
%{_datadir}/%{name}

%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/global.ini.php
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/manifest.inc.php

%dir %attr(0750,apache,apache) %{_datadir}/%{name}/tmp/

%files nginx
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf

%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf

%changelog
* Sat Mar  8 2014 Piotr Popieluch <piotr1212@gmail.com> - 2.1.0-1
- initial package

