# import subprocess
import sys
from subprocess import PIPE, Popen
targetFolder = "cd ../commons-math/;"
authors = []
def cmdline(command):
    process = Popen(
            args = command,
            stdout = PIPE,
            shell = True
            )
    return process.communicate()[0]

def targetIsGit():
    """Return true if targer folder is git folder, other wise return false"""
    cmd = targetFolder + 'git rev-parse --is-inside-work-tree'
    if cmdline(cmd)[:4] == "true":
        print "Can find git target folder, Analyzing..."
    else:
        print("Cannot find git target, exit the program")
        sys.exit();
    # print subprocess.check_output(cmd,shell = True)
def getAllBranchesName():
    """Return all branches of repository"""
    cmd = targetFolder + 'git branch -a'
    # print cmdline(cmd)
    
    branchesName = []
    for char in cmdline(cmd):
        branchesName.append(char)
    branchesName = branchesName[:-2]
    branch = ''.join(branchesName).split('\n  ')
    # print branch
# def getAllBranchesCommits():

def getAuthors():
    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    cmd = targetFolder + 'git log --branches --name-only'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    # print commits
    # print find_between( commits[-1], 'Author: ', ' <')
    for author in commits:
        
        authors.append( find_between( author, 'Author: ', ' <'))
    # print authors
    print len(list(set(authors)))
# def getCommitFromBranches():
    
# # def get
def main():
       
    targetIsGit()
    # getAllBranchesName()
    getAuthors()
# This module is being run standalone.
if __name__ == "__main__": main()
