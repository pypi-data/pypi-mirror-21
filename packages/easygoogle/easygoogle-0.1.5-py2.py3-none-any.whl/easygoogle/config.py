from pickle import load, dump
from os.path import dirname, join
import logging
from re import compile as rExcompile, findall
from urllib.request import Request as req, urlopen as uopen

with open(join(dirname(__file__), 'apis.pk'), 'rb') as fl:
	apis = load(fl)

logger = logging.getLogger("easygoogle.configurator")

def config():
    prevnames = {y['scope']:x for x, y in apis.items()}
    
    pgdata =uopen(req('https://developers.google.com/api-client-library/python/apis/',
                      headers={'User-Agent': 'easyGoogle python api configurator'}))
    findings = findall(r"<td>(.+?)<\/td>\s+?<td>(.+?)<\/td>\s+?<td><a href=\"https:\/\/developers.google.com\/api-client-library.+?\">(.+?)<\/a><\/td>", pgdata.read().decode())
    
    logger.debug("Found %d" % len(findings))
    
    python_confirmed = {(x[0], x[2]):x for x in findings}
    
    pgdata = uopen(req('https://developers.google.com/identity/protocols/googlescopes',
                       headers={'User-Agent': 'easyGoogle python api configurator'}))
    
    rx_header = rExcompile("\\s*<h2.*?<a href=.*?\">(.+? API)</a>, (v.+?)</h2>")
    rx_scope = rExcompile("\\s*<tr><td>(.+?)</td>")
    
    while pgdata.length > 0:
        line = pgdata.readline().decode()
        match_header = rx_header.match(line)
        if match_header:
            logger.debug("Header found: %s --> %s" % match_header.group(1, 2))
            if match_header.group(1, 2) in python_confirmed:
                logger.debug("Header is valid")
                while True:
                    line = pgdata.readline().decode()
                    if line == "</table>\n":
                        break
                    
                    match_scope = rx_scope.match(line)
                    if match_scope:
                        setapiinfo(python_confirmed[match_header.group(1, 2)],
                                   match_scope.group(1),
                                   prevnames)

    with open('apis.pk', 'wb') as fl:
        dump(apis, fl)
                        
def setapiinfo(info, scope, prevconfig):
    scopecode = scope.split('/')[-1]
    if scope in prevconfig:
        name = prevconfig[scope]
    else:
        name = scopecode
    
    logger.info("Configuring scope \"%s\" for \"%s\"..." % (scopecode, info[0]))
    
    apis[name] = {'name': info[1],
                  'version': info[2],
                  'scope': scope}


if __name__=="__main__":
    import coloredlogs
    logging.basicConfig(level=logging.INFO, format="[%(name)-20s][%(levelname)-8s]:%(asctime)s: %(message)s")
    coloredlogs.install(level=logging.INFO)
    config()
