# $revision: 1.27 $, $Date: 2010-06-08 08:07:41 $
#
# Conditional build:
%bcond_with	mysql	# build with experimental MySQL support
#
%define		snap	rc1

Summary:	IP Flow Meter is a bandwidth analysis tool
Summary(pl.UTF-8):	IP Flow Meter - program analizujący wykorzystanie łącza
Name:		ipfm
Version:	0.12.0
Release:	0.%{snap}%{?with_mysql:.mysql}.1
Epoch:		1
License:	GPL
Group:		Networking/Utilities
Source0:	http://robert.cheramy.net/ipfm/archive/%{name}-%{version}%{snap}.tgz
# Source0-md5:	46925af88fb88888cbbdc278b340f5d6
Source1:	%{name}.init
Patch0:		%{name}-mysql.patch
Patch1:		%{name}-configure.in.patch
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
%{?with_mysql:This version is with experimental MySQL support.}

%description -l pl.UTF-8
IP Flow Meter to program analizujący wykorzystanie łącza. Mierzy on, w
jakim stopniu poszczególne hosty wykorzystują dostępne łącze do
Internetu.
%{?with_mysql:Ta wersja eksperymentalnie obsługuje MySQL-a.}

%prep
%setup -q -n %{name}-%{version}%{snap}
%{?with_mysql:%patch0 -p1}
%patch1 -p0

%build
%{__autoconf}
%configure
%{__make} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d}

%{__make} install \
	ROOT=$RPM_BUILD_ROOT

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
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_logdir}
%{_mandir}/man[58]/*
