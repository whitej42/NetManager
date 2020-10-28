""" Custom topology - Mininet

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        H1 = self.addHost( 'h1' )
        H2 = self.addHost( 'h2' )
        H3 = self.addHost( 'h3' )
        H4 = self.addHost( 'h4' )
        SW1 = self.addSwitch( 'sw1' )
        SW2 = self.addSwitch( 'sw2' )
        SW3 = self.addSwitch( 'sw3' )
        SW4 = self.addSwitch( 'sw4' )
        
        switchList = (SW1, SW2 ,SW3, SW4)
        
        # Add Switch Links
        for index in range (0, len(switchList)):
            for index2 in range(index + 1, len(switchList)):
                self.addLink(switchList[index], switchList[Index])

        # Add host links
        self.addLink( H1, SW1 )
        self.addLink( H2, SW2 )
        self.addLink( H3, SW3 )
        self.addLink( H4, SW4 )

topos = { 'mytopo': ( lambda: MyTopo() ) }