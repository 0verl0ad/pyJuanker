"""Usage: pyRobots.py --url=URL

Options:
    --url=URL  target url
    -h --help  show this screen
"""
import docopt
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def getDirectories(urlD):
    urlD = urlD + '/robots.txt'
    req = Request(urlD)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        directoryS = response.read().decode('utf-8')
        dirL = directoryS.split('\n')
        return dirL


def parseDirectories(directoriesList):
    validDir = {}
    for s in directoriesList:
        if (s.find("Disallow") != -1 and s[-1] == '/'):
            cad = s.split()
            validDir[cad[1]] = ''
    return validDir


def findDirectories(urlD, validDirectories):
    for d in validDirectories:
        u = urlD + d
        req = Request(u)
        try:
            response = urlopen(req)
        except HTTPError as e:
            validDirectories[d] = str(e.code) + '  ' + e.reason
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            validDirectories[d] = str(response.getcode()) + '  ' + response.reason
    return validDirectories


def printRes(urlD, validDirectories):
    i = 0
    for d in validDirectories:
        print(i, ' ->  ' + urlD + d + '         code: ', validDirectories[d])
        i += 1


if __name__ == '__main__':
    try:
        arguments = docopt.docopt(__doc__)
        urlD = arguments['--url']
    except docopt.DocoptExit as e:
        print(e)
    else:
        if(urlD[-1:] == '/'):
            urlD = urlD[:-1]
        if(urlD.find('http://') != -1):
            dirL = getDirectories(urlD)
        else:
            urlD = 'http://' + urlD
            dirL = getDirectories(urlD)
        if dirL:
            print()
            print('                 Site: ' + urlD)
            print('===========================================================')
            validD = parseDirectories(dirL)
            directories = findDirectories(urlD, validD)
            printRes(urlD, directories)
