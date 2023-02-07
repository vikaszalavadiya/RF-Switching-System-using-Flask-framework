<?php
#######################################################################
#				PHP Simple Captcha Script
#	Script Url: http://toolspot.org/php-simple-captcha.php
#	Author: Sunny Verma
#	Website: http://toolspot.org
#	License: GPL 2.0, @see http://www.gnu.org/licenses/gpl-2.0.html
########################################################################
session_start();
if(isset($_POST["captcha"])&&$_POST["captcha"]!=""&&$_SESSION["code"]==$_POST["captcha"])
{
	?>
	 <input type="hidden" name="name" value="<?php echo $row['name'] ?>" />
     <?php
header('Location:../sendcontact.php');
//Do you stuff
}
else
{
	echo "<script type=\"text/javascript\">window.alert('you enter wrong code.');
	window.location.href = '../index.html#contact';</script>"; 
	exit;
	echo"<br>";
}
?>
<!--<a href="../contact.html"><button style="width:50px;height:30px;">Back</button></a>-->
