# CS5302 Database Project
The following documentation describes how to (1) configure the version of the Lahman database that has been augmented using data provided by Retrosheets and (2) generate the web pages that were created for the CSI 5302 group project by the team consisting of Matthew Hayes, Sarah Smallwood, and Joshua Wellman.

Information regarding the original Lahman database can be found at: [lahman](https://www.seanlahman.com/files/database/readme2017.txt).
Original Retrosheets data can be found at: [retrosheets](https://retrosheet.org/).

> **NOTE:** When viewing the database through the web app, we are intentionally filtering out data prior to 1974, as this is as far back as we imported retrosheets data for.

## Recreate Database
All of the Database SQL files are located in *Documentation/SQL/*. The database will be dumped to *00-dump.sql*. If this file exists, you can recreate the entire database with it. In the event that it does not exist, all of the following SQL scripts will be necessary to recreate the database for development and need to be run in the following order:
1. 01-createDB.sql
1. 02-createAuth.sql
1. 03-lahman2019.sql
1. 04-pitchingAgainst.sql
1. 05-pitchingAnalytics.sql
1. 06-pitchingAnalyticsTrigger.sql
1. 07-pitchingAgainst_update.sql
   * *NOTE: This script will take approximately 10 minutes to run.*
1. 08-battingAnalytics.sql
1. 09-favorites.sql

> **Note:** For details on how data was imported from RetroSheets, see: (Documentation/Scripts/README.md)[./Documentation/Scripts/README.md]

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
In order to launch the web app, you will need to enter `flask run` from within the virtual environment. Flask will attempt to connect to the database using the following credentials:
* username: **web**
* password: **dbrules**
Once Flask connects to the database, open a web browser and go to `localhost:5000`.

## Navigating the Web App
When the web application loads, perform the following actions:
1. Navigate to the Register link in the upper right corner of the page and create an account.
   * You can register with any username and password you wish; it does not need to match that of your database login.
1. Once you are registered, navigate to the Login page and login to your account.
1. After creating an account, you can navigate to the Home page and search for a player to view their statistics


## Project Creation Notes -- do not include this in project submission

This repository is intended for us to work on the project together from a distance.

If you have any questions or trouble pushing/pulling/forking the repo, please let someone know.



###### Please use and merge branches so that we're not overwriting each other's work - or doing the same thing twice.

## Basic Git Usage

- Install Git [git-scm Install Site](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

- Use `$ git --version` to check install and version number.

- Use `$ git init` to start a local repository.

- Use `$ git remote add origin git@github.com:<YOUR-USERNAME>/CS5302.git` to add the remote repo to git.

- You can check the remotes you have saved by using `$ git remote show origin`

- Use `$ git pull origin main` to make a local copy of the main repository.

- Use `$ git checkout -b <branch-name>` to create a new local branch. The highlighted one is your current working branch.

- Use `$ git branch -a` to show all branches.

- Use `$ git push -u origin <YOUR-branch-name>` this will create a remote branch if none exists of the same name as your branch. We will review and merge code using the GitHub interface.

- If you make an accidental commit *locally*, you can reset it by using `$ git reset HEAD`. This will reset **1** commit backwards.

*Don't remove your branch until all merges on GitHub are complete*

- To merge locally Use `$ git merge --no-ff <branch-name>` Make sure you're in the branch you want to merge **into**.

- To remove a branch locally use `$ git branch -d <branch-name>`

*You can't delete a branch that is currently in use. Use* `$ git branch checkout master` *to change to the master (or main) branch before deletion.*

- You'll still have /remotes/origin/<branch-name> Remove with `$ git push origin --delete <brach-name>` **Warning this will delete the remote branch too!**

### Pre-Commit Hooks
A number of pre-commit hooks have been included to help keep our code neat and tidy. You must follow the guidance above to create a virtual environment and install the packages from *requirements.txt* to utilize pre-commit.

1. Install pre-commit: `pre-commit install`
1. Initially install hooks: `pre-commit run --all-files`

The hooks will run whenever you attempt to commit new files. You will not be able to commit unless you fix the errors that are indicated. You can run the individual hooks via:

* `black .`
* `flake8 .`
* `mypy .`

There may be times when you don't agree with **flake8**.  In these cases, it may be necessary to put `  # noqa` at the end of a line to avoid all errors.  If there is a specific error you want to avoid, you can mark it with `  # noqa: E1234` assuming the error was E1234.

#### Hooks
1. *Black* - Code Formatting
1. *Flake8* - Code Linting
1. *Mypy* - Type Checking

Additionally, there are a number of GitHub provided hooks that ensure trailing white-space is caught and configuration files (like *json* or *yaml*) are formatted correctly.
