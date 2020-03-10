# Reddit Post Microservice

## Prerequisites 
* Make sure that Flask is installed. If it is not, enter the following command: **pip3 install Flask**
  * **Note:** This microservice was developed using Python 3
* In order to use the .env file, you must have python-dotenv installed. To do so, enter the following command: **pip3 install python-dotenv**
* In order to make use of the **request** module, it must be installed. To do so, enter the following command: **pip3 install requests**

## Instructions
1. Clone repository
2. If running for the first time, navigate to the directory where you saved this project and type: **sqlite3 reddit.db < reddit.sql**
  * **Note:** This will generate the reddit.db file
3. Enter the following command: **flask run**
4. In order to test the microservice, you can either use the scripts provided or test using your own curl commands
  * **Note:** You must open one terminal window for **flask run** command and another terminal window for testing the scripts or **CURL** commands
  * Command to run a script: **sh filename.sh**

  
