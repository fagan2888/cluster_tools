# Cluster Tools
a submit command that works from one's local machine.


## Pain points of daily job submission
- Editing file on the server is slow. The network filesystem has limited bandwidth,
  it is inconvenient to directly code in an ssh session. As far as I know, there are two common ways around it:
  1. Write the code on the local machine and `rsync` to the access node for running.
  2. Ssh into a worker node, and use the local storage, submit the job directly from the worker node.

- Launch tensorboard and port forwarding.
  There are many steps if this is done by hand,
  1. Figure out which port is not used, and launch tensorboard at that port. (Or use a fixed port and risk that it is already used by another person/yourself).
  2. Find the machine that the job is submitted to.
  3. Open another terminal window and `ssh` to the worker machine through the access node with port forwarding.
  4. Open the url in the browser.
  5. Terminate the `ssh` that forwards the port once the job is completed.
  There are voices that a central server can be used for hosting tensorboard/visdom,
  but in my opinion it will be more resource efficient and easier for maintainence if the workers are reused for this purpose.

- Access the result after broken pipe.
  If the program runs for days, you will have to redo the tensorboard staff if the `ssh` connection is broken in the middle, more pain!


## Solutions
- This repo provides a local `submit` command. The job is launched to the cluster by prepending the command with the `submit`.
  Behind the scene your local modifications are copied to the cluster through the access node.

- The `submit` command will handle the the tensorboard for you. It will probe for an unused port, and launch `tensorboard` at that port.
  The `submit` command waits until port and worker machine are reported back, and start a `ssh` subprocess with port forwarding.
  The url to the tensorboard will be printed in your terminal and it will take just a click to access the output of the experiments.

- The `submit` command will not quit until `Ctrl-C` is sent.
  When `Ctrl-C` is sent, it will prompt and ask whether you want the remote job to be canceled, it sends a `scancel` command if your answer is `yes`.
  When the network is broken for a while, an exception will be thrown and the same prompt will be shown.
  If `no` is selected, it will reconnect to the access node, and redo the tensorboard port forwarding etc.


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
