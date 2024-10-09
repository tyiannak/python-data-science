
# Virtual environments
## using the existing requirements:
```
virtualenv -p python3.9 venv
source venv/bin/activate
pip3 install numpy==1.20.3
python3 deleteme.py
```

To save our own requirements we either do it manually by editing the requirements file or we do:
```
pipreqs .
```

Notes:
 * we suppose that before that we first create the virtual `env` and we activate it as above, and then we manually pip install the requirements one by one) 
 * the results is saved in `requirements.txt` by default
 * we share the `requirements.txt` in the repo along with our code
 * για να βγω απο το virtual environment κάνω απλα deactivate 

# git / github

## download the repo code (clone repo):
```
git clone https://github.com/tyiannak/python-data-science.git
```

## then we do changes in the code locally (using our IDE and testing)

## see the changes we have done locally:
```
git status
```
or 
```
git status .
```

or see changes in particular files:
```
git diff <some_file>
```
## steps to add a new file in the repo:
 * first we create and/or edit a file (say, `TODOs`) 
 * `git add TODOs` (can add more than one file)
 * `git commit -m "added a TODOs list and initated it with a first TODO message"`
 * `git push` (this sends the changes to the repo)

## to get the changes locally:
 * `git pull`: get latest version of current branch (see bellow for branches!)
 * `git checkout <some_branch`: select branch (see bellow for branches!)


## Github Project example
1. Create a new project
2. Add a new task and convert it to "issue"
3. Select issue to work on and drag it to "ongoing"
4. Open the issue and "create a new branch"
5. `git fetch` locally to get list of branches
6. `git checkout <name_of_the_branch_i_created>` locally to "enable" the selected branch
7. work locally to do the required changes on the code of the selected branch and repeat the aforementioned procedure (git add, git commit, git push ON THE BRANCH). 
8. as soon as i am sure the work is done --> pull request on github page (also mentions coworkers to do the QA. Also drag the issue from Ongoing to QA in the project view)
9. The person(s) that have been tagged to QA, checkout (git-checkout) the branch locally, they test it, and as soon as they are sure the code works without any bugs or new issues, they merge to master (through the github page). After this, automatically: the issue is deleted and the task is moved to "Done" in the project view

Summary of steps for a single task/issue:
task / issue --> branch --> work on branch locally --> push changes to branch and P(ull) R(equest) when ready --> the person(s) that do the QA do the final merging of the branch to master

## Example for a small excercise for 2-persons teams:
 * person A creates a new github repo. Adds person B as "collaborator".
 * persons A and B create a "project",  add a QA column before DONE 
 * persons A and B create two dummy tasks and convert them to "issues" in the project view
 * person A works on the first dummy issue: (drag to ongoing, create branch, checkout branch locally, add a new dummy file, git add file, git commit, git push). And finally creates a PR (pull request) in github and tags person B
 * person B works on the second dummy issue: (drag to ongoing, create branch, checkout branch locally, add a new dummy file, git add file, git commit, git push). And finally creates a PR (pull request) in github and tags person A
 * persons A and B check second and first issues (PRs) respectively, and if they agree merge the changes to master



