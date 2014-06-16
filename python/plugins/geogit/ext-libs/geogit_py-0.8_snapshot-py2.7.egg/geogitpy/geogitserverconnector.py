import re
import requests
from connector import Connector
from commit import Commit
import xml.etree.ElementTree as ET
from geogitexception import GeoGitException
import traceback

SHA_MATCHER = re.compile(r"\b([a-f0-9]{40})\b")

class GeoGitServerConnector(Connector):
    ''' A connector that connects to a geogit repo through a geogit-server instance'''

    def log(self, tip, sincecommit = None, until = None, since = None, path = None, n = None):                
        if since is not None or path is not None:
            raise NotImplementedError()
        if SHA_MATCHER.match(tip) is None:
            tip = self.revparse(tip)
        if sincecommit and SHA_MATCHER.match(sincecommit) is None:
            tip = self.revparse(sincecommit)            
        oldref = "?oldRefSpec=" + sincecommit if sincecommit else ""
        url = self.repo.url + "/commits?newRefSpec=%s%s" % (tip, oldref) 
        r = requests.get(url)
        r.raise_for_status()
        commits = r.json()['commits']
        log = []
        for c in commits:
            commit = Commit(self.repo, c['sha'], None, c['parent'], c['[message]'], 
                            c['author']['name'], c['author']['date'], c['committer']['name'], c['committer']['date'])
            log.append(commit)
        return log
    
    def checkisrepo(self):
        try:
            url = self.repo.url + '/commits'
            r = requests.get(url)
            response = r.json()
            return 'currentBranch' in reponse
        except:            
            return False
        
    def revparse(self, rev):
        try:
            url = self.repo.url + '/refparse'
            r = requests.get(url, params = {'name' : rev})
            root = ET.fromstring(r.text)            
            id = root.iter('objectId').next().text
            return id   
        except Exception, e:
            print traceback.format_exc()
            raise GeoGitException("Reference %s not found" % rev)
        
    @staticmethod
    def createrepo(url, name):
        r = requests.put(url, data = name)
        r.raise_for_status()
    