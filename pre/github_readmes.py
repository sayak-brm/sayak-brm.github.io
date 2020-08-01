#!/usr/bin/python3

import sys, base64, datetime, json

import github
from github.GithubException import UnknownObjectException

def gen_readme(repo):
    readme_contents = base64.b64decode(repo.get_readme().content)

    title = bytes(repo.name, "UTF-8")
    title_loc = readme_contents.find(b"# ")
    if title_loc != -1:
        readme_title = readme_contents[title_loc+2:readme_contents.find(b"\n", title_loc)]
        if readme_title != '':
            title = readme_title

    with open(f"content/projects/{repo.name}.md", 'wb') as readme:
        readme.write(b"---\ntitle: ")
        readme.write(title)
        if repo.description is not None:
            readme.write(b"\nsubtitle: ")
            readme.write(bytes(repo.description, "utf8"))
        readme.write(b"\ndate: ")
        readme.write(bytes(repo.pushed_at.strftime("%Y-%m-%dT%H:%M:%S+05:30"), "utf8"))
        readme.write(b"\ndraft: false\ntoc: true\ntags: \n")
        for topic in repo.get_topics():
            readme.write(bytes(f"  - {topic}\n", "utf8"))
        readme.write(b"---\n\n")

        readme.write(readme_contents)

        readme.write(b"\n---\n\n")
        readme.write(bytes(f"*Contents automatically generated from [GitHub]({repo.html_url}).*\n", "utf8"))

if len(sys.argv)<3:
    print("Invalid Arguments")
    exit(1)

username = sys.argv[1]
gh = github.Github(sys.argv[2])

exceptions = json.load(open("pre/github_readmes_exceptions.json"))

for repo in gh.get_user().get_repos():
    if not repo.private and not repo.fork and repo.name not in exceptions:
        try:
            gen_readme(repo)
            print(f"Generated page for {gh.get_user().login}/{repo.name}")
        except UnknownObjectException:
            pass
