#!/usr/bin/env python3

from github import Github

# First create a Github instance:

# using username and password
g = Github("OlegAnanyev", "jz7RJkottzmTMrbYs5w3")

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)