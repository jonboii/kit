#! /usr/bin/python3

import os
from termcolor import colored

# Maybe sometime later we'll take this and make a separate file, but for now, I want everything in 
## one single executable file

#TODO: Make this less error prone - some linux flavors don't have /home at the root
#TODO: Check to make sure we're in the Downloads directory before installs & downloads - otherwise bail
#TODO: Grab the neo4j database info, make sure its running and provide to user
#TODO: Grab the neo4j webserver & the associated port
#TODO: Adjust the dir/file checks to local, rather than abspath
#TODO: Use a list of github repos and iterate through them, rather than this mess
#TODO: Install assetfinder
#TODO: After install, rename the privilege-escalation-suite dir to PEAS
#TODO: Ensure that the Metasploit database service is up & running, provide info to the user
# sudo systemctl start postgresql
# <check to ensure the service is running now>
# msfdb init

apt_packages = ['seclists','gobuster','metasploit-framework',
                'crackmapexec','snmpcheck','enum4linux','smbmap','wfuzz','sublime-text',
                'yersinia','bloodhound','subfinder','tilix']

pypi_packages = ['one-lin3r','ptftpd','bloodhound']

sublime = 'deb https://download.sublimetext.com/ apt/stable/'
user = os.getlogin()

def system_update():
    os.system(f"cd /home/{user}/Downloads/")
    print(colored("Beginning System updates, please wait...", 'blue'))
    os.system('sudo apt install python3-pip -y')
    os.system('sudo apt update -y')
    os.system('sudo apt upgrade -y')
    os.system('sudo apt upgrade -y')
    os.system('sudo apt autoremove -y')
    print(colored("Finished SYSTEM setup", 'green'))
    return()



def software_update():
    os.system(f"cd /home/{user}/Downloads/")
    print(colored("Beginning Software install(s) & updates, please wait...", 'blue'))
    print("")
    os.system('wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg\
                | sudo apt-key add -')
    os.system('sudo apt-get install apt-transport-https')
    os.system(f'echo {sublime} | sudo tee /etc/apt/sources.list.d/sublime-text.list')
    for pkg in apt_packages:
        os.system(f'sudo apt install {pkg} -y')
        os.system('sudo apt install -y')
        print('done')
    for pkg in pypi_packages:
        os.system(f'pip3 install {pkg}')
    os.system('sudo mkdir -p /usr/share/neo4j/logs')
    os.system('sudo touch /usr/share/neo4j/logs/neo4j.log')
    os.system('sudo neo4j start')

    ### BEGIN IF/ELSE CHECKS FOR SOFTWARE ####
    if os.path.exists("/usr/local/bin/one-lin3r"):
        print(colored("one-lin3r already exists in /usr/local/bin already exists in /usr/local/bin, continuing...\n", 'green'))
    else:
        os.system(f"sudo ln -s /home/{user}/.local/bin/one-lin3r /usr/local/bin")

    if os.path.exists("/home/$user/Downloads/nmap-vulners"):
        os.system(f'sudo cp /home/{user}/Downloads/nmap-vulners/vulners.nse /usr/share/nmap/scripts/vulners.nse')
        print(colored("nmap-vulners already installed, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/vulnersCom/nmap-vulners')
        if not os.path.exists('/usr/share/nmap/scripts/vulners.nse'):    
            os.system(f'sudo cp /home/{user}/Downloads/nmap-vulners/vulners.nse /usr/share/nmap/scripts/vulners.nse')
        else:
            print(colored("vulners.nse has been downloaded and copied into the nmap scripts DB", 'green'))

    if os.path.exists(f'/home/{user}/Downloads/nmapAutomator'):
        print(colored("nmapAutomator already installed, continuing...", 'green'))
        if not os.file.exists('/usr/local/bin/nmapAutomator.sh'):
            os.system(f'sudo ln -s /home/{user}/Downloads/nmapAutomator/nmapAutomator.sh /usr/local/bin/')
        else:
            print(colored("Already have nmapAutomator in local binaries, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/21y4d/nmapAutomator')
        os.system(f'chmod +x /home/{user}/Downloads/nmapAutomator/nmapAutomator.sh')
        print(colored('nmapAutomator is now dynamically executable', 'green'))


    if os.path.exists(f'/home/{user}/Downloads/Impacket'):
        print(colored("Impacket is already installed, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/SecureAuthCorp/Impacket')

    if os.path.exists(f'/home/{user}/Downloads/privilege-escalation-awesome-scripts-suite'):
        print(colored("LinPEAS & WinPEAS already installed, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite')


    if os.path.exists('/usr/local/bin/LinEnum.sh'):
        print(colored("LinEnum already installed, continuing...\n", 'green'))
    else:
        os.system(f'wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh\
                    -O /home/{user}/Downloads/LinEnum.sh')
        os.system(f'sudo ln -s /home/{user}/Downloads/LinEnum.sh /usr/local/bin/')


    if os.path.exists(f'/home/{user}/Downloads/evil-winrm'):
        print(colored("evil-winRM already installed, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/HackPlayers/evil-winrm')


    if os.path.exists(f'/home/{user}/Downloads/Enum4LinuxPy'):
        print(colored("Enum4LinuxPy already installed, continuing...\n", 'green'))
    else:
        os.system('git clone https://github.com/0v3rride/Enum4LinuxPy')


    if os.path.exists(f'/home/{user}/Downloads/vlan-hopping'):
        print(colored("VLAN-Hopping already installed, continuing...", 'green'))
    else:
        os.system('git clone https://github.com/nccgroup/vlan-hopping.git')
        #### END IF ELSE CHECKS #####

    ### TOOL UPDATES & SETUPS ###
    print("Updating searchsploit DB....\n")
    os.system('sudo searchsploit -u')
    print(colored("Finished searchsploit update", 'green'))
    print("Updating locate DB...\n")
    os.system('sudo updatedb')
    print(colored("Finished locate DB update \n", 'green'))
    print("Updating nmap script database\n")
    os.system('sudo nmap --script-updatedb')
    print(colored("nmap script database updated \n", 'green'))

    print("Checking if rockyou has been unzipped...")
    if os.path.isfile('/usr/share/wordlists/rockyou.txt.gz'):
        print("It hasn't been decompressed - decompressing now...\n")
        os.system('sudo gunzip /usr/share/wordlists/rockyou.txt.gz')
    else:
        print(colored("rockyou has already been unzipped \n", 'green'))

    print(colored("Software & Tool updates have been completed!", 'green'))
    return()
    #### END TOOL UPDATES & SETUPS ####

def main():
    print(colored("Automated Kit buildout script\n", 'blue'))
    print("Would you like to install ALL or just the TOOLS?\n")
    print("Please type TOOLS or ALL \n")
    choice = input()
    choice = str(choice)
    if choice == "ALL":
        system_update()
        software_update()
    elif choice == "TOOLS":
        software_update()
    else:
        print("You had one simple choice and you already screwed that up")

if __name__ == "__main__":
    main()    
