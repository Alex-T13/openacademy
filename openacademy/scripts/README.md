The behavior and principle of the script ("odoo_api_xml.py").
This script is designed to create sessions for courses via the API. 
Sessions must be created for 7 days, every two weeks. Script launch parameters:

usage: odoo_api_xml.py [-h] [-u URL] [-ns NUMBER_OF_SESSIONS] [-sd START_DATE] 
                        [-s SEATS] db user password

positional arguments:
  db                    database name
  user                  user name or email
  password              password

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     number of sessions (default=http://localhost:8069)
  -ns NUMBER_OF_SESSIONS, --number_of_sessions NUMBER_OF_SESSIONS
                        number of sessions (default=1)
  -sd START_DATE, --start_date START_DATE
                        start date of session ('YYYY-MM-DD')(default - today)
  -s SEATS, --seats SEATS
                        seats of session (default=10)

An approximate algorithm for the script:
    • checking the entered parameters
    • user authentication (if the attempt fails, display a message in the console)
    • checking the availability of instructors (there must be at least one instructor)
    • checking the availability of such a course (by name)
    • checking for the presence of the same sessions (to control the uniqueness of 
the start dates)
    • getting a list of start dates for sessions (for already created sessions with 
the same name) to avoid duplication of start dates for new sessions with existing ones 
(the start date must be at least one day different)
    • creating a new session or multiple sessions (depending on the entered parameters)
and outputting success or error messages to the console.



The behavior and principle of the script ("odoo_api_json.py").
This script is designed to create sessions for courses via the API. 
Sessions must be created for 10 days, every five weeks. Script launch parameters:

usage: odoo_api_json.py [-h] [-u URL] [-ns NUMBER_OF_SESSIONS] [-sd START_DATE] 
                        [-s SEATS] db user password

positional arguments:
  db                    database name
  user                  user name or email
  password              password

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     number of sessions (default=http://localhost:8069/jsonrpc)
  -ns NUMBER_OF_SESSIONS, --number_of_sessions NUMBER_OF_SESSIONS
                        number of sessions (default=1)
  -sd START_DATE, --start_date START_DATE
                        start date of session ('YYYY-MM-DD')(default - today)
  -s SEATS, --seats SEATS
                        seats of session (default=10)

The algorithm of this script is similar to the script ("odoo_api_json.py").



The behavior and principle of the script ("odoo_api_create_instructor_json.py").
This script is designed to create instructors for courses through the API. Instructors 
should be created with a logo or photo. Script launch parameters:

usage: odoo_api_create_instructor_json.py [-h] [-u URL] [-name INSTRUCTOR_NAME] 
                        [-pi PATH_TO_IMAGE] db user password

positional arguments:
  db                    database name
  user                  user name or email
  password              password

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     number of sessions (default - http://localhost:8069/jsonrpc)
  -name INSTRUCTOR_NAME, --instructor_name INSTRUCTOR_NAME
                        instructor name (default - Name unknown)
  -pi PATH_TO_IMAGE, --path_to_image PATH_TO_IMAGE
                        path to images (default: ~/image/image_1.png)


An approximate algorithm for the script:
     • checking the entered parameters
     • user authentication (if the attempt is unsuccessful, print a message to the console)
     • getting an ID of the category "teacher"
     • creation of a new instructor with the tag "teacher" and the logo or photo 
specified in the parameters
