# This is based off of https://github.com/s0md3v/Zen
	
import re
import sys
import json
import argparse
import threading
from requests import get
from requests.auth import HTTPBasicAuth

i = '' # your GitHub username here
p = '' # your GitHub password here

def findContributorsFromRepo(username, repo):
	response = get('https://api.github.com/repos/%s/%s/contributors?per_page=100' % (username, repo), auth=HTTPBasicAuth(i, p)).text
	contributors = re.findall(r'https://github\.com/(.*?)"', response)
	return contributors

def findReposFromUsername(username):
	response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username, auth=HTTPBasicAuth(i, p)).text
	repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
	nonForkedRepos = []
	for repo in repos:
		if repo[1] == 'false':
			nonForkedRepos.append(repo[0])
	return nonForkedRepos

def findEmailFromContributor(username, repo, contributor):
	response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(i, p)).text
	latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
	if latestCommit:
		latestCommit = latestCommit.group(1)
	else:
		latestCommit = 'dummy'
	commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(i, p)).text
	email = re.search(r'<(.*)>', commitDetails)
	if email:
		email = email.group(1)
	return email

def findEmailFromUsername(username):
	repos = findReposFromUsername(username)
	for repo in repos:
		email = findEmailFromContributor(username, repo, username)
		return email or ''

def findEmailsFromRepo(username, repo):
	contributors = findContributorsFromRepo(username, repo)
	for contributor in contributors:
		email = (findEmailFromContributor(username, repo, contributor))
		if email:
			print (contributor + ' : ' + email)

def findUsersFromOrganization(username):
	response = get('https://api.github.com/orgs/%s/members?per_page=100' % username, auth=HTTPBasicAuth(i, p)).text
	members = re.findall(r'"login":"(.*?)"', response)
	return members


uname = [] #list of usernames
emails_dict = dict.fromkeys(uname,'')
for name in uname:
	email = findEmailFromUsername(name)
	emails_dict[name] = email
	print(name, email)
print(emails_dict)
