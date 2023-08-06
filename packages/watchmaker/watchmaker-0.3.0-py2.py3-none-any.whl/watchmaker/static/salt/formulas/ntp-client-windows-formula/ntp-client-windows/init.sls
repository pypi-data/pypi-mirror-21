{%- from "ntp-client-windows/map.jinja" import time with context %}

w32tm_specialpollinterval:
  reg.present:
    - name: 'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient\SpecialPollInterval'
    - value: {{ time.specialpollinterval }}
    - vtype: 'REG_DWORD'
    - reflection: False
    - watch_in:
      - service: w32tm_service

w32tm_ntpserver:
  reg.present:
    - name: 'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters\NtpServer'
    - value: {{ time.servers }}
    - vtype: 'REG_SZ'
    - reflection: False
    - watch_in:
      - service: w32tm_service

w32tm_type:
  reg.present:
    - name: 'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters\Type'
    - value: 'NTP'
    - vtype: 'REG_SZ'
    - reflection: False
    - watch_in:
      - service: w32tm_service

w32tm_service:
  service.running:
    - name: 'W32Time'
    - onchanges_in:
      - cmd: w32tm_resync

w32tm_resync:
  cmd.run:
    - name: 'w32tm /config /update'
