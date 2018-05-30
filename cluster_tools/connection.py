from getpass import getpass
from fabric import Connection
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
from colorama import Style, Fore

def connect_entry_node(config):
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
  conn = Connection(config.hostname, user=config.user, connect_kwargs=connect_kwargs)
  try:
    conn.open()
    if conn.is_connected:
      logging.info(f"Connection to {Fore.CYAN}{config.hostname}{Style.RESET_ALL} ESTABLISHED")
    return conn
  except:
    logging.exception(f"Connection to {Fore.RED}{config.hostname}{Style.RESET_ALL} FAILED")
