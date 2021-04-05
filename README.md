# TelegramTorrent
Para hacer descargas de archivos .torrent y PDF a la nas de QNAP desde Telegram usando su api

En la carpeta build están los instaladores para QNAP

The following instructions can help you to build and use this QPKG.

### Setup QDK Environment
Before start to develop your QPKG or use this example, NAS should already setup the QDK environment:

In QTS Desktop, open **App Center**.

Search **QDK** and install the latest version.

### Build
Upload this project to one of your NAS folder.

Login to QNAP NAS and execute **qbuild** command to build this qpkg.


```

### Installation

After successfully build QPKG.

Download the corresponding QPKG file in **build/** folder to your computer. (depends on the architecture of your QNAP NAS model)

In QTS Desktop, open **App Center**.

Then manual Install the QPKG.

Now you can test this example QPKG and start to develop your own.
