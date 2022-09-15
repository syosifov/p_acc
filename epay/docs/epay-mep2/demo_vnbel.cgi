#!/usr/bin/perl

use strict;
use warnings;

use CGI;

# XXX ePay.bg URL
my $submit_url  = 'https://www.epay.bg/';

my $beneficiary = 'DATAMAX';                        # XXX Beneficiary name
my $account     = 'BG32 CECB 9790 1100 0154 00';    # XXX IBAN of the Beneficiary
my $bic         = 'CECBBGSF';                       # XXX BIC of the Beneficiary's bank
my $sum         = sprintf("%.2f", rand(100) * 100); # XXX Amount
my $descr       = 'Test';                           # XXX Payment description

# XXX Packet:
#     MERCHANT                     REQUIRED
#     IBAN                         REQUIRED
#     BIC                          REQUIRED
#     TOTAL                        REQUIRED
#     STATEMENT                    REQUIRED
#     PSTATEMENT                   OPTIONAL

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

<form action="$submit_url" method=post>
<input type=hidden name=PAGE value="paylogin">
<input type=hidden name=MERCHANT value="$beneficiary">
<input type=hidden name=IBAN value="$account">
<input type=hidden name=BIC value="$bic">
<input type=hidden name=STATEMENT value="$descr">
<input type=hidden name=PSTATEMENT value="">

<TR>
<TD>
<xmp>
Получател:      $beneficiary
Сметка:         $account
BIC:            $bic
Вид плащане: 
Сума:           $sum
Основание:      $descr
</xmp>

</TD>
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
