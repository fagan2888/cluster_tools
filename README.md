# Cluster Tools
a submit command that works from one's local machine.

## Installation
```shell
pip install git+ssh://git@github.com/mavenlin/cluster_tools.git#egg=cluster_tools
```

## Use
```shell
cd /path/to/main.py
submit -c=cedar.json python main.py
```
#### Tips
- `/path/to/main.py` needs to be within a git repo. The submit command will find the root of the git repo and do a `git archive` to make tarball out of the repo. An `sbatch_script.sh` is generated and packaged into the tarball, and the tarball will be send to the server for execution.
  - If the git repo is not clean, a dirty branch will be automatically created to store the status of the code at the time of execution. This will have no effect on your working copy of the code. But you can always find the submitted version of code in the future.
- send a `--sbatch_json={"--mem": "20G", ... }` argument if you want to change the sbatch options. The default option is in the `cedar.json` file.
- `--tensorboard` flag controls whether a tensorboard process needs to be launched together with the job under the execution pwd. It defaults to `True`. The submit command will automatically forward a local port to the remote tensorboard port to save your troubles.
