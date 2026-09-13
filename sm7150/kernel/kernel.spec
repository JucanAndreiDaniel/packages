%global _tag v7.1_rc3

Name: kernel
ExclusiveArch: aarch64
Version: 7.1.0
Release: 4.davinci%{?dist}
# Full kernel release string as printed by `make kernelrelease`
# (tree Makefile version + EXTRAVERSION + CONFIG_LOCALVERSION=-sm7150)
%global krel %{version}-%{release}-sm7150
Summary: Mainline kernel, modules and headers for Xiaomi Mi 9T / Redmi K20 (davinci).
URL: https://github.com/sm7150-mainline/linux
Source1: %{url}/archive/refs/tags/%{_tag}.tar.gz
# Local config fragment with parent symbols missing from arm64 defconfig
# (without it, olddefconfig silently drops e.g. the UFS storage stack).
Source2: davinci-fixups.config
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
BuildRequires: file
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
in-tree arch/arm64/configs/sm7150.config fragment plus
arch/arm64/configs/efi.config (EFI_ZBOOT so the installed vmlinuz
is a PE-COFF EFI application bootable via systemd-boot) plus the
packaging's davinci-fixups.config (parent symbols missing from
arm64 defconfig, e.g. for the UFS storage stack).

%prep
tar -xzf %{SOURCE1}
# GitHub tag archives don't have a stable top-level dir name across
# tags, so resolve it once and reuse it via a symlink.
ln -sfn linux-* src
cp %{SOURCE2} src/arch/arm64/configs/davinci-fixups.config

%build
cd src
./scripts/kconfig/merge_config.sh -m arch/arm64/configs/defconfig arch/arm64/configs/sm7150.config arch/arm64/configs/efi.config arch/arm64/configs/davinci-fixups.config
make olddefconfig

make EXTRAVERSION="-%{release}" -j%{_smp_build_ncpus} vmlinuz.efi modules dtbs

%install
cd src
kernel_version=$(make EXTRAVERSION="-%{release}" kernelrelease)

mkdir -p %{buildroot}/boot/
cp arch/arm64/boot/vmlinuz.efi %{buildroot}/boot/vmlinuz-$kernel_version
cp System.map %{buildroot}/boot/System.map-$kernel_version
cp .config %{buildroot}/boot/config-$kernel_version

make EXTRAVERSION="-%{release}" modules_install INSTALL_MOD_PATH=%{buildroot}/usr DEPMOD=true
# davinci DTS is split by panel (samsung = tested default, visionox alt).
# NOTE: ostree expects usr/lib/modules/<kver>/devicetree to be a SINGLE
# FILE and tries to checksum-read it, so a devicetree *directory* there
# breaks deployment ("Is a directory"). Ship the multi-DTB layout ostree
# supports instead: a real dtb/ directory, no devicetree entry at all.
mkdir -p %{buildroot}/usr/lib/modules/$kernel_version/dtb
cp arch/arm64/boot/dts/qcom/sm7150-xiaomi-davinci-samsung.dtb arch/arm64/boot/dts/qcom/sm7150-xiaomi-davinci-visionox.dtb %{buildroot}/usr/lib/modules/$kernel_version/dtb/
cp arch/arm64/boot/vmlinuz.efi %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz
# systemd-boot LoadImage() requires PE-COFF. Fail the build early
# instead of shipping an unbootable vmlinuz (e.g. raw Image.gz).
file %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz | grep -q "PE32.*EFI"
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
/boot/System.map-%{krel}
/boot/config-%{krel}
/boot/vmlinuz-%{krel}

%posttrans core
/sbin/depmod -a %{krel}
dracut -f --kver %{krel} /usr/lib/modules/%{krel}/initramfs.img
kernel-install add %{krel} /usr/lib/modules/%{krel}/vmlinuz /usr/lib/modules/%{krel}/initramfs.img


%postun core
kernel-install remove %{krel} /usr/lib/modules/%{krel}/vmlinuz


%package modules
License: GPL-2.0-only
Summary: Mainline kernel, modules and headers for Xiaomi Mi 9T / Redmi K20 (davinci).
Requires: %{name}-core = %{version}-%{release}

%description modules
Mainline kernel fork for Xiaomi Mi 9T / Redmi K20 (davinci, SM7150).

%files modules
/usr/lib/modules/%{krel}/

%package headers
License: GPL-2.0-only
Summary: Mainline kernel headers for Xiaomi Mi 9T / Redmi K20 (davinci).

%description headers
Mainline kernel headers for Xiaomi Mi 9T / Redmi K20 (davinci).

%files headers
/usr/include/

%changelog
%autochangelog
