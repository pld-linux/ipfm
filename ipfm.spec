Summary:	IP Flow Meter is a bandwidth analysis tool
Name:		ipfm
Version:	0.11.4
Release:	2
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(pl):	Sieciowe/Narzêdzia
Source0:	http://www.via.ecp.fr/~tibob/ipfm/archive/%{name}-%{version}.tgz
Source1:	%{name}.init
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
%{__install} -d $RPM_BUILD_ROOT%{_sbindir}

%{__make} ROOT=$RPM_BUILD_ROOT install

%{__install) %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipfm

%post
/sbin/chkconfig --add ipfm
if [ -f /var/lock/subsys/ipfm ]; then
    /etc/rc.d/init.d/ipfm restart 1>&2
else
    echo "Run \"/etc/rc.d/init.d/ipfm start\" to start ipfm daemon."
fi

%preun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/ipfm ]; then
	/etc/rc.d/init.d/ipfm stop 1>&2
    fi
    /sbin/chkconfig --del ipfm
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/*
%dir /var/log/ipfm/
%{_mandir}/*
