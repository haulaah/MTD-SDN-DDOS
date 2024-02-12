                                              # A REACTIVE AND PROACTIVE MOVING TARGET DEFENSE SHUFFLING MECHANISM
                                              # SMART BUILDING CONNECTION TO A EDGE/FOG COMPUTING SCENARIO 
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import icmp
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib import hub
from time import time
from random import randint,seed
from colorama import Fore 

#The MTD mechanism will be a hybrid MTD Shuffling technique: IP Shuffling/Host Randomization (Reactive and Proactive)

#Time out Event
class Event_msg(event.EventBase):
    def __init__(self, message):
        print("Establishing MTD Shuffle with 45 seconds timer interval Proactive mutations")
        super(Event_msg, self).__init__()
        self.msg=message

#Establishing the core app that extends the already exisiting ryu script simple_switch_13
class MTDMechanism(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _EVENTS = [Event_msg] 
    
    #Actual IP Addresses
    Real_Virtual={"10.0.0.1":"","10.0.0.2":"","10.0.0.3":"","10.0.0.4":"","10.0.0.5":"","10.0.0.6":"","10.0.0.7":"","10.0.0.8":"","10.0.0.9":"","10.0.0.10":""}
    #Dictionary object
    Virtual_Real={}   
    #Virtual IP's that will be shuffled between hosts per interval/Reaction
    VirtItems=["10.0.0.11","10.0.0.12","10.0.0.13","10.0.0.14", "10.0.0.15","10.0.0.16", "10.0.0.17","10.0.0.18","10.0.0.19","10.0.0.20", "10.0.0.21","10.0.0.22", "10.0.0.23","10.0.0.24", "10.0.0.25","10.0.0.26","10.0.0.27","10.0.0.28", "10.0.0.29","10.0.0.30","10.0.0.31","10.0.0.32", "10.0.0.33","10.0.0.34", "10.0.0.35", "10.0.0.36","10.0.0.37","10.0.0.38","10.0.0.39","10.0.0.40","10.0.0.41","10.0.0.42", "10.0.0.43","10.0.0.44", "10.0.0.45","10.0.0.46","10.0.0.47","10.0.0.48", "10.0.0.49","10.0.0.50", "10.0.0.51","10.0.0.52", "10.0.0.53","10.0.0.54","10.0.0.55","10.0.0.56", "10.0.0.57","10.0.0.58","10.0.0.59","10.0.0.60", "10.0.0.61","10.0.0.62", "10.0.0.63", "10.0.0.64","10.0.0.65","10.0.0.66", "10.0.0.67", "10.0.0.68","10.0.0.69","10.0.0.70"  ]
    
    def start(self):        
#Declaring User defined event 
        super(MTDMechanism,self).start()
        self.threads.append(hub.spawn(self.EventGenerationTimer))
            
    def EventGenerationTimer(self):
# Time out - 45s      
        while 1:
            self.send_event_to_observers(Event_msg("Time out!"))
            hub.sleep(45) #Establishing a 45 sceonds interval time
    
    def __init__(self, *args, **kwargs):  
        super(MTDMechanism, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths=set()
        self.HostAtSwitch={}
        self.offset_of_mappings=0
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def handleSwitchFeatures(self, ev): 
#Addign Switching info to datapath and flow entry to switches 
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        self.datapaths.add(datapath);
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
          
    def EmptyTable(self,datapath):   
#Empty flow rules.
        ofProto=datapath.ofproto
        parser = datapath.ofproto_parser
        match=parser.OFPMatch()
        flow_mod=datapath.ofproto_parser.OFPFlowMod(datapath,0,0,0,ofProto.OFPFC_DELETE,0,0,1,ofProto.OFPCML_NO_BUFFER,ofProto.OFPP_ANY,ofProto.OFPG_ANY,0,match=match,instructions=[])
        datapath.send_msg(flow_mod)
        
#Listen to timeout & updating RIP-VIP mappings
    @set_ev_cls(Event_msg)
    def update_VirtItems(self,ev):      
 #Random Number generation         
        seed(time())
        NumRand = randint(0,len(self.VirtItems)-1) #returns a random number from the VirtItems
      
        for keys in self.Real_Virtual.keys():
            #A VIP is attached to each host from the pool of VirtItems which commences from the selected inter from the variable: NumRand
            self.Real_Virtual[keys]=self.VirtItems[NumRand]
            NumRand=(NumRand+1)%len(self.VirtItems)    
        self.Virtual_Real = {v: k for k, v in self.Real_Virtual.items()}
        print (Fore.RED +"'" *75  + Fore.RESET)
        print ("*--------------* ACTUAL IP ~~> VIRTUAL IP SHUFFLE MAPPINGS *--------------*")
        print (Fore.RED +"'" *75  + Fore.RESET)
        print (self.Real_Virtual, "\n")
    
        for curSwitch in self.datapaths:
            #Delete existing flow entries
            parser = curSwitch.ofproto_parser
            match=parser.OFPMatch()
            flowModMsg=self.EmptyTable(curSwitch)
            #Establis the Addition of default flow rule
            ofProto=curSwitch.ofproto
            actions = [parser.OFPActionOutput(ofProto.OFPP_CONTROLLER,
                                          ofProto.OFPCML_NO_BUFFER)]
            self.add_flow(curSwitch, 0, match, actions)
        
    def ripa(self,ipAddr):  #returns if Real IP
       
        if ipAddr in self.Real_Virtual.keys():
            return True
    
    def vipa(self,ipAddr):   #returns if Virutal IP
       
        if ipAddr in self.Real_Virtual.values():
            return True
        
    def dirconnect(self,datapath,ipAddr):  #returns if there is a connection between switch and host
       
        if ipAddr in self.HostAtSwitch.keys():
            if self.HostAtSwitch[ipAddr]==datapath:
                return True
            else:
                return False
        return True
            
    def add_flow(self, datapath, priority, match, actions, buffer_id=None, hard_timeout=None):
   #Establishes Addition of Flow rules to switch    
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser        
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id :
            if hard_timeout==None:
                mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
            else:
                mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, hard_timeout=hard_timeout)
        else:
            if hard_timeout==None:
                mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
            else:
                mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, hard_timeout=hard_timeout)
        datapath.send_msg(mod)

    #Packet Handler ICMP & ARP perform Proactive IP Shuffling
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def handlePacketInEvents(self, ev):
       
        actions=[]
        pktDrop=False        
               
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
            
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        arp_Obj=pkt.get_protocol(arp.arp)# Extract ARP object from packet
        icmp_Obj=pkt.get_protocol(ipv4.ipv4)# Extract ICMP object packet
        
