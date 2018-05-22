from git import Repo
from datetime import datetime
from invoke import run

def pack():
  # check if the repo is clean
  repo = Repo("./", search_parent_directories=True)
  diff = repo.index.diff(None)
  timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
  branch_name = repo.active_branch.name
  relative_dir = repo.git.rev_parse(show_prefix=True)
  if len(diff) > 0:
    repo.git.add('-u')
    repo.index.commit(f"[dirty] commit {timestamp}")
    name = f"{branch_name}-dirty-{timestamp}"
    dirty_branch = repo.create_head(name, 'HEAD')
    with open(f"{name}.tar", "wb") as f:
      repo.archive(f, format="tar", prefix=f"{name}/")
    repo.head.reset("HEAD~1")
  else:
    sha = repo.git.rev_parse("HEAD", short=True)
    name = f"{branch_name}-{sha}-{timestamp}"
    with open(f"{name}.tar", "wb") as f:
      repo.archive(f, format="tar", prefix=f"{name}/")

  return f"{name}.tar", relative_dir

if __name__ == "__main__":
  print(pack())
