#
# Conditional build:
%bcond_with	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	ViTooKi - The Video ToolKit
Name:		vitooki
Version:	0.1
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	%{name}-20100804.tar.bz2
# Source0-md5:	-
URL:		http://vitooki.sourceforge.net/
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	nasm
BuildRequires:	openssl-devel
BuildRequires:	qt-devel
BuildRequires:	slang-devel
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Video-Toolkit is a operating system independent, powerful
high-level C++ multimedia library developed to simplify the
implementation of multimedia applications.

%prep
%setup -q -n %{name}

sed -i -e '/all4itec:/s/ffmpeg//' Makefile # untouched
sed -i -e '/all4itec:/s/lame//' Makefile # untouched
sed -i -e '/all4itec:/s/paragui//' Makefile # untouched
sed -i -e '/all4itec:/s/isomp4lib//' Makefile # untouched
sed -i -e '/all4itec:/s/xvid//' Makefile # unknown
sed -i -e '/all4itec:/s/libdvdcss//' Makefile # untouched
sed -i -e '/all4itec:/s/libdvdread//' Makefile # untouched
sed -i -e '/all4itec:/s/libmatroska//' Makefile
sed -i -e '/all4itec:/s/libebml//' Makefile

%build
cd 3rdparty/sord
if [ ! -f Makefile ]; then
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
		%{__perl} configure.pl
fi
%{__make}
cd -

%{__make} -j1 commonucl vitooki \
	PWD=$(pwd) \
	CPP="%{__cxx}" \
	GCC="%{__cc}" \
	PREFIX=%{_prefix} \
	SDL_LIBS=%{_libdir} \
%ifarch %{ix86}
	VITOOKI_BUILD_ARCH=intel32 \
%endif
%ifarch %{x8664}
	VITOOKI_BUILD_ARCH=intel64 \
%endif

%{?with_apidocs:doxygen doxygen.cfg}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGLIST DOCUMENTATION INSTALL TODO
