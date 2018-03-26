#!/bin/python3

import sys, os, subprocess, pydoc

# Main definition - constants
menu_actions = {}
logs_actions = {}
messages = '/var/log/messages'

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')

    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Logs")
    print("2. Services")
    print("3. Monitor")
    print()
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_main_menu(choice)

    return

# Logs Menu
def logs_menu():
    os.system('clear')
    print("Logs Menu:\n")
    print("1. Messages")
    print("2. Cron")
    print("3. Secure")
    print("4. ATS - Cwcats")
    print("5. ATS - Manager")
    print("6. ATS - Diags")
    print()
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_log_menu(choice)
    return

# Services
def services_menu():
    os.system('clear')
    print("Services Menu:\n")
    print("1. Trafficserver - Reload")
    print("2. Trafficserver - Restart")
    print()
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_services_menu(choice)
    return

# Monitor
def monitor_menu():
    os.system('clear')
    print("Monitor Menu:\n")
    print("1. CPU, MEM & Processes")
    print("2. Network General Stats")
    print("3. Disk I/O")
    print("4. Filesystems")
    print()
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_monitor_menu(choice)
    return


# ========================
#     MENUS EXECUTION
# ========================

# Execute menu
def exec_main_menu(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions['main_menu']()
  else:
    try:
      menu_actions[ch]()
    except KeyError:
      print("Invalid selection, please try again.\n")
      menu_actions['main_menu']()
  return

def exec_log_menu(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    logs_actions['logs_menu']()
  else:
    try:
      print()
      logs_actions[ch]()
    except KeyError:
      print("Invalid selection, please try again.\n")
      logs_actions['logs_menu']()
  return

def exec_services_menu(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    services_actions['services_menu']()
  else:
    try:
      print()
      services_actions[ch]()
    except KeyError:
      print("Invalid selection, please try again.\n")
      services_actions['services_menu']()
  return

def exec_monitor_menu(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    monitor_actions['monitor_menu']()
  else:
    try:
      print()
      monitor_actions[ch]()
    except KeyError:
      print("Invalid selection, please try again.\n")
      monitor_actions['monitor_menu']()
  return



# ====================
#     COMMANDS
# ====================

def htop():
  try:
    os.system('/usr/bin/htop')
    # htop = subprocess.Popen(['sudo','/usr/bin/htop']) # , stdin=subprocess.PIPE, stdout=sys.stdout
    # htop.wait()
    monitor_actions['monitor_menu']()
  except KeyboardInterrupt:
    raise

def iotop():
  try:
    os.system('sudo /sbin/iotop')
    # iotop = subprocess.Popen(['sudo','/sbin/iotop']) # , stdin=subprocess.PIPE, stdout=sys.stdout
    # iotop.wait()
    monitor_actions['monitor_menu']()
  except KeyboardInterrupt:
    raise

def iptraf():
  try:
    os.system('sudo /sbin/iptraf-ng -g')
    # iptraf = subprocess.Popen(['sudo','/sbin/iptraf-ng','-g']) # , stdin=subprocess.PIPE, stdout=sys.stdout
    # iptraf.wait()
    monitor_actions['monitor_menu']()
  except KeyboardInterrupt:
    raise

def dfh():
  try:
    os.system("/bin/df -h")
    input("Press Enter to go back...")
    monitor_actions['monitor_menu']()
  except KeyboardInterrupt:
    raise

def less(file):
  try:
    less = subprocess.Popen(['sudo','/bin/less', file], stdin=subprocess.PIPE, stdout=sys.stdout)
    less.stdin.close()
    less.wait()
    logs_actions['logs_menu']()
  except KeyboardInterrupt:
    raise

def systemctl(action, service):
  try:
    systemctl = subprocess.Popen(['sudo','/bin/systemctl', action, service], stdin=subprocess.PIPE, stdout=sys.stdout)
    systemctl.stdin.close()
    systemctl.wait()
    if systemctl.returncode == 0:
      print("Return code is " + str(systemctl.returncode) + ". Looks Good.")
    else:
      print(systemctl.stdout)
    services_actions['services_menu']()
  except KeyboardInterrupt:
    raise
  except subprocess.CalledProcessError as exc:
    print("Status : FAIL", exc.returncode, exc.output)

# Back to main menu
def back():
  menu_actions['main_menu']()

# Exit program
def exit():
  sys.exit()

def less_messages():
  less('/var/log/messages')

def less_cron():
  less('/var/log/cron')

def less_secure():
  less('/var/log/secure')

def less_ats_cwcats():
  less('/var/log/trafficserver/cwcats.log')

def less_ats_manager():
  less('/var/log/trafficserver/manager.log')

def less_ats_diags():
  less('/var/log/trafficserver/diags.log')

def systemctl_reload_trafficserver():
  confirm = input("Are you sure you want to reload? (y/n) ")
  if confirm.lower() == "y":
    systemctl('reload', 'trafficserver')
  else:
    services_actions['services_menu']()

def systemctl_restart_trafficserver():
  confirm = input("Are you sure you want to restart? (y/n) ")
  if confirm.lower() == "y":
    systemctl('restart', 'trafficserver')
  else:
    services_actions['services_menu']()





# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
  'main_menu': main_menu,
  '1': logs_menu,
  '2': services_menu,
  '3': monitor_menu,
  '9': back,
  '0': exit,
}

logs_actions = {
  'logs_menu': logs_menu,
  '1': less_messages,
  '2': less_cron,
  '3': less_secure,
  '4': less_ats_cwcats,
  '5': less_ats_manager,
  '6': less_ats_diags,
  '9': back,
  '0': exit,
}

services_actions = {
  'services_menu': services_menu,
  '1': systemctl_reload_trafficserver,
  '2': systemctl_restart_trafficserver,
  '9': back,
  '0': exit,
}

monitor_actions = {
  'monitor_menu': monitor_menu,
  '1': htop,
  '2': iptraf,
  '3': iotop,
  '4': dfh,
  '9': back,
  '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
  # Launch main menu
  main_menu()
