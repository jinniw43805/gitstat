from __future__ import division
from subprocess import PIPE, Popen
import sys
import numpy as np
targetFolder = "cd ../commons-math/;"
authors = []
totalCommits = 0
def cmdline(command):
    # Init for cmdline operation
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
    return branch

def getAuthors():
    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
    def getCommitName():
        cmd = targetFolder + 'git log --branches --pretty=format:"%H %aN"'
        commits = []
        info = []
        for char in cmdline(cmd):
            commits.append(char)
        commits = ''.join(commits).split('\n')
        for line in commits:
            commitName = line.split(' ')[0]
            authorName = line[line.index(' '):]
            newObj = {
                    "authorName":authorName[1:],
                    "commitName":commitName
                    }
            info.append(newObj)

        return info
        # search author object and put into commit name
    # getCommitName()
    authorNames = []
    commitNames = []
    cmd = targetFolder + 'git log --branches --name-only'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    # print commits
    # print find_between( commits[-1], 'Author: ', ' <')
    for author in commits:
        # print author.index("\n")
        # commitNames.append( find_between( author, '','\n' ) )       
        authorNames.append( find_between( author, 'Author: ', ' <'))
    # print commits
    # print len(list(set(authors)))
    
    authorNames = list(set(authorNames))
    
    

    for newAuthorName in authorNames:
        newAuthorObj = {
                "author":newAuthorName,
                "changedFiles":[],
                "commit":[],
                "stat":{
                    "commitCount":0,
                    "commitPercent":0
                    }
        }
        authors.append(newAuthorObj)

    # print authors
    commitInfo = getCommitName()
    global totalCommits
    for commit in commitInfo:
        for authorObj in authors:
            # print commit['authorName']
            # print commit['authorName']
            # print authorObj['author']
            if commit['authorName'] == authorObj['author']:
                authorObj['commit'].append(commit['commitName'])
                totalCommits = (totalCommits + 1)
                # print "Can not append"
    return authors
def getChangedFilesByAuthors():
    cmd = targetFolder + 'git log --branches --name-only'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    # print commits[-1]
def getStatForAuthors():
    # print authors
    global totalCommits
    # print "hey"
    for author in authors:
        author['stat']['commitCount'] = len(author['commit'])
        # author['stat']['commitPercent'] = (1/totalCommits)
        author['stat']['commitPercent'] = (author['stat']['commitCount']/totalCommits)
    # print authors
def printStat():
    global authors
    for author in authors:
        print author['author']
        print author['stat']

def main():
    
    targetIsGit()
    # getAllBranchesName()
    getAuthors()
    authors = getChangedFilesByAuthors()
    getStatForAuthors()
    
    # print authors
    printStat()
# This module is being run standalone.
if __name__ == "__main__": main()
