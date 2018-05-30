from getpass import getpass
from fabric import Connection
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
from colorama import Style, Fore


def _authenticate(config):
  """ Try authentication methods in the following order
  1. get password from config
  2. get ssh key path from config
  3. get password from terminal
  4. use system default key
  """
  if hasattr(config, "password"):
    connect_kwargs = {"password": config.password}
  elif hasattr(config, "ssh_key"):
    connect_kwargs = {"key_filename": config.ssh_key}
  else:
    password = getpass(f"Password for {config.hostname}: ")
    if password:
      connect_kwargs = {"password": password}
    else:
      connect_kwargs = None
  return connect_kwargs


def connect_entry_node(config):
  """ Make a connection with the entry node as defined in the configuration
  """
  connect_kwargs = _authenticate(config)
  try:
    conn = Connection(config.hostname, user=config.user, connect_kwargs=connect_kwargs)
    conn.open()
    if conn.is_connected:
      logging.info(f"Connection to {Fore.CYAN}{config.hostname}{Style.RESET_ALL} ESTABLISHED")
    return conn
  except:
    logging.exception(f"Connection to {Fore.RED}{config.hostname}{Style.RESET_ALL} FAILED")


def connect_node(config, node, gateway):
  """ Connect to the node the job is running using the entry node as a gateway
  """
  try:
    conn = Connection(node, user=config.user, gateway=gateway, connect_kwargs=gateway.connect_kwargs)
    conn.open()
    if conn.is_connected:
      logging.info(f"Connection to {Fore.CYAN}{node}{Style.RESET_ALL} through {Fore.CYAN}{gateway.host}{Style.RESET_ALL} ESTABLISHED")
    return conn
  except:
    logging.exception(f"Connection to {Fore.RED}{node}{Style.RESET_ALL} through {Fore.CYAN}{gateway.host}{Style.RESET_ALL} FAILED")
