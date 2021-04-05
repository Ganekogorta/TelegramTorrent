<?php 
session_start();
$archivo="../clave.md5";
$filesize = filesize($archivo);
$password = "";
if ($filesize == 0){
    $password = "7eae385761fcdc3b6ee6e1682efed2b2";
	} else {
	$file = fopen($archivo,"r");
	$password = fgets($file);
	fclose($file);	
	}

if($_POST['password']){
    if(md5($_POST['password']) == $password){
        $_SESSION['password'] = "alm";
    }else{
		echo "<span style='color:red;font-weight:bold;'>La contraseña $password es incorrecta</span>";
    }}
	
if(!$_SESSION['password']){
?>
<center>
<h2><br /><br />Acceso configuraci&oacute;n de Telegram Torrent</h2>
<br />
<form style="margin:12px;" name="form1" method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
<input type="password" name="password">
<input type="submit" name="Submit" value="Entrar"></form>
</center>

<?php 
}else{
    if($_GET['acabar']){
        session_destroy();
		exit("<span style='color:blue;font-weight:bold;'>Te has desconectado, ya puedes cerrar esta ventana</span>");
    }
?>	

<?php
if(isset($_POST['Guardar'])){
 $nombre = "";
  if (!empty($_REQUEST['name'])){
   $nombre = $_REQUEST['name'];
}
$post = "";
if (!empty($_REQUEST['token'])){
 $post = $_REQUEST['token'];
}
$torrent = "";
if (!empty($_REQUEST['torrent'])){
 $torrent = $_REQUEST['torrent'];
}
$pdf = "";
if (!empty($_REQUEST['pdf'])){
 $pdf = $_REQUEST['pdf'];
}
$usuarios = "";
if (!empty($_REQUEST['usuarios'])){
 $usuarios = $_REQUEST['usuarios'];
}
$archivo = "../botcfg.txt";
$file = fopen($archivo,"w");
fwrite($file,"TOKEN = '".$post."'\n"."ruta = '".$torrent."'\n"."rutaPDF = '".$pdf."'\n"."usuarios = {".$usuarios."}\n");
fclose($file);
}
$archivo = "../flag2.txt";
$file = fopen($archivo,"w");
fwrite($file,"toca reiniciar");
fclose($file);


$out = fopen("../BotTorrent.py", "w");
          $in = fopen("../botini.txt", "r");
          while ($line = fgets($in)){
                /*print $file;*/
               fwrite($out, $line);
          }
          $in = fopen("../botcfg.txt", "r");
          while ($line = fgets($in)){
                /*print $file;*/
               fwrite($out, $line);
          }
          fclose($in);
		  $in = fopen("../botfin.txt", "r");
          while ($line = fgets($in)){
                /*print $file;*/
               fwrite($out, $line);
          }
		  fclose($in);
		fclose($out);


$ar = fopen("../botcfg.txt","r") or die("No se pudo abrir el archivo");
$i=0;
while (!feof($ar)){
 $linea = fgets($ar);
 $i = $i + 1 ;
 /*$lineasalto = nl2br($linea);
 echo $lineasalto; */
 if ($i == 1) $valor1 = $linea ;
 if ($i == 2) $valor2 = $linea ;
 if ($i == 3) $valor3 = $linea ;
 if ($i == 4) $valor4 = $linea ;
}
fclose($ar);
$valor1 = substr($valor1, 9);
$valor1 = substr($valor1, 0, -2);
$valor2 = substr($valor2, 8);
$valor2 = substr($valor2, 0, -2);
$valor3 = substr($valor3, 11);
$valor3 = substr($valor3, 0, -2);
$valor4 = substr($valor4, 12);
$valor4 = substr($valor4, 0, -2);
?>

<form method="post" action="">
<center><br /><h3> Definición de  las variables y rutas del Telegram Torrent.</h3>
<br />Token de Telegram:
<br />
<input type="text" name="token" size="60" value="<?php echo $valor1; ?>" />
<br />
<br />Ruta de descarga de archivos .torrent: 
<div style="font-size:14px"> ejemplo:/share/MD0_DATA/Download/Torrents/ </div>
<input type="text" name="torrent" size="60" value="<?php echo $valor2; ?>" />
<br />
<br />Ruta de descarga de archivos .pdf 
<div style="font-size:14px"> ejemplo:/share/MD0_DATA/Download/pdf/</div>
<input type="text" name="pdf" size="60" value="<?php echo $valor3; ?>" />
<br />
<br />Usuarios permitidos:<br />
<div style="font-size:14px"> ejemplo 555666677 : 'usuario1', '12345678' : 'usuario2' </div> 
<input type="text" name="usuarios" size="60" value="<?php echo $valor4; ?>" />
<br/>
<br/>
<input type="submit" name="Guardar" value="Guardar"> 
<br/>
<br/>
<center><h3> Cambio de la clave de acceso.</h3>
<input type="text" name="clave" size="20">
<input type="submit" name="Actualizar" value="Actualizar"> 
<br/>
<a href="<?php echo $_SERVER['PHP_SELF']; ?>?acabar=si">Desconectar</a>
<br />
</center>
</form>

<?php 	
}
?>
<?php
if(isset($_POST['Actualizar'])){
 $nombre = "";
  if (!empty($_REQUEST['clave'])){
   $clave = $_REQUEST['clave'];
}
$clave=md5($clave);
$archivo = "../clave.md5";
$file = fopen($archivo,"w+");
fwrite($file,$clave);
fclose($file);
}
?>
