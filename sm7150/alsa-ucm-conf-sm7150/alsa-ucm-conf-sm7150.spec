Name: alsa-ucm-conf-sm7150
Version: 1
Release: 1
Summary: ALSA UCM configuration for Xiaomi Mi 9T / Redmi K20 (davinci)
Source1: Xiaomi Mi 9T.conf
Source2: HiFi_davinci.conf
License: Unknown
BuildArch: noarch

Requires: alsa-ucm

%description
ALSA Use Case Manager configuration for SM7150-based Xiaomi Mi 9T /
Redmi K20 (davinci). Card-name symlinks may need adjusting to match
/proc/asound/cards on the device (see TODO in HiFi_davinci.conf).

%install
install -Dm644 "%{SOURCE1}" "%{buildroot}%{_datadir}/alsa/ucm2/conf.d/sm8250/Xiaomi Mi 9T.conf"
install -Dm644 "%{SOURCE2}" "%{buildroot}%{_datadir}/alsa/ucm2/Qualcomm/sm8250/HiFi_davinci.conf"

ln -s "Xiaomi Mi 9T.conf" "%{buildroot}%{_datadir}/alsa/ucm2/conf.d/sm8250/Xiaomi-Mi9T-davinci.conf"

%files
%{_datadir}/alsa/ucm2/conf.d/sm8250/Xiaomi\ Mi\ 9T.conf
%{_datadir}/alsa/ucm2/Qualcomm/sm8250/HiFi_davinci.conf
%{_datadir}/alsa/ucm2/conf.d/sm8250/Xiaomi-Mi9T-davinci.conf

%changelog
%autochangelog
