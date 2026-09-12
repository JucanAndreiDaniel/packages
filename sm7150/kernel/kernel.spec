%global _tag v7.1_rc3

Name: kernel
ExclusiveArch: aarch64
Version: 7.1.3
Release: 1.davinci%{?dist}
Summary: Mainline kernel, modules and headers for Xiaomi Mi 9T / Redmi K20 (davinci).
URL: https://github.com/sm7150-mainline/linux
Source1: %{url}/archive/refs/tags/%{_tag}.tar.gz
License: GPL-2.0-only

BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: zstd
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: glibc-static
BuildRequires: rsync
BuildRequires: opencsd-devel >= 1.0.0
BuildRequires: openssl-devel

Requires: dracut
Requires: bash
Requires: coreutils
Requires: systemd
Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-modules = %{version}-%{release}

%description
Mainline kernel fork for Xiaomi Mi 9T / Redmi K20 (davinci, SM7150).
Config is generated from upstream defconfig merged with the
in-tree arch/arm64/configs/sm7150.config fragment.

%prep
tar -xzf %{SOURCE1}
# GitHub tag archives don't have a stable top-level dir name across
# tags, so resolve it once and reuse it via a symlink.
ln -sfn linux-* src

%build
cd src
./scripts/kconfig/merge_config.sh -m arch/arm64/configs/defconfig arch/arm64/configs/sm7150.config
make olddefconfig

make EXTRAVERSION="-%{release}" -j%{_smp_build_ncpus} Image.gz modules dtbs

%install
cd src
kernel_version=$(make EXTRAVERSION="-%{release}" kernelrelease)

mkdir -p %{buildroot}/boot/
mkdir -p %{buildroot}/usr/lib/modules/$kernel_version/devicetree
cp arch/arm64/boot/Image.gz %{buildroot}/boot/vmlinuz-$kernel_version
cp System.map %{buildroot}/boot/System.map-$kernel_version
cp .config %{buildroot}/boot/config-$kernel_version

make EXTRAVERSION="-%{release}" modules_install INSTALL_MOD_PATH=%{buildroot}/usr DEPMOD=true
# davinci DTS is split by panel (samsung = tested default, visionox alt)
cp arch/arm64/boot/dts/qcom/sm7150-xiaomi-davinci-samsung.dtb arch/arm64/boot/dts/qcom/sm7150-xiaomi-davinci-visionox.dtb %{buildroot}/usr/lib/modules/$kernel_version/devicetree
ln -s ./devicetree %{buildroot}/usr/lib/modules/$kernel_version/dtb
cp arch/arm64/boot/Image.gz %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz
make EXTRAVERSION="-%{release}" headers_install INSTALL_HDR_PATH=%{buildroot}/usr
rm -f %{buildroot}/usr/lib/modules/$kernel_version/build
rm -f %{buildroot}/usr/lib/modules/$kernel_version/source

%files


%package core
License: GPL-2.0-only
Summary: Mainline kernel, modules and headers for Xiaomi Mi 9T / Redmi K20 (davinci).


%description core
Mainline kernel fork for Xiaomi Mi 9T / Redmi K20 (davinci, SM7150).

%files core
/boot/System.map-%{version}-%{release}
/boot/config-%{version}-%{release}
/boot/vmlinuz-%{version}-%{release}

%posttrans core
/sbin/depmod -a %{version}-%{release}
dracut -f --kver %{version}-%{release} /usr/lib/modules/%{version}-%{release}/initramfs.img
kernel-install add %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz /usr/lib/modules/%{version}-%{release}/initramfs.img


%postun core
kernel-install remove %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz


%package modules
License: GPL-2.0-only
Summary: Mainline kernel, modules and headers for Xiaomi Mi 9T / Redmi K20 (davinci).
Requires: %{name}-core = %{version}-%{release}

%description modules
Mainline kernel fork for Xiaomi Mi 9T / Redmi K20 (davinci, SM7150).

%files modules
/usr/lib/modules/%{version}-%{release}/

%package headers
License: GPL-2.0-only
Summary: Mainline kernel headers for Xiaomi Mi 9T / Redmi K20 (davinci).

%description headers
Mainline kernel headers for Xiaomi Mi 9T / Redmi K20 (davinci).

%files headers
/usr/include/

%changelog
%autochangelog
