from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from time import sleep

class MulticastTestTopo( Topo ):
    "Simple multicast testing example"
    
    def __init__( self ):
        "Create custom topo."
        
        # Initialize topology
        Topo.__init__( self )
        
        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        h11 = self.addHost('h11')
        
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        
        
        # Add links
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s4)
        self.addLink(s4, s5)
        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s6, s3)
        self.addLink(s3, s7)
        self.addLink(s7, s5)
        
        self.addLink(s2, h1)
        self.addLink(s3, h2)
        self.addLink(s3, h3)
        self.addLink(s5, h4)
        self.addLink(s5, h5)
        self.addLink(s5, h6)
        self.addLink(s2, h7)
        self.addLink(s6, h8)
        self.addLink(s7, h9)
        self.addLink(s4, h10)
        self.addLink(s1, h11)

def mcastConfig(net):
    # Configure hosts for multicast support
    net.get('h1').cmd('route add -net 224.0.0.0/4 h1-eth0')
    net.get('h2').cmd('route add -net 224.0.0.0/4 h2-eth0')
    net.get('h3').cmd('route add -net 224.0.0.0/4 h3-eth0')
    net.get('h4').cmd('route add -net 224.0.0.0/4 h4-eth0')
    net.get('h5').cmd('route add -net 224.0.0.0/4 h5-eth0')
    net.get('h6').cmd('route add -net 224.0.0.0/4 h6-eth0')
    net.get('h7').cmd('route add -net 224.0.0.0/4 h7-eth0')
    net.get('h8').cmd('route add -net 224.0.0.0/4 h8-eth0')
    net.get('h9').cmd('route add -net 224.0.0.0/4 h9-eth0')
    net.get('h10').cmd('route add -net 224.0.0.0/4 h10-eth0')
    net.get('h11').cmd('route add -net 224.0.0.0/4 h11-eth0')

def mcastTest():
    topo = MulticastTestTopo()

    # External controller
    # ./pox.py samples.pretty_log openflow.discovery openflow.igmp_manager openflow.groupflow log.level --WARNING --openflow.igmp_manager=WARNING --openflow.groupflow=DEBUG
    net = Mininet(topo, controller=RemoteController, build=False)
    pox = RemoteController('pox', '127.0.0.1', 6633)
    net.addController('c0', RemoteController, ip = '127.0.0.1', port = 6633)
    
    net.start()
    mcastConfig(net)
    # net.get('h2').cmd('python ./multicast_receiver.py &');
    # net.get('h3').cmd('python ./multicast_receiver.py &');
    # net.get('h4').cmd('python ./multicast_receiver.py &');
    sleep(8)   # Allow time for the controller to detect the topology
    net.get('h6').cmd('python ./multicast_receiver.py &');
    sleep(2)
    net.get('h1').cmd('python ./multicast_sender.py &');
    sleep(5)
    net.get('h5').cmd('python ./ss_multicast_receiver.py &');
    CLI(net)
    net.stop()

topos = { 'mcast_test': ( lambda: MulticastTestTopo() ) }

if __name__ == '__main__':
    setLogLevel( 'info' )
    mcastTest()
