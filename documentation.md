# Setting Up a Debian 12 with Netbird and Wazuh

## __Table of Contents__
- [Introduction](#1-introduction)
- [Preparing for Installation](#2-preparing-for-installation)
- [Installing Debian 12](#3-installing-debian-12)
- [Customization: Zsh and Neovim](#4-customization-zsh-and-neovim)
- [Installing and Configuring Netbird](#5-installing-and-configuring-netbird)
- [Installing and Configuring Wazuh](#6-installing-and-configuring-wazuh)
- [Finalizing the Setup](#7-finalizing-the-setup)
- [Conclusion and Future Enhancements](#8-conclusion-and-future-enhancements)
## 1. __Introduction__
- __Overview of the home lab setup__
    - Debian 12 as a server running [Netbird](https://netbird.io/) and [Wazuh](https://wazuh.com/)
- __Purpose and goals of the setup__  
    - The ultimate goal for this was to gain visibility into my network. I knew that I wanted to be able to access the Wazuh dashboard remotely and I was not willing to do it insecurely. Before diving into Wazuh I installed suricata and configured some basic NIDS rules but, setting up dashboards and integrating them while, possible was out of the scope of time for what I wanted to do. 
## 2. __Preparing for Installation__
### 2.1. Hardware and Software Requirements
#### [Debian](https://www.debian.org/releases/stable/i386/ch03s04.en.html)
- **RAM:** 1 GB
- ***DISK SPACE:*** 2 GB
- ***CPU:*** Pentium 4 1GHz
---
#### [Wazuh Server](https://documentation.wazuh.com/current/installation-guide/wazuh-server/index.html)
- **Reccomended Operating Systems:**
   - Amazon Linux 2, Amazon Linux 2023
   - Red Hat Enterprise Linux 7, 8, 9
   - CentOS 7, 8
   - Ubuntu 16.04, 18.04, 20.04, 22.04, 24.04
- ***RAM:***
    - 2 GB
    - 2 Cores
- ***DISK SPACE:***
    - Alerts Per Second | GB/90 Days
        - 0.25 | 0.1
        - 0.1  | 0.04
        - 0.5  | 0.2
---
#### [Wazuh Indexer](https://documentation.wazuh.com/current/installation-guide/wazuh-indexer/index.html)
- **Reccomended Operating Systems:**
   - Amazon Linux 2, Amazon Linux 2023
   - Red Hat Enterprise Linux 7, 8, 9
   - CentOS 7, 8
   - Ubuntu 16.04, 18.04, 20.04, 22.04, 24.04
- ***RAM:***
    - 4 GB
    - 2 Cores
- ***DISK SPACE:***
    - Alerts Per Second | GB/90 Days
        - 0.25 | 3.7
        - 0.1  | 1.5
        - 0.5  | 7.4
---
#### [Wazuh Dashboard](https://documentation.wazuh.com/current/installation-guide/wazuh-dashboard/index.html)
- **Reccomended Operating Systems:**
   - Amazon Linux 2, Amazon Linux 2023
   - Red Hat Enterprise Linux 7, 8, 9
   - CentOS 7, 8
   - Ubuntu 16.04, 18.04, 20.04, 22.04, 24.04
- ***RAM:***
    - 4 GB
    - 2 Cores
- ***DISK SPACE:***
    - Alerts Per Second | GB/90 Days
        - 0.25 | 3.7
        - 0.1  | 1.5
        - 0.5  | 7.4
---
#### [Netbird](https://docs.netbird.io/selfhosted/selfhosted-quickstart)
- **RAM:** 2 GB
- ***CPU:*** 1 Core CPU
---
### 2.2. Creating a Bootable USB with Ventoy
- What is Ventoy:
    - Ventoy is a tool that allows multiple ISO/WIM/IMG/VHD(X)/EFI files to be bootable via a usb drive for quick imaging of computers. I followed [this guide](https://www.ventoy.net/en/doc_start.html) and set up a spare [64 GB 3.0 USB Thumbdrive](https://www.amazon.com/SuperSpeed-64GB-USB-3-0-Storage/dp/B07T4J6X1N/ref=asc_df_B07T4J6X1N?mcid=ec6e32bcae683e74a16da893e0c5fddf&hvocijid=5717512751185308201-B07T4J6X1N-&hvexpln=73&tag=hyprod-20&linkCode=df0&hvadid=721245378154&hvpos=&hvnetw=g&hvrand=5717512751185308201&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9007574&hvtargid=pla-2281435181498&th=1). 
- Adding the Debian 12 ISO  
    - I went to the [Debian Download Page](https://cdimage.debian.org/debian-cd/12.10.0-live/amd64/iso-hybrid/) and downloaded ```debian-live-12.10.0-amd64-xfce.iso```. A simple drag and drop onto the mounted ventoy USB drive, allow the transfer, and safely eject the media.  
## 3. __Installing Debian 12__
- Insert Ventoy USB into Lenovo M910 PC
- Catch boot into BIOS via F12 
- Boot into Ventoy USB
### 3.1. Installation Process
- Once booted up into the Debian Live Installer. I went through the basic steps of:
    - Choosing preferred language 
    - Country / Region
    - Keyboard Layout
    - Configure Network 
    - Set Hostname
    - Create Root Password
    - Create User Account and Password
    - Partition the Disk (guided)

### 3.2. Initial Post-Installation Setup
- Standard Post Install Steps:
    - Update system for latest security patches and software:
        - ```sudo apt update && sudo apt upgrade -y```  

    - Remove unecessary packages:
        - ```sudo apt autoremove && sudo apt purge -y```

    - Add user account to sudo group
        - ```adduser doggybitsuser```
        - ```usermod -aG sudo doggybitsuser```

    - Install Uncomplicated firewall (UFW)
        - ``` sudo apt install ufw -y ```

    - Configure default security policies
        - ``` sudo ufw default deny incoming```
        - ``` sudo ufw default allow outgoing ```

    - Enable UFW 
        - ``` sudo ufw enable ```
        - ``` sudo ufw status ```

- Custom Post Install Steps: 
    - Install zsh 
        - ``` sudo apt install zsh -y ```
        - ``` zsh --version ```

    - Change defualt shell from bash to z shell 
        - ```sudo chsh -s $(which zsh) ```

    - Reboot
        - ``` sudo reboot ```

    - Log in and check user shell   
        - ``` echo $SHELL ```

    - Install Neovim
        - ``` sudo apt install neovim -y ```

    - Install [LazyVim](https://www.lazyvim.org/)
        - ``` git clone https://github.com/LazyVim/starter ~/.config/nvim ```

    - Check health of Neovim
        - ``` :LazyHealth ```

    - Install [Oh My Zsh](https://ohmyz.sh/)
        - ``` sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" ```
## 4. __Customization: Zsh and Neovim__
### 4.1 Configuring ohmyzsh
- Edit the .zshrc Config
    - ``` nvim ~/.config/.zshrc ```
- Uncomment / Change the following lines
- Change Line 10
    - ``` ZSH_THEME="random" ```

- Change Line 14
    - ``` plugins=(git zsh-syntax-highlighting zsh-autosuggestions) ```

- Change Line 29
    - ``` Zstyle':omz:update' mode reminder ```

- Uncommented the following alias'
    - ``` alias zshconfig="nvim ~/.zshrc" ```
    - ``` alias ohmyzsh="nvim~/.oh-my-zsh" ```
### 4.2 Configuring lazyvim
- Confirm nvim version 
    - ``` nvim version ```

- Installed JetBrains Mono Nerd Fonts
    - ```mkdir -p ~/.local/share/fonts/NerdBrains```
    - ```curl -L -o ~/.local/share/fonts/NerdBrains/NerdBrains.tff \ "https://github.com/AlexW00/NerdBrains/raw/main/NerdBrains-Regular.tff" ```

- Refresh Font Cache
    - ```fc-cache -f -v ~/.local/share/fonts```

- Resync Lazy Vim
    - ```:Lazy sync```
## 5. __Installing and Configuring Netbird__
### 5.1. Overview of Netbird
- Netbird is self described as an open source, decentralized, mesh VPN with the core objectives including: 
    - Automated P2P Connections eliminating configurations
    - Secure Communications via riding the backbone of WireGuard encryption tunnels
    - Zero Trust networking principals which can ensure access controls void of a central server
    - Cross platform compatibility between various OS via agent or agentless monitioring 
    - Scalability from soho networks to large enterprise implementations
- Use Cases
    - Secure access to internal resoruces (servers, databases, tools/utilities, securitiy visibility)
    - Secure communication between IoT devices, edge servers, and cloud platforms
    - Gaming & Media streaming via plex 
### 5.2. Installation Steps
- Downloading and installing [Netbird](https://docs.netbird.io/how-to/installation)
    - Add the Repo
        - ``` sudo apt-get update ```

        - ``` sudo apt-get install ca-certificates curl gnupg -y ```
        
        - ``` curl -sSL https://pkgs.netbird.io/debian/public.key | sudo gpg --dearmor --output /usr/share/keyrings/netbird-archive-keyring.gpg ```

        - ``` echo 'deb [signed-by=/usr/share/keyrings/netbird-archive-keyring.gpg] https://pkgs.netbird.io/debian stable main' | sudo tee /etc/apt/sources.list.d/netbird.list ```
    - Update APT Cache
        - ``` sudo apt-get update ```

    - Install Netbird package
        - ``` sudo apt-get install netbird ```

    - Installer runs and ends with a pop up for device registration through either MFA SSO or a user account with Netbird. 
- Configuring Netbird for secure remote access
    - There wasn't much configuration on the Netbird side of things I followed [this guide](https://docs.netbird.io/how-to/add-machines-to-your-network) which had me enter a website to netbird and install a windows installer for the Netbird peer (agent) to be installed on my Windows 10 laptop. When installing the Server, Indexer, and Dashboard, the agent was also installed on my Debian PC. 
    - I was able to connect my Windows computer to my Debian computer via the Netbird tunnel and ensure ICMP connectivity with a ping from the private VPN IP address provided in the Netbird dashboard.
## 6. __Installing and Configuring Wazuh__
### 6.1. Overview of Wazuh
- Wazuh is a open source platform that stiches together XDR (Extended Detection and Response), SIEM (Security Information and Event Management), and Compliance Monitoring together into one package that can be installed locally and for free. Their primary goals include: 
    - Threat Detection across enpoints, cloud agents, and containers
    - Aggregation and analysis driven from diverse logging sources for security insight
    - Adherence to standards such as GDPR, HIPAA, PCI-DSS, and NIST
    - Scanning capabilities to look into unpatched software, misconfigurations, and potential risk exposure
    - Built on OSSEC HIDS 
- Security benefits 
    - Real Time Threat Detection
    - Comprehensive Compliance
    - Scaleable SIEM Capabilities
    - Cost-Effective / Open Source

### 6.2. Installing the Wazuh Agent
- Convientient One Liner for Installation 
    - ``` curl -sO https://packages.wazuh.com/4.11/wazuh-install.sh && sudo bash ./wazuh-install.sh -a ```

- Once install is complete it provides the web interface address as well as the default admin user with a default hashed password. 
- Disable auto updates for reliability 
    - ``` sed -i "s/^deb /#deb /" /etc/apt/sources.list.d/wazuh.list ```
    - ``` sudo apt update ```

- Connecting to a Wazuh server  
    - ``` https://localhost:443 ```
    
- I knew that the purpose of this was to be able to access the dashboards and my systems securely and remotely when away from my apartment. I looked into how I could add a wazuh api for my VPN net. I navigated to the opensearch_dashboard.yml file located at ``` /etc/wazuh-dashboard ``` I then added another indexer node for the dashboard to push to by editing the following lines ``` server.host ```, ``` server.port```, ```opensearch.hosts```, and ```opensearch.ssl.verificationMode```. I then restarted the wazuh-manager and connected to the wazuh-dashboard over the VPN tunnel.  
### 6.3. Configuring and Testing Wazuh
- Ensuring proper log collection  
- Testing alerts and monitoring  
## 7. __Finalizing the Setup__
### 7.1. Security Hardening
- Basic security measures (firewall, SSH hardening, etc.)  

### 7.2. System Monitoring and Maintenance
- Regular updates  
- Monitoring system logs  
## 8. __Conclusion and Future Enhancements__
- Summary of the setup  
- Possible next steps for improvement  
