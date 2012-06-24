Summary:	IP Flow Meter is a bandwidth analysis tool
Name:		ipfm
Version:	0.11.4
Release:	3
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(pl):	Sieciowe/Narz�dzia
Source0:	http://www.via.ecp.fr/~tibob/ipfm/archive/%{name}-%{version}.tgz
Source1:	%{name}.init
BuildRequires:	libpcap-devel
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/%{name}
%define		_initdir		/etc/rc.d/init.d
%define		_logdir			/var/log/%{name}

%description
IP Flow Meter is a bandwidth analysis tool, that measures how much
bandwidth specified hosts use on their Internet link.

%prep
%setup  -q 

%build

%configure
%{__make} CFLAGS="%{rpmcflags}"

gzip -9nf HISTORY TODO

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_initdir}}

%{__make} ROOT=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT%{_initdir}/%{name}

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) %{_initdir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_logdir}
%{_mandir}/man[58]/*
