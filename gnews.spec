Summary:	Gnome Panel applet that displays scrolling news headlines
Summary(pl):	Applet dla GNOME wyświetlający wiadomości
Name:		gnews
Version:	0.1.3
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL:		http://gnews.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-libs-devel >= 1.0.54
BuildRequires:	gnome-core-devel
BuildRequires:	libghttp-devel
BuildRequires:	gdk-pixbuf >= 0.7.0
BuildRequires:	ORBit-devel
BuildRequires:	gtk+-devel
BuildRequires:	XFree86-devel
BuildRequires:	db3-devel
BuildRequires:	glib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/X11/GNOME
%define         _localstatedir  /var

%description
The gnews package provides a Panel applet which displays news
headlines from well known sites.

%description -l pl
Pakiet gnews dostarcza applet umożliwiający wyświetlanie nowinek z
dobrze znanych serwisów sieciowych.

%prep
%setup -q

%build
rm -f config.cache
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
%configure \
	--with-gnome=%{_prefix} \
	--with-gtk-prefix=%{_prefix} \
	--with-gtk-exec-prefix=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_pixmapsdir}/*
%{_datadir}/applets/*/*.desktop
%{_sysconfdir}/*/*/*.gnorba
