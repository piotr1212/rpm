Name:		piwik
Version:	2.1.0
Release:	1%{?dist}
Summary:    Free Web Analytics Software	

Group:		Applications/Internet
License:	GPLv3+ and Public Domain and BSD and (MIT or GPLv2) and (MIT or GPL) and MIT and (BSD or GPLv2) and LGPL and GPL and LGPLv3+ and (MIT or GPLv3) and CC-BY and LGPLv2.1
URL:	    https://piwik.org/	
Source0:	https://builds.piwik.org/%{name}-%{version}.tar.gz
Source1:	%{name}-nginx.conf

BuildArch:  noarch

#BuildRequires:	
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

# Create configdif
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -ad config/global.ini.php %{buildroot}%{_sysconfdir}/%{name}
cp -ad config/manifest.inc.php %{buildroot}%{_sysconfdir}/%{name}

# Create tmpdir (shouldn't this be in /var/lib instead of /usr/share?)
install -dm 750 %{buildroot}%{_datadir}/%{name}/tmp

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf

%files
%doc README.md LEGALNOTICE
%{_datadir}/%{name}

%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/global.ini.php
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/manifest.inc.php

%files nginx
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/tmp/

%files httpd

%changelog
* Sat Mar  8 2014 Piotr Popieluch <piotr1212@gmail.com> - 2.1.0-1
- initial package

