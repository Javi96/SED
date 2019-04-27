SSHPASS=raspberry sshpass -e sftp -oBatchMode=no -b - pi@192.168.0.24 << ! 
cd /ruta/archivo/remoto/
lcd /ruta/archivo/local/
get nombreArchivoRemoto nombreConElQueSeGuardaLocal
bye
!
