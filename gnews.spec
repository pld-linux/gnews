Summary:	Gnome Panel applet that displays scrolling news headlines
Name:		gnews
Version:	0.0.5
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	ftp://gnews.sourceforge.net/pub/devel/%{name}/%{name}-%{version}.tar.gz
URL:		http://gnews.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

Requires:	libghttp
Requires:	gnome-core >= 1.1.2
Requires:	gdk-pixbuf >= 0.7.0

%define		_prefix		/usr/X11R6

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on Open Source software.
The gnews package provides a Panel applet which displays news
headlines from well known sites.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

##############################################################################
##
function ProcessLang() {
 # rpm provides a handy scriptlet to do the locale stuff lets use that.
 if [ -f %{_libdir}/rpm/find-lang.sh ] ; then
  %{_libdir}/rpm/find-lang.sh $RPM_BUILD_ROOT %name
  sed "s:(644, root, root, 755):(444, bin, bin, 555):" %{name}.lang >tmp.lang && mv tmp.lang %{name}.lang
  if [ -f %{name}.files ] ; then
    cat %{name}.files %{name}.lang >tmp.files && mv tmp.files %{name}.files
  fi
 fi
}
function ProcessBin() {
  # Gather up all the executable files. Stripping if requested.
  # This will not recurse.
  if [ -d $RPM_BUILD_ROOT%{_bindir} ] ; then
    echo "%defattr (0555, bin, bin)" >>%{name}.files
    find $RPM_BUILD_ROOT%{_bindir} -type f -print | sed "s:^$RPM_BUILD_ROOT::g" >>%{name}.files
  fi
}

function ProcessLib() {
  # Gather up any libraries.
  # Usage: ProcessLib <dir> <type> <output file>
  # Type is either 'runtime' or 'devel'
  if [ -d $1 ] ; then
    echo "%defattr (0555, bin, bin)" >>$3
    case "$2" in
      runtime)
       # Grab runtime libraries
       find $1 -name "*.so.*" -print | sed "s:^$RPM_BUILD_ROOT::g" >>$3
       ;;
      devel)
       find $1 -name "*.so" -print | sed "s:^$RPM_BUILD_ROOT::g" >>$3
       find $1 -name "*.la" -print | sed "s:^$RPM_BUILD_ROOT::g" >>$3
       find $1 -name "*.a" -print | sed "s:^$RPM_BUILD_ROOT::g" >>$3
       find $1 -name "*.sh" -print | sed "s:^$RPM_BUILD_ROOT::g" >>$3
       ;;
    esac
   fi
}
function ProcessDir() {
  # Build a list of files in the specified dir sticking
  # a %defattr line as specified in front of the mess. This is intended
  # for normal dirs. Use ProcessLib for library dirs
  # for include dirs. Appending to <output file>.
  # This will recurse.
  #
  # Usage: ProcessDir <dir> <output file> <attr>
  #
  if [ -d $1 ] ; then
   if [ ! -z "$3" ] ; then
     echo "%defattr ($3)" >>$2
   fi
   echo "*** Processing $1"
   find $1 -type f -print | sed "s:^$RPM_BUILD_ROOT::g" >>$2
  fi
}

function BuildFiles() {
  ProcessBin
  ProcessLang
  for i in `find $RPM_BUILD_ROOT%{_datadir} -maxdepth 1 -type d -print | \
     sed "s:^$RPM_BUILD_ROOT%{_datadir}::g"` ; do
    echo $i
    case $i in
     /applets|/asclock|/clockmail|/geyes|/gnome|/gweather|/odometer|/sound-monitor|/pixmaps|/tickastat|/xmodmap)

         ProcessDir $RPM_BUILD_ROOT%{_datadir}$i %{name}.files "0444, bin, bin, 0555"
         ;;
     *)
         ;;
   esac
  done
ProcessDir $RPM_BUILD_ROOT%{_sysconfdir} %{name}.files "0444, bin, bin, 0555"
  ProcessLib $RPM_BUILD_ROOT%{_libdir} runtime %{name}.files
}

BuildFiles

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
