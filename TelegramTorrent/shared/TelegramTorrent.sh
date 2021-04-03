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
		chmod 660 $QPKG_ROOT/flag2.txt
		
		# creo enlace simbolico a la página web
		ln -s $QPKG_ROOT/web /home/Qhttpd/Web/TelegramTorrent
		# creo enlace simbólico al archivo de configuración
		ln -s $QPKG_ROOT/botcfg.txt /home/Qhttpd/Web/TelegramTorrent/botcfg.txt
		chmod 660 $QPKG_ROOT/botcfg.txt
		# creo enlace simbólico al archivo flag2.txt
		ln -s $QPKG_ROOT/flag2.txt /home/Qhttpd/Web/TelegramTorrent/flag2.txt
		chmod 660 $QPKG_ROOT/flag2.txt
		# creo enlace simbólico al inicio del archivo de configuración
		ln -s $QPKG_ROOT/botini.txt /home/Qhttpd/Web/TelegramTorrent/botini.txt
		# creo enlace simbólico al final archivo de configuración
		ln -s $QPKG_ROOT/botfin.txt /home/Qhttpd/Web/TelegramTorrent/botfin.txt
		# creo enlace simbólico al archivo de configuración
		ln -s $QPKG_ROOT/BotTorrent.py /home/Qhttpd/Web/TelegramTorrent/BotTorrent.py
		chmod 660 $QPKG_ROOT/BotTorrent.py
	else
	    # creo enlace simbolico a la página web
		ln -s $QPKG_ROOT/web /home/Qhttpd/Web/TelegramTorrent
		# creo enlace simbólico al archivo de configuración
		ln -s $QPKG_ROOT/botcfg.txt /home/Qhttpd/Web/TelegramTorrent/botcfg.txt
		chmod 660 $QPKG_ROOT/botcfg.txt
		# creo enlace simbólico al archivo flag2.txt
		ln -s $QPKG_ROOT/flag2.txt /home/Qhttpd/Web/TelegramTorrent/flag2.txt
		chmod 660 $QPKG_ROOT/flag2.txt
		# creo enlace simbólico al inicio del archivo de configuración
		ln -s $QPKG_ROOT/botini.txt /home/Qhttpd/Web/TelegramTorrent/botini.txt
		# creo enlace simbólico al final archivo de configuración
		ln -s $QPKG_ROOT/botfin.txt /home/Qhttpd/Web/TelegramTorrent/botfin.txt
		# creo enlace simbólico al archivo de configuración
		ln -s $QPKG_ROOT/BotTorrent.py /home/Qhttpd/Web/TelegramTorrent/BotTorrent.py
		chmod 660 $QPKG_ROOT/BotTorrent.py
		
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
	#elimino los enlaces simbólicos para que no se pueda entrar en la web de configuración
	rm /home/Qhttpd/Web/TelegramTorrent/botcfg.txt
	rm /home/Qhttpd/Web/TelegramTorrent/botini.txt
	rm /home/Qhttpd/Web/TelegramTorrent/botfin.txt
	rm /home/Qhttpd/Web/TelegramTorrent/BotTorrent.py
    rm /home/Qhttpd/Web/TelegramTorrent
	
	#eliminar lineas de tareas autorranque en crontab
    sed -i '/comprobador.sh/d' /etc/config/crontab
	#tarea de activar crontab editado
	crontab  /etc/config/crontab
	/etc/init.d/crond.sh restart
	
	#tarea de desactivar Telegram Torrent
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
