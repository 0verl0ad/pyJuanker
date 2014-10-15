#
#	Database provided by MaxMind -- http://www.maxmind.com
#
"""Usage: pyGeo.py [--ip=IP] [--l=ipList]

Options:
    --ip=IP     IP direction.
    --l=ipList  IP list to generate a kml file.
    -h --help   Show this screen.
"""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import docopt
import os.path
import gzip
import pygeoip
import simplekml

def findDb():
    if (os.path.exists('db') is False):
        os.mkdir('db')

    if (os.path.exists('db/GeoLiteCity.dat') is False):
        print('Downloading GeoDatabase...')
        urlDb = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz'
        req = Request(urlDb)
        try:
            f = urlopen(req)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            data = f.read()
            with open("db/GeoLiteCity.dat.gz", "wb") as code:
                code.write(data)
            f.close()

            print('Decompressing GeoDatabase...')
            inF = gzip.GzipFile('db/GeoLiteCity.dat.gz', 'rb')
            s = inF.read()
            inF.close()
            outF = open('db/GeoLiteCity.dat', 'wb')
            outF.write(s)
            outF.close()
            os.remove('db/GeoLiteCity.dat.gz')


def getData(ipDir):
    gi = pygeoip.GeoIP('db/GeoLiteCity.dat')
    rec = gi.record_by_name(ipDir)
    return rec

def readIpList(fName):
    with open(fName, encoding='utf-8') as f:
        fCon = f.read()
    return fCon.split('\n')
    
def main():
    try:
        arguments = docopt.docopt(__doc__)
        ipDir = arguments['--ip']
        fName = arguments['--l']
    except docopt.DocoptExit as e:
        print(e)
    else:
        findDb()
        if arguments["--ip"]:
            rec = getData(ipDir)
            print()
            print('                 IP: ' + ipDir)
            print('===============================================================')
            print('Ciudad: ' + rec['city'])
            print('Pais: ' + rec['country_name'])
            print('Continente: ' + rec['continent'])
            print('Longitud: ' + str(rec['longitude']))
            print('Latitud: ' + str(rec['latitude']))
            print()
        elif arguments["--l"]:
            kml = simplekml.Kml()
            m = []
            fCon = readIpList(fName)
            for d in fCon:
                #m.append([d, getData(d)['longitude'], getData(d)['latitude']])
                kml.newpoint(name=d, coords=[(getData(d)['longitude'],getData(d)['latitude'])])  # lon, lat, optional height
            kml.save("map.kml")
            print()
            print('KML file generated')
            print()

if __name__ == '__main__':
    main()
