Directory: src/
Description: Contains the following OSNAP LOST web app demo source files.
             This application should be run with wsgi via Apache, NOT as direct Python script.

1. templates/ - directory containing the following .html source files
    1.1.  index.html - OSNAP LOST user login page, used as home page
    1.2.     rf.html - "Report Filter" page, lets user request desired report type
    1.3.    fir.html - "Facility Inventory Report" page, lists all assets at specified facility
    1.4.    itr.html - "In-Transit Report" page, lists all assets on specified route
    1.5. logout.html - User logout page, prompts to return to home

2. app.py - main Flask Python script for database integration with .html pages

3. config.py - python script for further configuration with json script

4. lost_config.json - json script for database configuration

5. lost.wsgi - wsgi script to run application

6. README.txt - this text file

NOTE: My sql imports are still not quite functional, so I used the sql/ directory
      from https://github.com/dellswor/lost for testing purposes.
