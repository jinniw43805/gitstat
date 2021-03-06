from __future__ import division
from subprocess import PIPE, Popen
import sys
import numpy as np
from numpy import median
import time as sysTime
import datetime
import csv
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
def targetIsGit():
    """Return true if targer folder is git folder, other wise return false"""
    cmd = targetFolder + 'git rev-parse --is-inside-work-tree'
    if cmdline(cmd)[:4] == "true":
        print "Can find git target folder, Analyzing..."
    else:
        print("Cannot find git target, exit the program")
        sys.exit();

def getAllBranchesName():
    """Return all branches of repository"""
    cmd = targetFolder + 'git branch -a'
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
        cmd = targetFolder + 'git log --all --branches --pretty=format:"%H %aN" --before="2017-11-01"'
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
    emails = []
    commitNames = []
    cmd = targetFolder + 'git log --all --branches --name-only --before="2017-11-1"'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for author in commits:
        authorNames.append( find_between( author, 'Author: ', ' <'))
    authorNames = list(set(authorNames))
    # emails = list(set(emails))
    for newAuthorName in authorNames:
        newAuthorObj = {
                "author":newAuthorName,
                "email":"",
                "changedFiles":[],
                "changedFilesCountByCommit":[],
                "changedFilesTypeCountByCommit":[],
                "commit":[],
                "stat":{
                    "commitCount":0,
                    "commitPercent":0,
                    "changedFilesCount":0,
                    "changedFilesPercent":0,
                    "changedFilesAvg":0,
                    "changedFilesMed":0,
                    "latestCommitTime":"",
                    "latestCommitTimeStamp":"",
                    "M":0,
                    "D":0,
                    "A":0,
                    "Mavg":0,
                    "Davg":0,
                    "Aavg":0,
                    "Mmed":0,
                    "Dmed":0,
                    "Amed":0
                    }
        }
        authors.append(newAuthorObj)

    commitInfo = getCommitName()
    global totalCommits
    for commit in commitInfo:
        for authorObj in authors:
            if commit['authorName'] == authorObj['author']:
                authorObj['commit'].append(commit['commitName'])
                totalCommits = (totalCommits + 1)
    return authors
def getChangedFilesByAuthors():
    def storeFilesInAuthors(commitName, FileName):
        global authors
        for author in authors:
            for commit in author['commit']:
                if commit == commitName:
                    author['changedFiles'].append(FileName)

    def storeFilesCountByEachCommitInAuthors(commitName, count):
        global authors
        for author in authors:
            for commit in author['commit']:
                if commit == commitName:
                    author['changedFilesCountByCommit'].append(count)
                    author['changedFilesCountByCommit'].sort()
    cmd = targetFolder + 'git log --all --branches --name-only --pretty=short --before="2017-11-01"'
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for commit in commits:
        try:
            if commit.split('\n')[-2] == '' and commit.split('\n')[-1] == '':
                count = 2
                changedFilesCount = 0
                commitName = list(reversed(commit.split('\n')))[-1]
                while list(reversed(commit.split('\n')))[count] != '' and list(reversed(commit.split('\n')))[count][0] != ' ':
                    
                    storeFilesInAuthors(list(reversed(commit.split('\n')))[-1], list(reversed(commit.split('\n')))[count])
                    changedFilesCount = changedFilesCount + 1
                    count = count + 1
                storeFilesCountByEachCommitInAuthors(list(reversed(commit.split('\n')))[-1], changedFilesCount)
            # else:
        except IndexError:
            print len(commit.split('\n'))
    
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
    cmd = targetFolder + 'git log --all --before="2017-11-01" --name-status --reverse --date=iso' 
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for commit in commits:
        try:    
            time = find_between( commit, 'Date:' ,':')[3:-3]
            author = find_between( commit, 'Author:' ,' <' )[1:]
            if time != '':
                updateAuthorLatestTime(author, time)
        except IndexError:
            print "time is error"
def getChangedFilesTypeByAuthor():
    def isFilesLine(line):
        if (line[0] == "D" or line[0] == "M" or line[0]== "A") and line[1] == "\t":
            return True
        else:
            return False
    def FileType(line):
        return line[0]
        
        # return True
    def storeFilesTypesOfEachCommitInAuthors(authorName, typeObj):
        global authors
        for author in authors:
            if author['author'] == authorName:
                author['changedFilesTypeCountByCommit'].append(typeObj)
        # return True
    def storeFilesTypesOfEachCommitInTypeObj(typeObj, fileType):
        if fileType == "M":
            typeObj['commit']['M'] = typeObj['commit']['M'] + 1
        elif fileType == "D":
            typeObj['commit']['D'] = typeObj['commit']['D'] + 1
        elif fileType == "A":
            typeObj['commit']['A'] = typeObj['commit']['A'] + 1
        else:
            print "FileType is error"
        return typeObj
        # return True
    
    cmd = targetFolder + 'git log --all --before="2017-11-01" --name-status --reverse --date=iso' 
    commits = []
    for char in cmdline(cmd):
        commits.append(char)
    commits = ''.join(commits).split('commit ')
    for commit in commits:
        # get author name
        authorName = find_between( commit, 'Author:', ' <' )[1:]
        typeObj = {
                "author":authorName,
                "commit":{
                    "M":0,
                    "D":0,
                    "A":0
                    }
                }
        for eachLine in commit.split('\n'):
            try:
                
                if isFilesLine(eachLine) == True:
                    fileType = FileType(eachLine)
                    typeObj =storeFilesTypesOfEachCommitInTypeObj(typeObj, fileType)

            except IndexError:
                # ChangeLineSymbol
                eachLine
                # print "IndexError"
        storeFilesTypesOfEachCommitInAuthors(authorName, typeObj)
