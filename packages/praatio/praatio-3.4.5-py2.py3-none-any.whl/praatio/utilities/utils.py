'''
Created on Oct 30, 2015

@author: tmahrt
'''

import os
from os.path import join
import subprocess
import functools
import io
from pkg_resources import resource_filename

# Get the folder one level above the current folder
scriptsPath = resource_filename("praatio", "praatScripts", )


def invertIntervalList(inputList, maxValue=None):
    '''
    Inverts the segments of a list of intervals
    
    e.g.
    [(0,1), (4,5), (7,10)] -> [(1,4), (5,7)]
    '''
    inputList = sorted(inputList)
    
    invList = [[inputList[i][1], inputList[i + 1][0]]
               for i in range(0, len(inputList) - 1)]
    
    if len(invList) > 0:
        if inputList[0][0] != 0:
            invList.insert(0, [0, inputList[0][0]])
            
        if maxValue is not None:
            if inputList[-1][1] != maxValue:
                invList.append([inputList[-1][1], maxValue])
    else:
        if maxValue is not None:
            invList.append([0, maxValue])
    
    return invList


def makeDir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        

def findAll(txt, subStr):
    
    indexList = []
    index = 0
    while True:
        try:
            index = txt.index(subStr, index)
        except ValueError:
            break
        indexList.append(int(index))
        index += 1
    
    return indexList


class FileNotFound(Exception):
    
    def __init__(self, fullPath):
        super(FileNotFound, self).__init__()
        self.fullPath = fullPath
    
    def __str__(self):
        return ("File not found:\n%s" % self.fullPath)


class PraatExecutionFailed(Exception):
    
    def __init__(self, cmdList):
        super(PraatExecutionFailed, self).__init__()
        self.cmdList = cmdList
    
    def __str__(self):
        errorStr = ("\nPraat Execution Failed.  Please check the following:\n"
                    "- Praat exists in the location specified\n"
                    "- Praat script can execute ok outside of praat\n"
                    "- script arguments are correct\n\n"
                    "If you can't locate the problem, I recommend using "
                    "absolute paths rather than relative "
                    "paths and using paths without spaces in any folder "
                    "or file names\n\n"
                    "Here is the command that python attempted to run:\n")
        cmdTxt = " ".join(self.cmdList)
        return errorStr + cmdTxt
    
    
def runPraatScript(praatEXE, scriptFN, argList, cwd=None):
    
    # Popen gives a not-very-transparent error
    if not os.path.exists(praatEXE):
        raise FileNotFound(praatEXE)
    if not os.path.exists(scriptFN):
        raise FileNotFound(scriptFN)
    
    argList = ["%s" % arg for arg in argList]
    cmdList = [praatEXE, '--run', scriptFN] + argList
    
    myProcess = subprocess.Popen(cmdList, cwd=cwd)
    
    if myProcess.wait():
        raise PraatExecutionFailed(cmdList)


def _getMatchFunc(pattern):
    '''
    An unsophisticated pattern matching function
    '''
    
    # '#' Marks word boundaries, so if there is more than one we need to do
    #    something special to make sure we're not mis-representings them
    assert(pattern.count('#') < 2)

    def startsWith(subStr, fullStr):
        return fullStr[:len(subStr)] == subStr
            
    def endsWith(subStr, fullStr):
        return fullStr[-1 * len(subStr):] == subStr
    
    def inStr(subStr, fullStr):
        return subStr in fullStr

    # Selection of the correct function
    if pattern[0] == '#':
        pattern = pattern[1:]
        cmpFunc = startsWith
        
    elif pattern[-1] == '#':
        pattern = pattern[:-1]
        cmpFunc = endsWith
        
    else:
        cmpFunc = inStr
    
    return functools.partial(cmpFunc, pattern)


def findFiles(path, filterPaths=False, filterExt=None, filterPattern=None,
              skipIfNameInList=None, stripExt=False):
    
    fnList = os.listdir(path)
       
    if filterPaths is True:
        fnList = [folderName for folderName in fnList
                  if os.path.isdir(os.path.join(path, folderName))]

    if filterExt is not None:
        splitFNList = [[fn, ] + list(os.path.splitext(fn)) for fn in fnList]
        fnList = [fn for fn, name, ext in splitFNList if ext == filterExt]
        
    if filterPattern is not None:
        splitFNList = [[fn, ] + list(os.path.splitext(fn)) for fn in fnList]
        matchFunc = _getMatchFunc(filterPattern)
        fnList = [fn for fn, name, ext in splitFNList if matchFunc(name)]
    
    if skipIfNameInList is not None:
        targetNameList = [os.path.splitext(fn)[0] for fn in skipIfNameInList]
        fnList = [fn for fn in fnList
                  if os.path.splitext(fn)[0] not in targetNameList]
    
    if stripExt is True:
        fnList = [os.path.splitext(fn)[0] for fn in fnList]
    
    fnList.sort()
    return fnList


def openCSV(path, fn, valueIndex=None, encoding="utf-8"):
    '''
    Load a feature
    
    In many cases we only want a single value from the feature (mainly because
    the feature only contains one value).  In these situations, the user
    can indicate that rather than receiving a list of lists, they can receive
    a lists of values, where each value represents the item in the row
    indicated by valueIndex.
    '''
    
    # Load CSV file
    with io.open(join(path, fn), "r", encoding=encoding) as fd:
        featureList = fd.read().splitlines()
    featureList = [row.split(",") for row in featureList]
    
    if valueIndex is not None:
        featureList = [row[valueIndex] for row in featureList]
    
    return featureList
