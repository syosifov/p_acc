#!/usr/bin/perl

use strict;
use warnings;

use CGI;

use MIME::Base64;
use Digest::SHA1 qw(sha1);
use Digest::HMAC qw(hmac_hex);

# XXX ePay.bg URL (https://demo.epay.bg/ if POST to DEMO system)
my $submit_url = 'https://www.epay.bg/';
# XXX Secret word with which merchant make CHECKSUM on the ENCODED packet
my $secret     = 'SET_THIS_CORRECT';

my $min        = 'SET_THIS_CORRECT';
my $invoice    = sprintf("%.0f", rand(10) * 100000); # XXX Invoice
my $sum        = '22.80';                            # XXX Ammount
my $exp_date   = '01.08.2020';                       # XXX Expiration date
my $descr      = 'Test';                             # XXX Description

my $data = <<DATA;
MIN=$min
INVOICE=$invoice
AMOUNT=$sum
EXP_TIME=$exp_date
DESCR=$descr
DATA

# XXX Packet:
#     (MIN or EMAIL)=     REQUIRED
#     INVOICE=            REQUIRED
#     AMOUNT=             REQUIRED
#     EXP_TIME=           REQUIRED
#     DESCR=              OPTIONAL

my $ENCODED  = encode_base64($data, '');
my $CHECKSUM = hmac_hex($ENCODED, $secret, \&sha1);

print "Content-type: text/html; charset=windows-1251\n\n";
print <<HTML;
<HTML>
<head>
    <meta http-equiv="content-type" content="text/html; charset=windows-1251">
</head>
<BODY TEXT=#000000 BGCOLOR=#FFFFFF>
<BR>
<BR>
<CENTER><h1>DEMO</h1>
<TABLE border=1>

<form action="$submit_url" method=POST>
<input type=hidden name=PAGE value="paylogin">
<input type=hidden name=ENCODED value="$ENCODED">
<input type=hidden name=CHECKSUM value="$CHECKSUM">
<input type=hidden name=URL_OK value="SET_URL_OK_IF_NEEDED">
<input type=hidden name=URL_CANCEL value="SET_URL_CANCEL_IF_NEEDED">

<TR>
<TD>МИН: $min</TD>
</TR>

<TR>
<TD>Фактура номер: $invoice</TD>
</TR>

<TR>
<TD>Описание: $descr</TD>
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
Всичко   $sum
</xmp>

</TD>
</TR>

<TR>
<TD>Сума: $sum</TD>
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
HTML
