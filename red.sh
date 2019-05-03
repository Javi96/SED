SSHPASS=raspberry sshpass -e sftp -oBatchMode=no -b - pi@192.168.43.33 << ! 
cd /home/pi/Desktop/github/SED-PROYECTO/db
lcd /home/pi/Desktop/github/SED-PROYECTO/db
get localhost.txt 33.txt
bye
!
