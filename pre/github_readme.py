#!/usr/bin/python3

import sys, base64, datetime, json

import github
from github.GithubException import UnknownObjectException

def gen_readme(user, repo):
    readme_contents = base64.b64decode(repo.get_readme().content)
    titles = json.load(open("pre/github_readme/titles.json"))
    paths = json.load(open("pre/github_readme/paths.json"))

    title = bytes(repo.name, "UTF-8")
    if repo.full_name in titles.keys():
        title = bytes(titles[repo.full_name], "UTF-8")
    else:
        title_loc = readme_contents.find(b"# ")
        if title_loc != -1:
            readme_title = readme_contents[title_loc+2:readme_contents.find(b"\n", title_loc)]
            if readme_title != '':
                title = readme_title

    path = repo.name 
    if repo.full_name in paths.keys():
        path = paths[repo.full_name]
    if repo.fork or repo.owner.login != user.login:
        path = f"oss/{path}"
    path = f"content/projects/{path}.md"

    with open(path, 'wb') as readme:
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

def main():
    if len(sys.argv)<3:
        print("Invalid Arguments")
        exit(1)

    gh = github.Github(sys.argv[1])

    exceptions = json.load(open("pre/github_readme/exceptions.json"))
    oss_repos = json.load(open("pre/github_readme/oss.json"))
    repos = []

    for repo in gh.get_user().get_repos(type="public"):
        repos.append(repo)
    for repo_name in oss_repos:
        repos.append(gh.get_repo(repo_name))

    for repo in repos:
        if not repo.private and repo.full_name not in exceptions:
            try:
                gen_readme(gh.get_user(), repo)
                print(f"Generated page for {gh.get_user().login}/{repo.name}")
            except UnknownObjectException:
                pass

main()
