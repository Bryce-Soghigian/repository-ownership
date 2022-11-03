from collections import defaultdict, deque
import typing
import requests
class Contributor:
    def __init__(self, github_username, orgs_url):
        self.github_username = github_username
        self.orgs_url = orgs_url



class Graph:

    def __init__(self):
        self.state = defaultdict(set) # contributor_name -> Repos they are in, org that repo is in
        self.repos_to_org = defaultdict()
        self.repos = defaultdict(set)
        self.orgs_to_explore = set()
        self.seen_orgs = set()

    def _retrieve_repos_in_org(self, org_url: str):
        auth_obj = ('bryce-soghigian','<Personal access token>')
        response = requests.get(org_url, auth=auth_obj).json()

        # repo -> contributors 
        
        for repo in response:
            repo_name =repo["name"]   
            contributor_list_url = repo["contributors_url"]
            self._retrieve_contributors(contributor_list_url,org_url, repo_name,  auth_obj)
            self.repos_to_org[repo_name] = org_url
            self.seen_orgs.add(org_url)

    def _retrieve_contributors(self, url, org_url, repo_name, auth_obj):
        print("exploring contributors in repo:", repo_name, "For org:", org_url)
        response = requests.get(url, auth=auth_obj).json()
        
        for contributor in response:
            contributor_name = contributor["login"]
            self.state[contributor_name].add(repo_name)
            self.repos[repo_name].add(contributor_name)
            self.add_orgs_to_explore(contributor["organizations_url"], auth_obj)
    
    def add_orgs_to_explore(self, orgs_url, auth_obj):

        # iterate through orgs, check if we still havent explored them yet.
        response = requests.get(orgs_url, auth=auth_obj).json()
        for org in response:
            curr_org_url = f'https://api.github.com/orgs/{org["login"]}/repos'
            if curr_org_url not in self.seen_orgs:
                self.orgs_to_explore.add(curr_org_url)




    def __call__(self, starting_org: str):
        org_url = f'https://api.github.com/orgs/{starting_org}/repos'
        self.seen_orgs.add(org_url)
        # 1. Retrieve intital orgs 
        self._retrieve_repos_in_org(org_url)

        while len(self.orgs_to_explore) != 0:
            print("CURRENT GRAPH", self.state)
            #1. explore all orgs. in current orgs to explore
            for org in self.orgs_to_explore.copy():
                self._retrieve_repos_in_org(org)

graph = Graph()
graph("usgo")
