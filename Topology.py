from mininet.topo import Topo
from mininet.util import customClass

#SCENARIO-: Smart Building with Edge Service for Cloud-based Internet-of-Things

# Configures sFlow on OVS and posts topology to sFlow-RT web UI via sflow script
exec(open('sflow-rt/extras/sflow.py').read())

class MyTopo( Topo ):  
    
    def __init__( self ):
        "The custom topology consisting of Ten hosts, Four switches"
    
        # Initializing the topology
        Topo.__init__( self )

        # Adding of hosts(IoT devices, Edge Server, and Attacker Devices)
        Host1 = self.addHost( 'EdgeServer', ip='10.0.0.1/24')	#Edge Cloudlet server
        Host2 = self.addHost( 'IoThvac' ,  ip='10.0.0.2/24') 	#Iot Node 1
        Host3 = self.addHost( 'IoTcamera' ,  ip='10.0.0.3/24') 	#Iot Node 2
        Host4 = self.addHost( 'IoTlight' ,  ip='10.0.0.4/24') 	#Iot Node 3
        Host5 = self.addHost( 'IoTtherm' ,  ip='10.0.0.5/24') 	#Iot Node 4
        Host6 = self.addHost( 'IoTsensor' ,  ip='10.0.0.6/24') 	#Iot Node 5
        Host7 = self.addHost( 'IoTsecsys' ,  ip='10.0.0.7/24') 	#Iot Node 6
        Host8 = self.addHost( 'Attacker1' ,  ip='10.0.0.8/24')	#Attacker Machine 1
        Host9 = self.addHost( 'Attacker2' ,  ip='10.0.0.9/24')	#Attacker Machine 2
        Host10 = self.addHost( 'Attacker3' , ip='10.0.0.10/24')	#Attacker Machine 3
        
        # Adding of switches - Establising the Edge/Fog layer 
        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')
        Switch3 = self.addSwitch('s3')
        Switch4 = self.addSwitch('s4')
                
        # Add links (connection) to connect the host and switches
                              
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch2 )
        self.addLink( Host3, Switch2 )
        self.addLink( Host4, Switch2 )
        self.addLink( Host5, Switch3 )
        self.addLink( Host6, Switch3 )
        self.addLink( Host7, Switch3 )
        self.addLink( Host8, Switch4 )
        self.addLink( Host9, Switch4 )
        self.addLink( Host10, Switch4 )
        self.addLink( Switch2, Switch1 )
        self.addLink( Switch3, Switch1 )
        self.addLink( Switch4, Switch1 )
        
        
                
               
topos = { 'mytopo': ( lambda: MyTopo() ) } 