#MTD mechanism that learns:.
        if arp_Obj:
                 
            src=arp_Obj.src_ip
            dst=arp_Obj.dst_ip

            if self.ripa(src) and src not in self.HostAtSwitch.keys():
                self.HostAtSwitch[src]=datapath.id
                
            if self.ripa(src):
                match=parser.OFPMatch(eth_type=0x0806,in_port=in_port,arp_spa=src,arp_tpa=dst)
                spa = self.Real_Virtual[src] 
                print ("")
                print("Establishing MTD Shuffle for Reactive mutations")
                print("Swapping the Source RIP "+ Fore.GREEN +src+ Fore.RESET +" to  Source VIP "+ Fore.RED+spa+ Fore.RESET )
                
                actions.append(parser.OFPActionSetField(arp_spa=spa))
                
            if self.vipa(dst):
                match=  parser.OFPMatch(eth_type=0x0806,in_port=in_port,arp_tpa=dst,arp_spa=src)
                if self.dirconnect(datapath=datapath.id,ipAddr=self.Virtual_Real[dst]):
                    keys = self.Virtual_Real.keys() 
                    tpa = self.Virtual_Real[dst] 
                    print ("")
                    print("Establishing MTD Shuffle for Reactive mutations")
                    print("Swapping the Destination VIP "+ Fore.RED +dst+ Fore.RESET +" to Destination VIP "+ Fore.GREEN +tpa+ Fore.RESET)
                  
                    actions.append(parser.OFPActionSetField(arp_tpa=tpa))
                    
            elif self.ripa(dst):
                
                match=parser.OFPMatch(eth_type=0x0806,in_port=in_port,arp_spa=src,arp_tpa=dst)
                if not self.dirconnect(datapath=datapath.id,ipAddr=dst):
                    pktDrop=True
                    print ("Dropping from",dpid)
            else:
                pktDrop=True
        elif icmp_Obj:
           
            print("ICMP PACKET FOUND!")
            src=icmp_Obj.src
            dst=icmp_Obj.dst
            
            if self.ripa(src) and src not in self.HostAtSwitch.keys():
                self.HostAtSwitch[src]=datapath.id 
                           
#MTD mechanism that learns:.        
            if self.ripa(src):         
                match=  parser.OFPMatch(eth_type=0x0800,in_port=in_port,ipv4_src=src,ipv4_dst=dst)
                ipSrc = self.Real_Virtual[src]
                print ("")
                print("Establishing MTD Shuffle for Reactive mutations")
                print("Swapping the Source RIP "+ Fore.GREEN +src+ Fore.RESET +"to Source VIP "+ Fore.RED +ipSrc+ Fore.RESET)
                
                actions.append(parser.OFPActionSetField(ipv4_src=ipSrc))
            if self.vipa(dst):
                #print the host connected to the switch
                match=  parser.OFPMatch(eth_type=0x0800,in_port=in_port,ipv4_dst=dst,ipv4_src=src)
                if self.dirconnect(datapath=datapath.id,ipAddr=self.Virtual_Real[dst]):
                    ipDst = self.Virtual_Real[dst] 
                    print ("")
                    print("Establishing MTD Shuffle for Reactive mutations")
                    print("Swapping the Destination VIP "+ Fore.RED +dst+ Fore.RESET +"to Destination RIP "+ Fore.GREEN +ipDst+ Fore.RESET)
                    
                    actions.append(parser.OFPActionSetField(ipv4_dst=ipDst))
            
            elif self.ripa(dst):              
                match=parser.OFPMatch(eth_type=0x0806,in_port=in_port,arp_spa=src,arp_tpa=dst)
                if not self.dirconnect(datapath=datapath.id,ipAddr=dst):
                    pktDrop=True
                    print ("Dropping from",dpid)
            else:
                pktDrop=True
        #source eth object                           
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth.dst
        src = eth.src        
        self.mac_to_port.setdefault(dpid, {})
        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)             
        self.mac_to_port[dpid][src] = in_port
       
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        
        if not pktDrop:
            actions.append(parser.OFPActionOutput(out_port))
        
        if out_port != ofproto.OFPP_FLOOD:
#Validation of BUFFER ID 
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions,msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)    
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
#Packet out Message 
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
       
        datapath.send_msg(out)
