import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
        print '\nSuccessfully read open milestones on '+url
        for miles in json.loads(response.content):
            ms[miles['title'].encode("utf-8",'replace')] = str(miles['number'])
    else:
        print 'Could not read milestone'
        print 'Response:', response.content
    return ms

def read_issues(milestone):
    base_url = 'https://api.github.com/repos/%s/%s/issues' % (config['REPO_OWNER'], config['REPO_NAME'])
    
    query = "?&milestone="+str(read_milestone()[milestone])+"&state=closed&sort=updated&direction=desc&per_page=100&page=1"
    url = base_url+query
    f = open(milestone+"-issues.csv", "w")
    f.write("url,id,milestone,status,title\n")
    Next = True
    while Next:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200 :
            print '\nSuccessfully read issues on '+url
            if response.links.has_key("next"):
                url = response.links["next"]["url"]
            else:
                Next = False
            for issue in json.loads(response.content):
                if issue.has_key("pull_request"):
                    pass
                else:
                    u = issue['html_url']
                    i = str(issue['number'])
                    if issue.has_key("milestone"):
                        im = issue['milestone']
                        #print json.dumps(im,indent=4, sort_keys=True)
                        im = {k: unicode(v).encode("utf-8",'replace') for k,v in im.iteritems()}
                        m = issue['milestone']['title']
                    else:
                        m = " "
                    s = issue['state']
                    t = issue['title']
                    f.write(u+","+i+","+m+","+s+","+t+"\n")
        else:
            Next = False
            print 'Could not read issues'
            print 'Response:', response.content


    f.close()

read_issues("9.1.0")