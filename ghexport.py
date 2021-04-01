import sys
import requests
import json

with open('config.json', 'r') as j:
    config = json.load(j)
    print(config)

# Headers
headers = {
    "Authorization": "token %s" % config['TOKEN'],
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": config['USER_AGENT'],
}

def read_milestone():
    url = 'https://api.github.com/repos/%s/%s/milestones' % (config['REPO_OWNER'], config['REPO_NAME'])
    ms = {}
    
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200 :
        print('\nSuccessfully read open milestones on '+url)
        for miles in json.loads(response.content):
            #ms[miles['title'].encode("utf-8",'replace')] = str(miles['number'])
            ms[miles['title']] = str(miles['number'])
    else:
        print('Could not read milestone')
        print('Response:', response.content)
    print(ms)
    return ms

def read_issues(milestone):
    base_url = 'https://api.github.com/repos/%s/%s/issues' % (config['REPO_OWNER'], config['REPO_NAME'])
    
    query = "?&milestone="+str(read_milestone()[milestone])+"&state=closed&sort=updated&direction=desc&per_page=100&page=1"
    url = base_url+query
    f = open(milestone+"-issues.txt", "w")
    f.write("#id - title\n")
    Next = True
    while Next:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200 :
            print('\nSuccessfully read issues on '+url)
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                Next = False
            for issue in json.loads(response.content):
                if "pull_request" in issue:
                    pass
                else:
                    u = issue['html_url']
                    i = str(issue['number'])
                    if "milestone" in issue:
                        im = issue['milestone']
                        im = {k: v for k,v in im.items()}
                        m = issue['milestone']['title']
                    else:
                        m = " "
                    s = issue['state']
                    t = issue['title']
                    f.write("#"+i+" - "+t+"\n")
        else:
            Next = False
            print('Could not read issues')
            print('Response:', response.content)


    f.close()

read_issues("9.1.14")