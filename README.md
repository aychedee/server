Personal server config
======================

Services
--------

* www.interpretthis.org
* www.aychedee.com
* squid proxy

Installation from scratch
-------------------------

New instances on AWS with latest Ubuntu still need to be logged into and have Python installed on them:

    sudo apt-get install python
    
Then: 

    make deploy 
    
 Should install the sites and all services. After that some modifications to the name server records will be required
