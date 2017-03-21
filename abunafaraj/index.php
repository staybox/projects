<?php
require_once 'libs/swiftmailer/swiftmailer/lib/swift_required.php';

//If the form sent
if(isset($_POST['submit'])) {

    //Check name
    if(trim($_POST['contactname']) == '') {
        $hasError = true;
    } else {
        $name = trim($_POST['contactname']);
    }

    //Check Family Name
    if(trim($_POST['FamilyName']) == '') {
        $hasError = true;
    } else {
        $FamilyName = trim($_POST['FamilyName']);
    }

    //Check EMAIL
    if(trim($_POST['email']) == '')  {
        $hasError = true;
    } else if (!eregi("^[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]{2,4}$", trim($_POST['email']))) {
        $hasError = true;
    } else {
        $emailOfSender = trim($_POST['email']);
    }


    $phone = trim($_POST['phone']);
    $city = trim($_POST['city']);
    $country = trim($_POST['country']);





    //Check $startDate
    if(trim($_POST['startDate']) == '') {
        $hasError = true;
    } else {
        $startDate = trim($_POST['startDate']);
    }

    //Check $endDate
    if(trim($_POST['endDate']) == '') {
        $hasError = true;
    } else {
        $endDate = (trim($_POST['endDate']));
    }
    $nights = round((strtotime($endDate) - strtotime($startDate))/(60*60*24),0);

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


    $price_a1 = 230; //single
    $price_a2 = 140; //double
    $price_a3 = 120; //triple or quadruple
    $price_am = 65;  //meal

    //discout 50% 4-6 years old
    $price_c2_50 = $price_a2*0.5;
    $price_c3_50 = $price_a3*0.5;
    $price_cm_50 = $price_am*0.5;

    //discout 25% 7-12 years old
    $price_c2_25 = $price_a2*0.75;
    $price_c3_25 = $price_a3*0.75;
    $price_cm_25 = $price_am*0.75;
    $price_free = 0;


    $adults1 = intval(trim($_POST['adults1']));
    $adults2 = intval(trim($_POST['adults2']));
    $adults3 = intval(trim($_POST['adults3']));
    $adults_m = intval(trim($_POST['adults_meal']));
    $children2_50 = intval(trim($_POST['children2_50'])); // children 4-6 years old in double
    $children3_50 = intval(trim($_POST['children3_50'])); // children 4-6 years old in triple or quadruple
    $children_m_50 = intval(trim($_POST['children_meal_50'])); // children 4-6 years old - meal
    $children2_25 = intval(trim($_POST['children2_25'])); // children 7-12 years old in double
    $children3_25 = intval(trim($_POST['children3_25'])); // children 7-12 years old in triple or quadruple
    $children_m_25 = intval(trim($_POST['children_meal_25'])); // children 7-12 years old - meal
    $price_single = $price_a1 * $adults1*$nights;
    $price_double = ($price_a2*$adults2 + $price_c2_50*$children2_50+$price_c2_25*$children2_25)*$nights;
    $price_triple = ($price_a3*$adults3 + $price_c3_50*$children3_50+$price_c3_25*$children3_25)*$nights;
    $price_meal = ($price_am*$adults_m + $price_cm_50*$children_m_50+$price_cm_25*$children_m_25)*$nights;

    $price_total = $price_single+$price_double+$price_triple+$price_meal;


    $html_in_email_1 = '<html><body>';
    $html_in_email_2 = '</html></body>';
    $br = '<br>';
    $table1 = "<table width=\"80%\"><tr><td>";
    $table2 = "</table>";
    $tr1 = "<tr>";
    $tr2 = "</tr>";
    $td1 = "<td>";
    $td2 = "</td>";
    $p1 = "<p>";
    $p2 = "</p>";
    $th1 = "<th>";
    $th2 = "</th>";
    $thead1 = "<thead>";
    $thead2 = "</thead>";
    $tbody1 = "<tbody>";
    $tbody2 = "</tbody>";

    //If there are no errors - send an email.
    if(!isset($hasError)) {
        $subject = 'Reservation on '.$startDate;
        $myEmail = ''; // email address of the manager
        $myPass = '';
        $body = "
        $html_in_email_1
        IDENTIFICATION $br
        $table1 $tr1 $td1
        Name: $name $br
        Family name: $FamilyName $br
        Email: $emailOfSender $br
        $td2 $td1
        Phone: $phone  $br
        City:  $city  $br
        Country: $country $br
        $td2 $tr2 $table2
        YOUR DEMAND $br
        $table1 $tr1 $td1
        Start date: $startDate $br 
        Nights: $nights $td2
        End date: $endDate $br
        
        $td2 $tr2 $table2

$table1 $thead1 $tr1 
$th1 Stay in :$th2
$th1 Price for 1 night$th2
$th1 Quantity of adults
$th2 $th1 Quantity of children(4-6)
$th2 $th1 Quantity of children(7-12)
$th2 $th1 Price (ILS) $th2

$tr2 $thead2 $tbody1 $tr1 $td1 Single room $td2
$td1 230 ILS /pers $td2 $td1 $adults1
$td2 $td1 $td2 $td1 $td2
$td1 $price_single $td2 $tr2 $tr1 

$td1 Double room (twin or couple) $td2
$td1 140 ILS /pers $td2
$td1 $adults2 $td2 $td1 $children2_50
$td2 $td1 $children2_25
$td2 $td1 $price_double $td2

$tr2 $tr1 $td1 Triple or quadruple room $td2
$td1 120 ILS /pers $td2
$td1 $adults3 $td2
$td1 $children3_50
$td2 $td1 $children3_25
$td2 $td1 $price_triple $td2
$tr2 $tr1

$td1 Meal $td2
$td1 65 ILS /pers $td2
$td1 $adults_m
$td2 $td1 $children_m_50
$td2 $td1 $children_m_25
$td2 $td1 $price_meal $td2 $tr2
$tbody2 $table2

$p1 Comments: $br $comments $p2
$p1 TOTAL Price: $price_total ILS $p2 
        $p1
        Free for a children under 3 years old$br
        Free meal for a  children under 3 years old$br
        50% for a children 4-6 years old$br
        50% for the meal for a children 4-6 years old$br
        25% for a children 7-12 years old$br
        25% for the meal for a children 7-12 years old
        $p2
        $html_in_email_2
        ";

        //var_dump($_POST);

        $transport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, "ssl")
            ->setUsername($myEmail)
            ->setPassword($myPass);

        $mailer = Swift_Mailer::newInstance($transport);

        $message = Swift_Message::newInstance($subject)
            ->setFrom(array($myEmail => 'INFO'))
            ->setTo(array($myEmail))
            ->setContentType('text/html')
            ->setBody($body);


        $result = $mailer->send($message);


        $emailSent = true;

    }
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
    <meta charset="utf-8">
    <title>Abuna Faraj pilgrim house</title>

    <!-- datepicker -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Datepicker - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="/resources/demos/style.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script>
        $( function() {
            $( "#datepicker1" ).datepicker();
            $( "#datepicker2" ).datepicker();
        } );
    </script>



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
            background: #B0BD9F;
        }

        #contact-wrapper {
            width:950px;
            margin: 0 auto;
            border:1px solid #e2e2e2;
            background:#D9EDF7;
            padding:30px;
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
            font-size:14px;
        }

        form#contactform textarea {
            font-family:Arial, Tahoma, Helvetica, sans-serif;
            font-size:100%;
            padding:0.6em 0.5em 0.7em;
            border-color:#B7B7B7 #E8E8E8 #E8E8E8 #B7B7B7;
            border-style:solid;
            border-width:1px;
        }

        .panel-heading {
            font-size: 14px;
            background-color: #A5644E;
            padding: 10px 15px;
            border-bottom: 1px solid #ffffff;
            line-height: 1.42857143;
            color: #ffffff;
        }
        .btn {
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            background-image: -webkit-gradient(linear, left top, left bottom, from(#54b4eb), color-stop(60%, #2fa4e7), to(#1d9ce5));
        }


        table {
            width: 100%;
            max-width: 100%;
            margin-bottom: 20px;
            border-left: 0;
            padding: 5px;
            background-color:#fff !important

        }

        #text_down div {
            text-align:left;
        }

        .text-10 {
            font-size: 12px;
        }

        .required-col::after {
            content: "*";
            color: red;
        }
        .col-md-12{
            position:relative;
            min-height:1px;
            padding-left:15px;
            padding-right:15px;
            text-align:right;

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

        <div class="panel-heading"><strong>IDENTIFICATION</strong></div>
        <table width="100%">
            <tr><td>
                <div>
            <label for="name"><strong>Name:</strong></label>
            <input type="text" size="50" name="contactname" id="contactname" value="" class="required" />
        </div>

        <div>
            <label for="FamilyName"><strong>Family name:</strong></label>
            <input type="text" size="50" name="FamilyName" id="FamilyName" value="" class="required" />
        </div>

        <div>
            <label for="email"><strong>Email:</strong></label>
            <input type="text" size="50" name="email" id="email" value="" class="required email" />
        </div>
        </td>
        <td>
        <div class="">
            <label for="phone"><strong>Phone:</strong></label>
            <input type="text" size="50" name="phone" id="phone" value="" class="required" />
        </div>
        <div>
            <label for="city"><strong>City:</strong></label>
            <input type="text" size="50" name="city" id="city" value="" class="required" />
        </div>

        <div>
            <label for="country"><strong>Country:</strong></label>
            <input type="text" size="50" name="country" id="country" value="" class="required" />
        </div>
        </td>
        </tr>
        </table>

        <div class="panel-heading"><strong>YOUR DEMAND</strong></div>
        <table width="100%">
            <tr><td>
        <div>
            <label for="startDate"><strong>Start date:</strong></label>
            <input type="text" size="50" name="startDate" id="datepicker1" value="" class="required" />
        </div>
                </td>

            <td>
        <div>
            <label for="endDate"><strong>End date:</strong></label>
            <input type="text" size="50" name="endDate" id="datepicker2" value="" class="required" />
        </div>
                </td>
            </tr>
        </table>

        <table class="">
            <thead>
            <tr>
                <th>Stay in :</th>
                <th class="">Price for 1 night</th>
                <th class="required-col">
                    <span class="">Quantity of adults</span>
                </th>
                <th>
                    <span class="">Quantity of children(4-6)</span>
                </th>
                <th>
                    <span class="">Quantity of children(7-12)</span>
                </th>
                <th>
                    <span class="">Price (ILS)</span>
                </th>
            </tr>
            </thead>

            <tbody>
            <tr class="">
                <td>Single room</td>
                <td class="">230 ILS /pers</td>
                <td class="">
                    <input id="adults1" name="adults1" min="0" max="99" class="" type="number">
                </td>
                <td class=""></td>
                <td class=""></td>
                <td class="">0,00</td>
            </tr>
            <tr class="reservation">
                <td>Double room (twin or couple)</td>
                <td class="">140 ILS /pers</td>
                <td class="">
                    <input id="adults2" name="adults2" min="0" max="99" class="" type="number">
                </td>
                <td class="">
                    <input id="children2_50" name="children2_50" min="0" max="99" class="" type="number">

                </td>
                <td class="">
                    <input id="children2_25" name="children2_25" min="0" max="99" class="" type="number">
                </td>
                <td class="">0,00</td>
            </tr>
            <tr class="reservation">
                <td>Triple or quadruple room</td>
                <td class="">120 ILS /pers</td>
                <td class="reservation-adults">
                    <input id="adults3" name="adults3" min="0" max="99" class="" type="number">
                </td>
                <td class="">
                    <input id="children3_50" name="children3_50" min="0" max="99" class="" type="number">
                </td>
                <td class="">
                    <input id="children3_25" name="children3_25" min="0" max="99" class="" type="number">
                </td>
                <td class="">0,00</td>
            </tr>

            <tr class="reservation">
                <td>Meal</td>
                <td class="hidden-print">65 ILS /pers</td>
                <td class="reservation-adults">
                    <input id="adults_meal" name="adults_meal" min="0" max="99" class="" type="number">

                </td>
                <td class="reservation-children">
                    <input id="children_meal_50" name="children_meal_50" min="0" max="99" class="" type="number">
                </td>
                <td class="">
                    <input id="children_meal_25" name="children_meal_25" min="0" max="99" class="" type="number">
                </td>
                <td class="">0,00</td>
            </tr>
            </tbody>

        </table>

        <div class="row">

            <div class="col-md-12">
                <div class="">
                    <strong class="">
                        Total ILS: <span id="reservation-price-total" class="">0,00</span>
                    </strong>
                </div>
            </div>


            <div>
            <label for="message"><strong>More details (300 symbols max):</strong></label>
            <textarea rows="5" cols="50" name="message" id="message" class="required"></textarea>
        </div>

    <span><span style="color:red">*</span>required fields</span>

            <div class="text-10" id="text-down">
                <p>Free for a children under 3 years old</p>
                <p>Free meal for a  children under 3 years old</p>
                <p>50% for a children 4-6 years old</p>
                <p>50% for the meal for a children 4-6 years old</p>
                <p>25% for a children 7-12 years old</p>
                <p>25% for the meal for a children 7-12 years old</p>
            </div>
<br>


    <input class="btn" type="submit" value="Send Message" name="submit" />
    </form>
</div>
</body>
</html>

<!--
// TODO
// HTML in email
// JS for calc the total on page