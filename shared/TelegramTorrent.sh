#!/bin/sh
CONF=/etc/config/qpkg.conf
QPKG_NAME="TelegramTorrent"
QPKG_ROOT=`/sbin/getcfg $QPKG_NAME Install_Path -f ${CONF}`
APACHE_ROOT=`/sbin/getcfg SHARE_DEF defWeb -d Qweb -f /etc/config/def_share.info`
export QNAP_QPKG=$QPKG_NAME
directoriox="$(dirname -- $(readlink -fn -- "$0"; echo x))"
directorio="${directoriox%x}"
dirQPython=`getcfg QPython3 Install_Path -f /etc/config/qpkg.conf`
sisvol=`getcfg SHARE_DEF defVolMP -f /etc/config/def_share.info`
echo Donde estoy ahora $directorio 
echo Ruta de QPython3 = $dirQPython
echo Volumen de sistema = $sisvol

case "$1" in
  start)
    ENABLED=$(/sbin/getcfg $QPKG_NAME Enable -u -d FALSE -f $CONF)
    if [ "$ENABLED" != "TRUE" ]; then
        echo "$QPKG_NAME ha sido desactivado."
        exit 1
    fi
    : ADD START ACTIONS HERE
	#compruebo si NO existe flag.txt es el primer arranque. No inicio bot por no tener configuracion correcta
	if [ ! -f $QPKG_ROOT/flag.txt ];
	then
		# creo el archivo flag para saber que 
		touch $QPKG_ROOT/flag.txt
		#instalo pip
		sudo $dirQPython/bin/python3 $QPKG_ROOT/get-pip.py
		#instalo pyTelegramAPI
		sudo $dirQPython/bin/python3 -m pip install pyTelegramBotAPI
		#creo archivo flag2.txt como señal de futuros reinicios del servicio
		touch $QPKG_ROOT/flag2.txt
		#asigno permisos para que el usuario httpdusr pueda modificarlos
		chmod 666 $QPKG_ROOT/flag2.txt
		chmod 666 $QPKG_ROOT/botcfg.txt
		chmod 666 $QPKG_ROOT/BotTorrent.py
	else
	    #asigno permisos para que el usuario httpdusr pueda modificarlos
		chmod 666 $QPKG_ROOT/flag2.txt
		chmod 666 $QPKG_ROOT/botcfg.txt
		chmod 666 $QPKG_ROOT/BotTorrent.py
		#tarea de activar Telegram Torrent en segundo plano
		$dirQPython/bin/python3 $QPKG_ROOT/BotTorrent.py &
	fi
	
	#tarea de comprobacion de flag para reiniciar archivo
	echo -e "*/1 * * * * $QPKG_ROOT/comprobador.sh">> /mnt/HDA_ROOT/.config/crontab
	#tarea de activar crontab editado
	crontab  /etc/config/crontab
	/etc/init.d/crond.sh restart
	

    ;;

  stop)
    : ADD STOP ACTIONS HERE
		
	#eliminar lineas de tareas autorranque en crontab
    sed -i '/comprobador.sh/d' /etc/config/crontab
	#tarea de activar crontab editado
	crontab  /etc/config/crontab
	/etc/init.d/crond.sh restart
	
	#tarea de desactivación de Telegram Torrent
    ps | grep BotTorrent | grep -v grep | awk '{ print $1} ' | xargs kill
	;;

  restart)
    $0 stop
    $0 start
    ;;

  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

exit 0
