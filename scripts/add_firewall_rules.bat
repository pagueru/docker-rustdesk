netsh advfirewall firewall add rule name="RustDesk Self-Host TCP (21115-21119)" dir=in action=allow protocol=tcp localport=21115-21119 remoteip=any profile=any
netsh advfirewall firewall add rule name="RustDesk Self-Host UDP (21116)" dir=in action=allow protocol=udp localport=21116 remoteip=any profile=any
pause