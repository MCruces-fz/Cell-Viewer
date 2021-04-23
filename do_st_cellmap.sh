#!/bin/bash

COMMAND=$1
FROMDATE=$2
TODATE=$3

HLDDIR="/home/mcruces/Documents/fptrucha_hits/test01_hlds/"
OUTDIR="/home/mcruces/Documents/fptrucha_hits/test01/"
LUPTAB="/media/Datos2TB/tragaldabas/luptab/lookuptable.txt"
PARSDIR="/media/Datos2TB/damian/tragaldabas/2021DST/pars/" # Damian

function show_help() {
    echo "To use the run command, arguments [FROM] and [TO] must be:"
    echo "    Integers"
    echo "    Dates with the format YYDOYHHMMSS"
    echo "        YY: Two digits year"
    echo "        DOY: Three digits Day Of the Year"
    echo "        HHMMSS: Time HH:MM:SS"
    echo "They can have the desired length, but starting allways"
    echo "with the year (YY) and followed by the day of the year (DOY) "
}

function do_unpack() {
    FILENAME=$1
    # YY=${FILENAME:2:2}
    # DOY=${FILENAME:4:3}
    YY=21
    DOY=068

    # echo Analyzing file: $FILENAME

    root -l  <<EOF
{
Unpacker* u = new Unpacker("$HLDDIR", "$FILENAME", "$OUTDIR", 10000000, "$LUPTAB", "$PARSDIR/20${YY}_day_${DOY}_CalPars.txt");
}
EOF
}

function run() {

    re='^[0-9]+$'
    if ! [[ $FROMDATE =~ $re ]] ; then
        echo "Error: [FROM] is not a number" >&2
        exit 1

    elif ! [[ $TODATE =~ $re ]] ; then
        echo "Error: [TO] is not a number" >&2
        exit 1

    elif (( $FROMDATE > $TODATE )); then
        echo "Please: [FROM] < [TO]"
        exit 1
    fi

    for (( date=$FROMDATE; date<=$TODATE; date++))
    do
        for a in `find $HLDDIR -maxdepth 1 -type f -name tr$date* -print`;
        do
            do_unpack `basename $a`
        done
    done
}

case $COMMAND in
run)       run         ;;
--help)    show_help   ;;

*)
    if [[ $COMMAND == "" ]]; then
        echo "At least one argument is needed"
    else
        echo "Unrecognized command: ${COMMAND}"
    fi

    echo ""
    echo "Usage:"
    echo "$0 [COMMAND]"
    echo ""
    echo "COMMAND:"
    echo "    run [FROM] [TO]"
    echo "    --help    <- Show more extended help."
    echo "         "
    ;;
esac
