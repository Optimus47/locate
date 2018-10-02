#!/bin/bash
if [ "$1" = "1" ]
then
echo "#"
./script-pw-des.exp $2 $3| sed '1,/^#/d;/^#/{q}'
exit 0
elif [ "$1" = "2" ]
then
echo "#"
./script-user-des.exp $2 $3| sed '1,/^#/d;/^#/{q}'
exit 0
elif [ "$1" = "3" ]
then
echo "interface $3"
./script-cis-des.exp $2 $3 | sed '1,/^interface/d;/^!/{q}' 
exit 0
else
echo "=== Locate $1 ==="
macmac=`sudo nmap -n -sP $1 | awk -F'[ :]'  '/MAC/ {print $4$5"-"$6$7"-"$8$9}'`
if [ -z $macmac ]
then 
 echo "MAC Not FOUND!"; exit 0
fi
fi

echo "*** MAC is $macmac"


for x in sw1141 sw1221 
do
 ret=`./script-pw.exp $x $macmac| awk '/LEARNED/ {print $4}'|uniq`
if [ -n "$ret" ]
then
echo "==== Found on $x ===="
echo "+++ Port $ret
Description: $0 1 $x $ret"
#./script-pw-des.exp $x $ret| sed '1,/^#/d;/^#/{q}'
fi
done

for x in sw1211 sw1321 sw1322 sw1541 sw3115 sw1641
do
 ret=`./script-user.exp $x $macmac| awk '/LEARNED/ {print $4}'|uniq`
if [ -n "$ret" ]
then
echo "==== Found on $x ===="
echo "+++ Port $ret
Description: $0 2 $x $ret"
#./script-user-des.exp $x $ret| sed '1,/^#/d;/^#/{q}'
fi
done

macmac=${macmac//-/.}
echo "*** Cisco MAC is $macmac" 

for x in sw1651 sw1661 sw1681 sw1682
do
 ret=`./script-cis.exp $x $macmac| awk '/DYNAMIC/ {print $4}'`
if [ -n "$ret" ]
then
echo "==== Found on $x ===="
retport=`echo $ret| awk -F'[ /]' '/Po/ {print $1} /Gi/ {print "GigabitEthernet0/"$2}'`
retport=${retport//Po/Port-channel}
echo "+++ Port $ret"
#echo "Description: ./script-cis-des.sh $x $retport"
echo "Description: ./locate.sh 3 $x $retport"
fi
done
