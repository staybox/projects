<?php
require_once 'swiftmailer/lib/swift_required.php';

//If the form sent
if(isset($_POST['submit'])) {

	//Check name
	if(trim($_POST['contactname']) == '') {
		$hasError = true;
	} else {
		$name = trim($_POST['contactname']);
	}

	//Check theme
	if(trim($_POST['subject']) == '') {
		$hasError = true;
	} else {
		$subject = trim($_POST['subject']);
	}

	//Check EMAIL
	if(trim($_POST['email']) == '')  {
		$hasError = true;
	} else if (!eregi("^[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]{2,4}$", trim($_POST['email']))) {
		$hasError = true;
	} else {
        $emailOfSender = trim($_POST['email']);
	}

	//Check text in the message box
	if(trim($_POST['message']) == '') {
		$hasError = true;
	} else {
		if(function_exists('stripslashes')) {
			$comments = stripslashes(trim($_POST['message']));
		} else {
			$comments = trim($_POST['message']);
		}
	}

	//If there are no errors - send an email.
	if(!isset($hasError)) {

		$myEmail = ''; // email address of the manager
        $myPass = '';
		$body = "Name: $name \n\nEmail: $emailOfSender \n\nSubject: $subject \n\nComments:\n $comments";


        $transport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, "ssl")
            ->setUsername($myEmail)
            ->setPassword($myPass);

        $mailer = Swift_Mailer::newInstance($transport);

        $message = Swift_Message::newInstance($subject)
            ->setFrom(array($myEmail => 'INFO'))
            ->setTo(array($myEmail))
            ->setBody($body);

        $result = $mailer->send($message);


	$emailSent = true;

	}
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">

<head>
	<title>Abuna Faraj pilgrim house</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta http-equiv="Content-Style-Type" content="text/css" />

<script src="jquery.min.js" type="text/javascript"></script>
<script src="jquery.validate.pack.js" type="text/javascript"></script>

<script type="text/javascript">
$(document).ready(function(){
	$("#contactform").validate();
});
</script>

<style type="text/css">
body {
	font-family:Arial, Tahoma, sans-serif;
}
#contact-wrapper {
	width:530px;
	border:1px solid #e2e2e2;
	background:#D9EDF7;
	padding:20px;
}
#contact-wrapper div {
	clear:both;
	margin:1em 0;
}
#contact-wrapper label {
	display:block;
	float:none;
	font-size:16px;
	width:auto;
}
form#contactform input {
	border-color:#B7B7B7 #E8E8E8 #E8E8E8 #B7B7B7;
	border-style:solid;
	border-width:1px;
	padding:5px;
	font-size:16px;
	color:#333;
}
form#contactform textarea {
	font-family:Arial, Tahoma, Helvetica, sans-serif;
	font-size:100%;
	padding:0.6em 0.5em 0.7em;
	border-color:#B7B7B7 #E8E8E8 #E8E8E8 #B7B7B7;
	border-style:solid;
	border-width:1px;
}
</style>
</head>

<body>
	<div id="contact-wrapper">

	<?php if(isset($hasError)) { //If errors ?>
		<p class="error">Check please the fields</p>
	<?php } ?>

	<?php if(isset($emailSent) && $emailSent == true) { //If message sent ?>
		<p><strong>Email sent!</strong></p>
		<p>Thank you  <strong><?php echo $name;?></strong> for your reservation! Your message has been sent. We will write you in soon to confirm!</p>
	<?php } ?>

	<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>" id="contactform">
		<div>
		    <label for="name"><strong>Name:</strong></label>
			<input type="text" size="50" name="contactname" id="contactname" value="" class="required" />
		</div>

		<div>
			<label for="email"><strong>Email:</strong></label>
			<input type="text" size="50" name="email" id="email" value="" class="required email" />
		</div>

		<div>
			<label for="subject"><strong>Theme:</strong></label>
			<input type="text" size="50" name="subject" id="subject" value="" class="required" />
		</div>

		<div>
			<label for="message"><strong>Message:</strong></label>
			<textarea rows="5" cols="50" name="message" id="message" class="required"></textarea>
		</div>
	    <input type="submit" value="Send Message" name="submit" />
	</form>
	</div>
</body>
</html>
