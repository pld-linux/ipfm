# $revision: 1.27 $, $Date: 2004-04-09 15:20:44 $

%bcond_with	mysql	# build with experimental mysql support

Summary:	IP Flow Meter is a bandwidth analysis tool
Summary(pl):	IP Flow Meter - program analizuj±cy wykorzystanie ³±cza
Name:		ipfm
Version:	0.12.0pre1
Release:	2%{?with_mysql:.mysql}
License:	GPL
Group:		Networking/Utilities
Source0:	http://robert.cheramy.net/ipfm/archive/devel/0.12/%{name}-%{version}.tgz
Source1:	%{name}.init
Patch0:		%{name}-mysql.patch
URL:		http://robert.cheramy.net/ipfm/
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libpcap-devel
%{?with_mysql:BuildRequires:	mysql-devel}
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/%{name}
%define		_initdir		/etc/rc.d/init.d
%define		_logdir			/var/log/%{name}

%description
IP Flow Meter is a bandwidth analysis tool, that measures how much
bandwidth specified hosts use on their Internet link.
%{?with_mysql:This version is with experimental mysql support.}

%description -l pl
IP Flow Meter to program analizuj±cy wykorzystanie ³±cza. Mierzy on, w
jakim stopniu poszczególne hosty wykorzystuj± dostêpne ³±cze do
Internetu.
%{?with_mysql:Ta wersja eksperymentalnie obsluguje mysql-a.}

%prep
%setup -q
%{?with_mysql:%patch0 -p1}

%build
%{__autoconf}
%configure
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d}

%{__make} ROOT=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%doc HISTORY TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_logdir}
%{_mandir}/man[58]/*
