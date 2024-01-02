WINTER OF CODE 6.0 (INFOSEC DIVISION)
ATUL SM
23JE0184
CHEMICAL ENGINEERING

PROBLEM STATEMENT - Developing a Malware to monitor and export new files added to Victim File System.

OBJECTIVE/BRIEF - This file monitoring project is a scalable Python-based solution designed to provide real-time insights into file system activities. The primary aim of this project is to offer a comprehensive file monitoring tool that can track and log events such as file creations, modifications, deletions, and folder creations in multiple directories concurrently.
    NOTE - (Separate monitoring systems have been provided , one for monitoring all the above mentioned events, one for monitoring only creation of files/folders as per the problem statement)

TECH STACK USED - 1)Python - The main programming language used for this project.
                  2) Watchdog - Watchdog is a python library that can be used to monitor file system events such as creation, modification and deletions.The main                                             intension behind using watchdog library to form a monitoring system is that it is cross-platform compatible.
                                It provides and 'Observer' class for setting up event handlers and reacting to file system changes.
                  3) Multiprocessing - It is a module used for monitoring multiple folders parallely
                  4) MySQL Connector - The 'mysql.connector' library is used for connecting to a MySQL database. It allows Python programs to interact with MySQL 
                                       databases, executing SQL queries and managing database connections.
                  5) Logging - The built-in logging module is used for logging events and errors in the program. It provides a flexible framework for emitting log                                 messages from Python programs.
                  6) pytz - The 'pytz' library is used to handle timezones in python. In this project it had the role of converting GMT to IST timezone.
                  7) Datetime - The built-in 'datetime' module is used for working with dates and times in Python.
                  8) MySQL Database - The project involves interacting with a MySQL database to store information about monitored files . The databases stores such as file                                         paths, name,file extension, file size, creation time .
                                      (for the monitor used for all events some additional columns such as event type, modification time, deletion time etc are added )


PREREQUISITES FOR WORKING OF THE ABOVE FILE MONITORING SYSTEM - 
1)Install watchdog library using the command : pip install watchdog
   (If pip isn't available on the system , the installation procedure to install pip is mentioned in the below given video : https://youtu.be/fJKdIf11GcI?si=6sY-odhI1Qdiwb2B)
   
2)Install pytz library using the command : pip install pytz

3)Python IDE



                                      
  
              
        

                  
                                    

                


                  
                  

                  
