Summary:	IP Flow Meter is a bandwidth analysis tool
Name:		ipfm
Version:	0.11.4
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(pl):	Sieciowe/Narzêdzia
Source0:	http://www.via.ecp.fr/~tibob/ipfm/archive/%{name}-%{version}.tgz
BuildRequires:	libpcap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IP Flow Meter is a bandwidth analysis tool, that measures how much
bandwidth specified hosts use on their Internet link.

%prep
%setup  -q 

%build

%configure
%{__make} CFLAGS="%{rpmcflags}"
gzip -9nf HISTORY INSTALL LICENSE TODO

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

%{__make} ROOT=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%dir /var/log/ipfm/
%{_mandir}/*