def getStatForAuthors():
    def getStatM(author):
        mCount = 0
        medArray = []
        for eachCommit in author['changedFilesTypeCountByCommit']:
            mCount = mCount + int(eachCommit['commit']['M'])
            medArray.append(int(eachCommit['commit']['M']))
        author['stat']['M'] = mCount
        medArray.sort()
        author['stat']['Mmed'] = median(medArray)
        
        return author

    def getStatA(author):
        mCount = 0
        medArray = []
        for eachCommit in author['changedFilesTypeCountByCommit']:
            mCount = mCount + int(eachCommit['commit']['A'])
            medArray.append(int(eachCommit['commit']['A']))
        author['stat']['A'] = mCount
        medArray.sort()
        author['stat']['Amed'] = median(medArray)

        return author
    def getStatD(author):
        mCount = 0
        medArray = []
        for eachCommit in author['changedFilesTypeCountByCommit']:
            mCount = mCount + int(eachCommit['commit']['D'])
            medArray.append(int(eachCommit['commit']['D']))
        author['stat']['D'] = mCount
        medArray.sort()
        author['stat']['Dmed'] = median(medArray)

        return author
    global totalCommits
    global totalFilesCount
    for author in authors:
            author['stat']['changedFilesCount'] = len(author['changedFiles'])
            totalFilesCount = totalFilesCount + author['stat']['changedFilesCount']
    for author in authors:
        try:
            author['stat']['commitCount'] = len(author['commit'])
            # author['stat']['commitPercent'] = (1/totalCommits)
            author['stat']['commitPercent'] = (author['stat']['commitCount']/totalCommits)
            author['stat']['changedFilesPercent'] = author['stat']['changedFilesCount']/ totalFilesCount
            author['stat']['changedFilesMed'] = median(author['changedFilesCountByCommit'])
            author['stat']['changedFilesAvg'] = author['stat']['changedFilesCount'] / author['stat']['commitCount']

            author = getStatM(author)
            author = getStatD(author)
            author = getStatA(author)
            author['stat']['Mavg'] = author['stat']['M'] / author['stat']['commitCount']
            author['stat']['Davg'] = author['stat']['D'] / author['stat']['commitCount']
            author['stat']['Aavg'] = author['stat']['A'] / author['stat']['commitCount']
        except ZeroDivisionError:
            print "error"

def printStat():
    global authors
    for author in authors:
        print "Author"
        print author['author']
        print author['stat']
        # print author['changedFiles']
        print "changedFilesCountByCommit"
        print author['changedFilesCountByCommit']
        print author['changedFilesTypeCountByCommit']
        # print author['stat']['Mmed']
        # print author['stat']['Amed']
        # print author['stat']['Dmed']

def writeTocsv():
    global totalCommits
    global totalFilesCount
    with open('result.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(['Author', 'commit', '', 'FileChange', '', '', '', 'latestCommitTime', 'latestTimeStamp'])
        csvwriter.writerow(['', '#', '%', '#', '%', 'Avg.' ,'Med.'])
        for author in authors:
            length = len(author['author'])
            # csvwriter.set_column(csvwriter.writerow().index,1,len)
            csvwriter.writerow([author['author'], 
            author['stat']['commitCount'],
            '{:.2%}'.format(author['stat']['commitPercent']),
            author['stat']['changedFilesCount'],
            '{:.2%}'.format(author['stat']['changedFilesPercent']),
            format( author['stat']['changedFilesAvg'], '.2f'),
            author['stat']['changedFilesMed'],
            author['stat']['latestCommitTime']
            ])

        csvwriter.writerow(['totalCommits', totalCommits])
        csvwriter.writerow(['totalFilesChanged', totalFilesCount])
        
def writeTocsv2():
    global totalCommits
    global totalFilesCount
    with open('result2.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(['Developer','Avg', '', '','Median', '', ''])
        csvwriter.writerow(['','Added','Modified','Deleted','Added','Modified','Deleted'])

        for author in authors:
            # csvwriter.set_column(csvwriter.writerow().index,1,len)
            csvwriter.writerow(
            [author['author'], 
            format(author['stat']['Aavg'], '.2f'),
            format(author['stat']['Mavg'], '.2f'),
            format(author['stat']['Davg'], '.2f'),
            author['stat']['Amed'],
            author['stat']['Mmed'],
            author['stat']['Dmed']])        
def main():
    
    targetIsGit()


    getAuthors()
    getChangedFilesByAuthors()
    
    getInactiveAuthorsForSixMonths()
    getChangedFilesTypeByAuthor()
    
    
    getStatForAuthors()
    # # print authors
    printStat()
    writeTocsv()
    writeTocsv2()
    # print totalFilesCount
# This module is being run standalone.
if __name__ == "__main__": main()
