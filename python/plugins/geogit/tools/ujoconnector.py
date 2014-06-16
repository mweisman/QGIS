import requests
from geogit.gui import executor
from repodecorator import UjoRepository
import json

UJO_URL = "http://54.243.224.151/"
API_ENDPOINT = UJO_URL + "cli-api/"

def getUjoRepositories(user, password):
    def _getRepos():
        r = requests.get(API_ENDPOINT+ "users/%s/repos" % user, auth=(user, password))
        try:
            r.raise_for_status()
        except Exception, e:
            if "not found" in e.message.lower():
                if "User has no repos" in r.json()["message"].lower():
                    return []
                else:
                    raise AuthenticationException()
            else:
                raise e
        repos = r.json()  
        
        return [UjoRepository(API_ENDPOINT + "repos/%s/%s" % (user, repo["name"]), 
                              user, password, repo) for repo in repos]
    return executor.execute(_getRepos, "Retrieving Ujo repositories")


def createUjoRepository(user, password, name, title, description):
    def _createUjo():        
        data = {"name": name, "title": title, "description": description}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(API_ENDPOINT + "users/%s/repos" % user, 
                          data=json.dumps(data), headers=headers, auth=(user, password))
        r.raise_for_status()
        r = requests.get(API_ENDPOINT + "repos/%s/%s" % (user, name), auth=(user, password))
        r.raise_for_status()
        return UjoRepository(API_ENDPOINT + "repos/%s/%s" % (user, name), user, password, r.json())
    return executor.execute(_createUjo, "Creating Ujo repository")


class AuthenticationException(Exception):
    pass