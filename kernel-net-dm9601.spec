#
# Conditionan build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Davicom DM9601 chipset driver for Linux
Summary(pl.UTF-8):   Sterownik dla urządzeń na chipsecie Davicom DM9601
Name:		kernel%{_alt_kernel}-net-dm9601
Version:	1.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	dm9601.tar.gz
# Source0-md5:	ef0e470a4b8c019fe4bb3aa65201d2fd
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(dm9601)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the ethernet network
adapters built on Davicom DM9601 chipset.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
zbudowanych na układzie Davicom DM9601.

%package -n kernel%{_alt_kernel}-smp-net-dm9601
Summary:	Davicom DM9601 chipset driver for Linux
Summary(pl.UTF-8):   Sterownik dla urządzeń na chipsecie Davicom DM9601
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(dm9601)

%description -n kernel%{_alt_kernel}-smp-net-dm9601
This package contains the Linux SMP driver for the ethernet network
adapters built on Davicom DM9601 chipset.

%description -n kernel%{_alt_kernel}-smp-net-dm9601 -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
zbudowanych na układzie Davicom DM9601.

%prep
%setup -q -n 2.6.18
cat > Makefile <<'EOF'
obj-m := dm9601.o
EOF

%build
%build_kernel_modules -C . -m dm9601

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m dm9601 -d kernel/drivers/net -n dm9601 -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-dm9601
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-dm9601
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc readme.txt
/etc/modprobe.d/%{_kernel_ver}/dm9601.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/dm9601*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-dm9601
%defattr(644,root,root,755)
%doc readme.txt
/etc/modprobe.d/%{_kernel_ver}smp/dm9601.conf
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/dm9601*.ko*
%endif
