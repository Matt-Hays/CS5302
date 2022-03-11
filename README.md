# CS5302 Database Project

#### Necessary Packages - See requirements.txt

This repository is intended for us to work on the project together from a distance. 

If you have any questions or trouble psuhing/pulling/forking the repo, please let someone know.

###### Please use and merge branches so that we're not overwriting each other's work - or doing the same thing twice.

###### Basic Git Usage

- Install Git [git-scm Install Site](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

- Use `$ git --version` to check install and version number.

- Use `$ git init` to start a local repository.

- Use `$ git remote add origin git@github.com:<YOUR-USERNAME>/CS5302.git` to add the remote repo to git.
  
- You can check the remotes you have saved by using `$ git remote show origin`

- Use `$ git pull origin main` to make a local copy of the main repository.

- Use `$ git checkout -b <branch-name>` to create a new local branch. The hightlighted one is your current working branch.
  
- Use `$ git branch -a` to show all branches.

- Use `$ git push -u origin <YOUR-branch-name>` this will create a remote branch if none exists of the same name as your branch. We will review and merge code using the GitHub interface.

- If you make an accidental commit *locally*, you can reset it by using `$ git reset HEAD`. This will reset **1** commit backwards.

*Don't remove your branch until all merges on GitHub are complete*

- To merge locally Use `$ git merge --no-ff <branch-name>` Make sure you're in the branch you want to merge **into**.

- To remove a branch locally use `$ git branch -d <branch-name>`

*You can't delete a branch that is currently in use. Use* `$ git branch checkout master` *to change to the master (or main) branch before deletion.*

- You'll still have /remotes/orgin/<branch-name> Remove with `$ git push origin --delete <brach-name>` **Warning this will delete the remote branch too!**
