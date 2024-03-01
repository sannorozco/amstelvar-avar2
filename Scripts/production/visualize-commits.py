import os, time
from git import Repo

folder = os.path.dirname(os.path.dirname(os.getcwd()))

R = Repo(folder)
assert not R.bare

# print(R)
# print(dir(R))
# print(R.references)
# print(R.refs)

lastCommits = list(R.iter_commits("main", max_count=50))

for commit in lastCommits:
    print(commit)
    print(commit.author)
    print(time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commit.authored_date)))
    tree = R.heads.main.commit.tree
    print(tree['Sources']['Roman']['AmstelvarA2-Roman_wght400.ufo'])
    # for entry in tree:
    #     print(entry)
    print()