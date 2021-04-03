#!/bin/sh
CONF=/etc/config/qpkg.conf
QPKG_NAME="TelegramTorrent"
QPKG_NAME2="QPython3"
QPKG_ROOT=`/sbin/getcfg $QPKG_NAME Install_Path -f ${CONF}`
Python_ROOT=`/sbin/getcfg $QPKG_NAME2 Install_Path -f ${CONF}`
	if [ -s $QPKG_ROOT/flag2.txt ]; 
	then
		echo "desactivo BOT"
		#tarea de desactivar Telegram Torrent
		ps | grep BotTorrent | grep -v grep | awk '{ print $1} ' | xargs kill
		
		echo "vacio archivo flag2.txt"
		#vacio archivo flag2.txt para no volver a entrar aqui y hacer reinicios del servicio
		cat /dev/null > $QPKG_ROOT/flag2.txt

		ECHO "Arranco Bot Python"
		#tarea de activar Telegram Torrent en segundo plano
		$Python_ROOT/bin/python3 $QPKG_ROOT/BotTorrent.py &
	fi