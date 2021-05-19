# COMP3000 - University of Plymouth

### BSc (Hons) Computer & Information Security

* Project Owner: James White 
* Project Supervisor: Dr Lingfen Sun
  
![Logo](https://github.com/jwhite96/COMP3000/blob/main/NetManager/static/images/logo.png)

## NetManager: Network Configuration & Management Tool
NetManager is a network configuration & management (NCM) tool for automated configuration and monitoring of network devices. Built using the [Django Web Framework](https://www.djangoproject.com), NetManager provides a clean and easy to use web interface that interacts with network devices to retrieve information and push configuration changes by utilising the [Netmiko](https://pypi.org/project/netmiko/) Python library.

### System Functionality
* User account functionality
* Store and manage network devices
* View device information & configuration
* Configure device interfaces
* Disable all unused interfaces
* Create and delete access lists
* Apply and remove access lists from interfaces
* Send commands manually *if required
* Configuration audit logs

## YouTube Demonstation Video
https://www.youtube.com/watch?v=xxV7JNZJYpQ

## Help Guide
The application comes with a built in help page that explains how to carry out all of the functions within the NetManager application <br>
http://ec2-18-169-21-1.eu-west-2.compute.amazonaws.com/help

## User & Installation Guide
### Manual Installation
Since the application requires a live Cisco network to carry out most of the functionality, it is recommended to test the application using the online version. However, this section outlines the step required to run the application locally.
1. Install PyCharm and the Python 3.8 interpreter from: <br>
https://www.jetbrains.com/pycharm/download/#section=windows <br>
https://www.python.org/downloads/release/python-380/
3.	Clone the GitHub repository
4.	Using the command prompt or PowerShell, navigate to the folder where the repo installed and change to the directory **NetManager/NetManager/**
5.	Run the command “virtualenv venv”
*	**You may need to install virtualenv using PIP install**
5.	Navigate to directory **NetManager/NetManager/venv/bin**
6.	Run the command “source activate”
7.	Return to **NetManager/NetManager** and run the following commands 
*	*“python manage.py makemigrations”*
*	*“python manage.py migrate”*
*	*“python manage.py runserver”*
8.	This will migrate the database and start the virtual server
9.	Go to the browser and navigate to 127.0.0.1:8000
10.	The NetManager home page will appear

### Online Version
There is a working version of this application online with a full working network and user accounts. The information on how to access the site is listed below.
### If the server is down or for the test network is not responding, please send an email to james.white-12@students.plymouth.ac.uk and the issue will be rectified immediately.
Please avoid clicking multiple times during long loading process (keep an eye on the browser refresh icon). GET & POST requests are chargeable to the lead developer so please bare this in mind. You are free to use the application how you please.

#### URL:
http://ec2-18-169-21-1.eu-west-2.compute.amazonaws.com 

#### User Credentials:
This is the test account credentials that have been set up on this server. Login credentials are case sensitive. The account comes with the two test network devices already added to the account.
* **Username:** UOPTest 
*	**Password:** uop10590453

#### Device List:
Should you wish to create a new user account and add devices manually, below is the list of devices on the test network. The IP address is the SSH address or management address the application uses to make connections. All usernames, passwords and secrets are lower case.

| Device Name |    IP Address   | Username | Password | Secret |
|:-----------:|:---------------:|:--------:|----------|:------:|
|      R1     | 192.168.122.100 |   admin  | cisco    |  cisco |
|      R2     | 192.168.122.200 |   admin  | cisco    |  cisco |
