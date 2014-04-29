Name:		kibana
Version:	3.0.1
Release:	1%{?dist}
Summary:    	visualize logs and time-stamped data

Group:		Applications/Internet
License:	ASL 2.0
URL:	    	http://www.elasticsearch.org/overview/kibana/
Source0:	https://download.elasticsearch.org/kibana/kibana/kibana-3.0.1.tar.gz

BuildArch:  	noarch

#BuildRequires:	
Requires:	httpd

%description
Kibana is an open source (Apache Licensed), browser based analytics and search
interface to Logstash and other timestamped data sets stored in ElasticSearch. 
With those in place Kibana is a snap to setup and start using (seriously). 
Kibana strives to be easy to get started with, while also being flexible and 
powerful


%prep
%setup -q 


%build
# Nothing to build


%install
install -dm 755 %{buildroot}/%{_datadir}/%{name}

cp -ad . %{buildroot}/%{_datadir}/%{name}

%files
%doc README.md LICENSE.md
%{_datadir}/%{name}

%changelog
* Fri Apr 18 2014 Piotr Popieluch <piotr1212@gmail.com> - 3.0.1-1
- initial package

