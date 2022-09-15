#!/usr/bin/perl

use strict;
use warnings;

use CGI;

use MIME::Base64;
use Digest::SHA1 qw(sha1);
use Digest::HMAC qw(hmac_hex);

print "Content-type: text/html\n\n";

my $q = new CGI;
my $ENCODED  = $q->param('encoded');
my $CHECKSUM = $q->param('checksum');

# XXX Secret word with which merchant make CHECKSUM on the ENCODED packet
my $secret = 'SET_THIS_CORRECT';
my $hmac   = hmac_hex($ENCODED, $secret, \&sha1);

if ($hmac eq $CHECKSUM) { # XXX Check if the received CHECKSUM is OK
    
    my $data = decode_base64($ENCODED);
    my @lines = split /\n/, $data;
    my $info_data;
    
    for my $line (@lines) {
        next unless $line =~ /^INVOICE=(\d+):STATUS=(PAID|DENIED|EXPIRED)(:PAY_TIME=(\d+):STAN=(\d+):BCODE=([0-9a-zA-Z]+))?$/;
        my $invoice  = $1;
        my $status   = $2;
        my $pay_date = $4; # XXX if PAID
        my $stan     = $5; # XXX if PAID
        my $bcode    = $6; # XXX if PAID
        
        # XXX process $invoice, $status, $pay_date, $stan, $bcode here

        # XXX if OK for this invoice
        $info_data .= "INVOICE=$invoice:STATUS=OK\n";

        # XXX if error for this invoice
        # XXX $info_data .= "INVOICE=$invoice:STATUS=ERR\n";

        # XXX if not recognise this invoice
        # XXX $info_data .= "INVOICE=$invoice:STATUS=NO\n";
    }

    print $info_data, "\n";
}
else {
    print "ERR=Not valid CHECKSUM\n"; # XXX The description of error is REQUIRED
}
