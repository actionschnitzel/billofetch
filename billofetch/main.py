#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import platform
import psutil
import socket
import subprocess
import re

# Erstelle ein Tkinter-Fenster
fenster = tk.Tk()
fenster.title("BilloFetch")
#fenster.geometry("700x250")
fenster["background"]="#404040"





def get_cpu_name_linux():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except FileNotFoundError:
        return "CPU info not available on this system"
    except Exception as e:
        return f"Error: {str(e)}"

cpu_name = get_cpu_name_linux()

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor




get_wm = subprocess.Popen(["wmctrl", "-m"], stdout=subprocess.PIPE)
out, err = get_wm.communicate()

name_line = re.search(r'Name: (.+)', out.decode())

wm_name = name_line.group(1)


terminal_emulator = os.environ.get('TERM')



distro_name = os.popen("egrep '^(NAME)=' /etc/os-release")
distro_name = distro_name.read().strip('"\n').split('=')[1].strip('"')
print(distro_name)








#Infos
user =  os.environ["USER"]
host = socket.gethostname()
user_host = str(user +"@"+ host)

nice_name = os.popen("egrep '^(PRETTY_NAME)=' /etc/os-release")
nice_name = nice_name.read()
nice_name = "OS: " + nice_name.strip().split('=')[1]

deb_count = os.popen("dpkg --list | wc --lines")
deb_counted = deb_count.read()
deb_count.close()
#print(f"[Info]: {deb_counted[:-1]} .deb Packages Installed")
my_system = platform.uname()
get_de = os.environ.get("XDG_CURRENT_DESKTOP")
svmem = psutil.virtual_memory()


# Run the inxi -SG command and capture its output
command_output = subprocess.check_output(['inxi', '-SG'], universal_newlines=True)

# Use regular expressions to extract the desired text
pattern = r'Device-1: (.+?) driver:'
matches = re.search(pattern, command_output)

if matches:
    gpus = matches.group(1)
    print(gpus)
else:
    print("GPU information not found.")
    gpus = "Not found"




main_color = "#404040"
font_color = "white"
font_label = ("Sans",12)

# Erstelle einen Rahmen
logo_rahmen = tk.Frame(fenster,background=main_color,padx=20,pady=20)
logo_rahmen.pack(fill="both", expand=True,side=LEFT)

#distro_icon = PhotoImage(
#    file="/opt/billofetch/icons/nodistro_logo.png")

if distro_name == "Debian GNU/Linux":
    distro_icon = PhotoImage(file="/opt/billofetch/icons/debian.png")
elif distro_name == "Linux Mint":
    distro_icon = PhotoImage(file="/opt/billofetch/icons/mint_logo.png")
elif distro_name == "LMDE":
    distro_icon = PhotoImage(file="/opt/billofetch/icons/lmde_logo.png")
elif distro_name == "Ubuntu":
    distro_icon = PhotoImage(file="/opt/billofetch/icons/ubuntu.png")
else:
    distro_icon = PhotoImage(
        file="/opt/billofetch/icons/nodistro_logo.png") 

logo_label = tk.Label(logo_rahmen,image=distro_icon,background=main_color)
logo_label.pack()




info_rahmen = tk.Frame(fenster,padx=20,pady=20,background=main_color)
info_rahmen.pack(fill="both", expand=True,side=LEFT)



#Labels des rechten Rahmen

user_label = tk.Label(info_rahmen,text=user_host, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
user_label.pack(fill="x")

os_label = tk.Label(info_rahmen,text=nice_name, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
os_label.pack(fill="x")

host_label = tk.Label(info_rahmen,text="Host: " + host, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
host_label.pack(fill="x")

kernel_label = tk.Label(info_rahmen,text="Kernel: " + my_system.release, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
kernel_label.pack(fill="x")

pack_label = tk.Label(info_rahmen,text="Packages: " + deb_counted[:-1] + " (debian)", justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
pack_label.pack(fill="x")

shell_label = tk.Label(info_rahmen,text="Shell: " + os.environ['SHELL'][5:], justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
shell_label.pack(fill="x")

de_label = tk.Label(info_rahmen,text="DE: " + get_de, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
de_label.pack(fill="x")

wm_label = tk.Label(info_rahmen,text="WM: " + wm_name, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
wm_label.pack(fill="x")

term_label = tk.Label(info_rahmen,text="Terminal: " + str(terminal_emulator), justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
term_label.pack(fill="x")

cpu_label = tk.Label(info_rahmen,text="CPU: " + str(cpu_name), justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
cpu_label.pack(fill="x")

gpu_label = tk.Label(info_rahmen,text="GPU: " + gpus, justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
gpu_label.pack(fill="x")

memory_label = tk.Label(info_rahmen,text=f"Memory: {get_size(svmem.used)}/{get_size(svmem.total)}", justify=LEFT,anchor="w",font=font_label,background=main_color,foreground=font_color)
memory_label.pack(fill="x")
# Starte die Tkinter-Hauptschleife
fenster.mainloop()