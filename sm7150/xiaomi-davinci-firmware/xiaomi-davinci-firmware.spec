%global _commit 7c25d3fe5883f25f8f068e89c6442b4c608835f0
# modem blobs are prebuilt ELF files: don't autogenerate
#Requires/Provides from their NEEDED entries (see pipa firmware spec)
%global __requires_exclude ^.*\\.so.*$
%global __provides_exclude ^.*\\.so.*$
%global _firmwaredir %{_prefix}/lib/firmware
%global _qcomdir %{_firmwaredir}/qcom/sm7150

Name: xiaomi-davinci-firmware
Version: 1
Release: 2%{?dist}
Summary: Firmware for Xiaomi Mi 9T / Redmi K20 (davinci)
URL: https://github.com/sm7150-mainline/firmware-xiaomi-davinci
Source0: %{url}/archive/%{_commit}/firmware-xiaomi-davinci-%{_commit}.tar.gz
License: Unknown
BuildArch: noarch
Requires: qcom-firmware

%description
Nonfree firmware blobs for Xiaomi Mi 9T / Redmi K20 (davinci):
adsp/cdsp/modem/venus/ipa/a615-zap/wlanmdsp plus modem mcfg data
and ssc sensor configs.
The kernel requests them as qcom/sm7150/davinci/*, the repo ships
them as qcom/sm7150/xiaomi/davinci/*, so both paths are provided
(the short path is a symlink).

%prep
%autosetup -n firmware-xiaomi-davinci-%{_commit}

%install
# firmware blobs (repo already carries a usr/ tree)
cp -a usr %{buildroot}/
# compat path expected by sm7150-xiaomi-davinci.dts firmware-name entries
mkdir -p %{buildroot}%{_qcomdir}
ln -s xiaomi/davinci %{buildroot}%{_qcomdir}/davinci
find %{buildroot}%{_firmwaredir} -type f -exec chmod 0644 {} \;
find %{buildroot}%{_prefix}/share/qcom -type f -exec chmod 0644 {} \;

%files
%{_firmwaredir}/qcom/sm7150/
%{_prefix}/share/qcom/

%changelog
%autochangelog
