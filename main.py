from __future__ import division
from subprocess import PIPE, Popen
import sys
import numpy as np
from numpy import median
import time as sysTime
import datetime
targetFolder = "cd ../commons-math/;"
totalFilesCmd = "find ./ -type f | wc -l"
authors = []
authorsInactive = []
totalCommits = 0
totalFilesCount = 0
def cmdline(command):
    # Init for cmdline operation
    process = Popen(
            args = command,
            stdout = PIPE,
            shell = True
            )
    return process.communicate()[0]
def getTotalFiles():
    global totalFilesCount
    cmd = targetFolder + 'find ./ -type f | wc -l'
    totalFilesCount = int(cmdline(cmd)[4:-1])
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

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def getAuthors():
    def getCommitName():
        cmd = targetFolder + 'git log --branches --pretty=format:"%H %aN" --before="2017-11-01"'
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
    cmd = targetFolder + 'git log --branches --name-only --before="2017-11-1"'
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
                "changedFilesCountByCommit":[],
                "commit":[],
                "stat":{
                    "commitCount":0,
                    "commitPercent":0,
                    "changedFilesCount":0,
                    "changedFilesPercent":0,
                    "changedFilesAvg":0,
                    "changedFilesMed":0,
                    "latestCommitTime":"",
                    "latestCommitTimeStamp":""
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
    def storeFilesInAuthors(commitName, FileName):
        global authors
        for author in authors:
            # print author['author']
            for commit in author['commit']:
                # print commit
                # print commitName
                if commit == commitName:
                    # print "can add files"
                    author['changedFiles'].append(FileName)

        # for author in authors:
            # author['changedFiles'] = list(set(author['changedFiles']))
    
    def storeFilesCountByEachCommitInAuthors(commitName, count):
        global authors
        for author in authors:
            for commit in author['commit']:
                if commit == commitName:
                    author['changedFilesCountByCommit'].append(count)
                    author['changedFilesCountByCommit'].sort()
    cmd = targetFolder + 'git log --branches --name-only --pretty=short --before="2017-11-01"'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for commit in commits:
        try:
            if commit.split('\n')[-2] == '' and commit.split('\n')[-1] == '':
                # print commit.split('\n')
                # print "Extract files from commit"
                count = 2
                changedFilesCount = 0
                commitName = list(reversed(commit.split('\n')))[-1]
                # print list(reversed(commit.split('\n')))
                while list(reversed(commit.split('\n')))[count] != '' and list(reversed(commit.split('\n')))[count][0] != ' ':
                    
                    # print list(reversed(commit.split('\n')))[count]
                    storeFilesInAuthors(list(reversed(commit.split('\n')))[-1], list(reversed(commit.split('\n')))[count])
                    changedFilesCount = changedFilesCount + 1
                    count = count + 1
                storeFilesCountByEachCommitInAuthors(list(reversed(commit.split('\n')))[-1], changedFilesCount)
            # else:
                # print commit.split('\n')[-2]
        except IndexError:
            print len(commit.split('\n'))
    
def getStatForAuthors():
    # print authors
    global totalCommits
    global totalFilesCount
    # print "hey"
    for author in authors:
        try:
            author['stat']['commitCount'] = len(author['commit'])
            # author['stat']['commitPercent'] = (1/totalCommits)
            author['stat']['commitPercent'] = (author['stat']['commitCount']/totalCommits)
            author['stat']['changedFilesCount'] = len(author['changedFiles'])
            author['stat']['changedFilesPercent'] = author['stat']['changedFilesCount']/totalFilesCount
            author['stat']['changedFilesMed'] = median(author['changedFilesCountByCommit'])
            author['stat']['changedFilesAvg'] = author['stat']['changedFilesCount'] / author['stat']['commitCount']
        except ZeroDivisionError:
            print "error"

    # print authors
def getInactiveAuthorsForSixMonths():
    def updateAuthorLatestTime(updateAuthor, updateTime):
        global authors
        for author in authors:
            if author['author'] == updateAuthor:
                author['stat']['latestCommitTime'] = updateTime
                author['stat']['latestCommitTimeStamp'] = sysTime.mktime(datetime.datetime.strptime(updateTime, "%Y-%m-%d").timetuple())
                
    def getTimeStamp():
        return null
    def getInactiveSinceTime():
        return null
    global authors
    cmd = targetFolder + 'git log --before="2017-11-01" --name-status --reverse --date=iso' 
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for commit in commits:
        # print commit.split('\n')
        # print commit
        try:    
            time = find_between( commit, 'Date:' ,':')[3:-3]
            author = find_between( commit, 'Author:' ,' <' )[1:]
            if time != '':
                updateAuthorLatestTime(author, time)
                # print author
                # print time
                # updateAuthorLatestTime( author, time)

                # print commit
        except IndexError:
            print "time is error"
            # print commit
        # print time[0]
        # print find_between( commit, 'Date: ',':' )[]
def printStat():
    global authors
    for author in authors:
        print "Author"
        print author['author']
        print author['stat']
        # print author['changedFiles']
        print author['changedFilesCountByCommit']
def main():
    
    targetIsGit()
    getTotalFiles()


    getAuthors()
    getChangedFilesByAuthors()
    getStatForAuthors()
    
    getInactiveAuthorsForSixMonths()
    # # print authors
    printStat()
    # print totalFilesCount
# This module is being run standalone.
if __name__ == "__main__": main()
