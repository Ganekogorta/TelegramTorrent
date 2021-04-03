<?php
if(isset($_POST['Guardar'])){
 $nombre = "";
  if (!empty($_REQUEST['clave'])){
   $clave = $_REQUEST['clave'];
}
$clave=md5($clave);
$archivo = "clave.md5";
$file = fopen($archivo,"w+");
fwrite($file,$clave);
fclose($file);
}
?>

<form method="post" action="">
<center><br><h3> Cambio de la clave de acceso.</h3>
<br>
<input type="text" name="clave" size="20">
<br/>
<br/>
<input type="submit" name="Guardar" value="Guardar"> 
<br/>
<br/>
<br>
<a href='index.php'>Volver</a>
</center>
</form>

