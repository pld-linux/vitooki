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
Patch0:		gcc.patch
Patch1:		optflags.patch
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
%patch0 -p1
%patch1 -p1

#sed -i -e '/all4itec:/s/ffmpeg//' Makefile # untouched
sed -i -e '/all4itec:/s/lame//' Makefile # untouched
sed -i -e '/all4itec:/s/paragui//' Makefile # untouched
sed -i -e '/all4itec:/s/isomp4lib//' Makefile # untouched
sed -i -e '/all4itec:/s/xvid//' Makefile # unknown
sed -i -e '/all4itec:/s/libdvdcss//' Makefile # untouched
sed -i -e '/all4itec:/s/libdvdread//' Makefile # untouched
sed -i -e '/all4itec:/s/libmatroska//' Makefile
sed -i -e '/all4itec:/s/libebml//' Makefile

install -d 3rdparty/system-libs
mv 3rdparty/{lame,paragui,libmad*,libtheora*,libdvdcss,libdvdread,libmatroska,libebml} 3rdparty/system-libs

# error with UINT64_C symbol
#mv 3rdparty/ffmpeg 3rdparty/system-libs
# need "bitstream/bitstream.h"
#mv 3rdparty/xvidcore* 3rdparty/system-libs

%build
cd 3rdparty/sord
if [ ! -f Makefile ]; then
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
		%{__perl} configure.pl
fi
%{__make}
cd -


cd 3rdparty/ffmpeg
	./configure \
	--enable-pp \
	--enable-gpl \
	--enable-mp3lame \
	--enable-shared \
	--disable-static \
    --cc="%{__cc}" \

#    --extra-cflags="-D_GNU_SOURCE=1 %{rpmcppflags} %{rpmcflags}" \
#    --extra-ldflags="%{rpmcflags} %{rpmldflags}" \

%{__make}
cd -


%{__make} -j1 commonucl vitooki apps \
	PWD=$(pwd) \
	PREFIX=%{_prefix} \
	GCC="%{__cc}" \
	CPP="%{__cxx}" \
	OPT_CFLAGS="%{rpmcflags}" \
	OPT_CPPFLAGS="%{rpmcppflags} -funroll-loops -DVITOOKI_DEBUG_LEVEL=0 -fPIC" \
	xRELEASE_CPPFLAGS="%{rpmcppflags} -funroll-loops -DVITOOKI_DEBUG_LEVEL=0 -fPIC" \
	OPT_LDFLAGS="%{rpmldflags}" \
	SDL_LIBS="" \
	LIBMAD_LIBS="" \
	X11_LIBS="" \
	QT_LIBS="" \
	EXPAT_LIBS="" \
	QTDIR=/usr \
	xFFMPEG="/usr/include" \
	QT_INCLUDES="-I/usr/include/qt" \
	XVIDLIB="-lxvidcore" \
	PARALIB="-lparagui" \
%ifarch %{ix86}
	VITOOKI_BUILD_ARCH=intel32 \
%endif
%ifarch %{x8664}
	VITOOKI_BUILD_ARCH=intel64 \
	EXTRA_FLAGS="-fPIC" \
%endif

%{?with_apidocs:doxygen doxygen.cfg}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGLIST DOCUMENTATION INSTALL TODO
