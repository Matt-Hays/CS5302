# CS5302 Database Project
The following documentation describes how to (1) configure the version of the Lahman database that has been augmented using data provided by Retrosheets and (2) generate the web pages that were created for the CSI 5302 group project by the team consisting of Matthew Hayes, Sarah Smallwood, and Joshua Wellman.

Information regarding the original Lahman database can be found at: [lahman](https://www.seanlahman.com/files/database/readme2017.txt).
Original Retrosheets data can be found at: [retrosheets](https://retrosheet.org/).

> **NOTE:** When viewing the database through the web app, we are intentionally filtering out data prior to 1974, as the project requirements did not require Retrosheets data prior to 1974.**

## Recreate Database
All of the Database SQL files are located in *Documentation/SQL/*. The database will be dumped to [00-dump.sql](./Documentation/SQL/00-dump.sql). If this file exists, you can recreate the entire database with it. In the event that it does not exist, all of the following SQL scripts will be necessary to recreate the database for development and need to be run in the following order:
1. [01-createDB.sql](./Documentation/SQL/01-createDB.sql)
1. [02-createAuth.sql](./Documentation/SQL/02-createAuth.sql)
1. [03-lahman2019.sql](./Documentation/SQL/03-lahman2019.sql)
1. [04-pitchingAgainst.sql](./Documentation/SQL/04-pitchingAgainst.sql)
1. [05-pitchingAnalytics.sql](./Documentation/SQL/05-pitchingAnalytics.sql)
1. [06-pitchingAnalyticsTrigger.sql](./Documentation/SQL/06-pitchingAnalyticsTrigger.sql)
1. [07-pitchingAgainst_update.sql](./Documentation/SQL/07-pitchingAgainst_update.sql)
   * *NOTE: This script will take approximately 10 minutes to run.*
1. [08-battingAnalytics.sql](./Documentation/SQL/08-battingAnalytics.sql)
1. [09-favorites.sql](./Documentation/SQL/09-favorites.sql)

> **Note:** For details on how data was imported from RetroSheets, see: [Documentation/Scripts/README.md](./Documentation/Scripts/README.md)

## Configuring the Virtual Environment
A virtual environment will allow for the installation of the required packages (as specified in *requirements.txt*). There are a number of ways to do this. One of the easiest ways is to use the [venv](https://docs.python.org/3/library/venv.html) module. You may have to install this first (`pip install venv`). Once installed:
1. Create a new virtual environment: `python3 -m venv venv`
1. Activate the new virtual environment on Linux: `source venv/bin/activate`
	* For Windows activation, run the **venv/bin/Activate.ps1** Powershell script.  If it won't run, you may have to adjust the Powershell Execution Policy via `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` from a Powershell prompt.
1. Install packages: `pip install -r requirements.txt`

### Necessary Packages - See requirements.txt
If you have to install new packages, make sure you have activated the virtual environment as described above.  Once activated:

```pip
pip install NEWPACKAGE
```

Make sure you update requirements.txt via:

```pip
pip freeze > requirements.txt
```

## Flask Setup
You will need two files to direct flask to your database:

#### .env
Create a file called **.env** with the following contents ensuring you update **YOURPASSWORD** with your actual password:

```text
DATABASE_URI="mysql+pymysql://web:YOURPASSWORD@localhost:3306/lahmansbaseballdb"
SECRET_KEY="ishouldreallychangethis"
```

#### .flaskenv
Create a file called **.flaskenv** with the following contents:

```
FLASK_ENV=development
FLASK_APP=main.py
```

## Launching the Web App with Flask
In order to launch the web app, you will need to enter `flask run` from within the virtual environment. If using the provided .env file, Flask will attempt to connect to the database with the following credentials:
* username: **web**
* password: **dbrules**

If creating your own .env using the directions in the previous section, Flask will use your provided username and password to connect to the database. Once Flask connects to the database, open a web browser and go to `localhost:5000`.

## Navigating the Web App
When the web application loads, perform the following actions:
1. Navigate to the Register link in the upper right corner of the page and create an account.
   * You can register with any username and password you wish; it does not need to match that of your database login.
2. Once you are registered, navigate to the Login page and login to your account.
3. After creating an account, you can navigate to the Home page and search for a player to view their statistics
   * A random player is presented on the Home page for viewing until you search for a player of your choice
4. To add a (searched for or randomly generated) player to your Favorites, click the `Add to Favorites` button.
5. Navigate to the Favorites page in the upper right to view your favorite players and re-load their data.

## Project Contents
The [ER Diagrams](./Documentation/ER_diagrams.pdf) for this project are located in the *Documentation* folder.
