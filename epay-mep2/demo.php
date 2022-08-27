<?php
function hmac($algo,$data,$passwd){
        /* md5 and sha1 only */
        $algo=strtolower($algo);
        $p=array('md5'=>'H32','sha1'=>'H40');
        if(strlen($passwd)>64) $passwd=pack($p[$algo],$algo($passwd));
        if(strlen($passwd)<64) $passwd=str_pad($passwd,64,chr(0));

        $ipad=substr($passwd,0,64) ^ str_repeat(chr(0x36),64);
        $opad=substr($passwd,0,64) ^ str_repeat(chr(0x5C),64);

        return($algo($opad.pack($p[$algo],$algo($ipad.$data))));
}

# XXX ePay.bg URL (https://demo.epay.bg/ if POST to DEMO system)
$submit_url = 'https://www.epay.bg/';
# XXX Secret word with which merchant make CHECKSUM on the ENCODED packet
$secret     = 'SET_THIS_CORRECT';

$min        = 'SET_THIS_CORRECT';
$invoice    = sprintf("%.0f", rand(10) * 100000); # XXX Invoice
$sum        = '22.80';                            # XXX Ammount
$exp_date   = '01.08.2020';                       # XXX Expiration date
$descr      = 'Test';                             # XXX Description

$data = <<<DATA
MIN={$min}
INVOICE={$invoice}
AMOUNT={$sum}
EXP_TIME={$exp_date}
DESCR={$descr}
DATA;

# XXX Packet:
#     (MIN or EMAIL)=     REQUIRED
#     INVOICE=            REQUIRED
#     AMOUNT=             REQUIRED
#     EXP_TIME=           REQUIRED
#     DESCR=              OPTIONAL

$ENCODED  = base64_encode($data);
$CHECKSUM = hmac('sha1', $ENCODED, $secret); # XXX SHA-1 algorithm REQUIRED

echo <<<HTML
<HTML>
<head>
    <meta http-equiv="content-type" content="text/html; charset=windows-1251">
</head>
<BODY TEXT=#000000 BGCOLOR=#FFFFFF>
<BR>
<BR>
<CENTER><h1>DEMO</h1>
<TABLE border=1>

<form action="{$submit_url}" method=POST>
<input type=hidden name=PAGE value="paylogin">
<input type=hidden name=ENCODED value="{$ENCODED}">
<input type=hidden name=CHECKSUM value="{$CHECKSUM}">
<input type=hidden name=URL_OK value="SET_URL_OK_IF_NEEDED">
<input type=hidden name=URL_CANCEL value="SET_URL_CANCEL_IF_NEEDED">

<TR>
<TD>МИН: {$min}</TD>
</TR>

<TR>
<TD>Фактура номер: {$invoice}</TD>
</TR>

<TR>
<TD>Описание: {$descr}</TD>
</TR>

<TR>
<TD>

<xmp>
Продукти                    кол.  ед.цена   цена
------------------------------------------------
продукт1                     3      2.50    7.50
продукт2                     1      3.50    3.50
продукт3                     2      4.00    8.00
------------------------------------------------
общо   19.00
ДДС    3.80
Всичко   {$sum}
</xmp>

</TD>
</TR>

<TR>
<TD>Сума: {$sum}</TD>
</TR>


</table>

<table width=100%>
<TR align=center>
<TD><INPUT type=submit></TD>
</TR>


</TABLE>

</form>
</BODY>
</HTML>
HTML;
?>
