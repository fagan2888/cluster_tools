import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
from git import Repo
from datetime import datetime
from invoke import run

def pack(name, branch):
  # check if the repo is clean
  repo = Repo("./", search_parent_directories=True)
  diff = repo.index.diff(None)
  timestamp = datetime.now().strftime('%Y%m%d.%H%M%S')
  branch_name = repo.active_branch.name
  if branch:
    branch_name = branch
  exec_path = repo.git.rev_parse(show_prefix=True)
  if len(diff) > 0:
    repo.git.add('-u')
    repo.index.commit(f"[dirty] commit {timestamp}")
    ckpt_branch_name = f"{branch_name}.dirty/{timestamp}"
    tar_name = f"{name}-{branch_name}.dirty-{timestamp}"
    dirty_branch = repo.create_head(ckpt_branch_name, 'HEAD')
    prefix = f"{name}/{branch_name}.dirty/{timestamp}"
    with open(f"{tar_name}.tar", "wb") as f:
      repo.archive(f, format="tar", prefix=f"{prefix}/")
    repo.head.reset("HEAD~1")
  else:
    sha = repo.git.rev_parse("HEAD", short=True)
    if branch_name != repo.active_branch.name:
      ckpt_branch_name = f"{branch_name}.{sha}/{timestamp}"
      repo.create_head(branch_name, 'HEAD')
    tar_name = f"{name}-{branch_name}.{sha}-{timestamp}"
    prefix = f"{name}/{branch_name}.{sha}/{timestamp}"
    with open(f"{tar_name}.tar", "wb") as f:
      repo.archive(f, format="tar", prefix=f"{prefix}/")

  return f"{tar_name}.tar", prefix, exec_path

if __name__ == "__main__":
  print(pack())
