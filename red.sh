SSHPASS=raspberry sshpass -e sftp -oBatchMode=no -b - pi@192.168.43.210 << ! 
cd /home/pi/db/
lcd /home/pi/db/
get localhost.txt 210.txt
bye
!
SSHPASS=raspberry sshpass -e sftp -oBatchMode=no -b - pi@192.168.43.33 << ! 
cd /home/pi/db/
lcd /home/pi/db/
get localhost.txt 33.txt
bye
!