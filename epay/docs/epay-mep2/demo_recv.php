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

$ENCODED  = $_POST['encoded'];
$CHECKSUM = $_POST['checksum'];

# XXX Secret word with which merchant make CHECKSUM on the ENCODED packet
$secret = 'SET_THIS_CORRECT';
$hmac   = hmac('sha1', $ENCODED, $secret); # XXX SHA-1 algorithm REQUIRED

if ($hmac == $CHECKSUM) { # XXX Check if the received CHECKSUM is OK
    
    $data = base64_decode($ENCODED);
    $lines_arr = split("\n", $data);
    $info_data = '';
    
    foreach ($lines_arr as $line) {
        if (preg_match("/^INVOICE=(\d+):STATUS=(PAID|DENIED|EXPIRED)(:PAY_TIME=(\d+):STAN=(\d+):BCODE=([0-9a-zA-Z]+))?$/", $line, $regs)) {
            $invoice  = $regs[1];
            $status   = $regs[2];
            $pay_date = $regs[4]; # XXX if PAID
            $stan     = $regs[5]; # XXX if PAID
            $bcode    = $regs[6]; # XXX if PAID

            # XXX process $invoice, $status, $pay_date, $stan, $bcode here

            # XXX if OK for this invoice
            $info_data .= "INVOICE=$invoice:STATUS=OK\n";

            # XXX if error for this invoice
            # XXX $info_data .= "INVOICE=$invoice:STATUS=ERR\n";

            # XXX if not recognise this invoice
            # XXX $info_data .= "INVOICE=$invoice:STATUS=NO\n";
        }
    }

    echo $info_data, "\n";
}
else {
    echo "ERR=Not valid CHECKSUM\n"; # XXX The description of error is REQUIRED
}
?>
