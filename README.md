# Setting Up a Debian 12 with Netbird and Wazuh

## Table of Contents
- [Introduction](#1-introduction)
- [Preparing for Installation](#2-preparing-for-installation)
- [Installing Debian 12](#3-installing-debian-12)
- [Customization: Zsh and Neovim](#4-customization-zsh-and-neovim)
- [Installing and Configuring Netbird](#5-installing-and-configuring-netbird)
- [Installing and Configuring Wazuh](#6-installing-and-configuring-wazuh)
- [Finalizing the Setup](#7-finalizing-the-setup)
- [Conclusion and Future Enhancements](#8-conclusion-and-future-enhancements)

## 1. Introduction
- Overview of the home lab setup
    - Debian 12 as a server running [Netbird](https://netbird.io/) and [Wazuh](https://wazuh.com/)
- Purpose and goals of the setup  
    - The ultimate goal for this was to gain visibility into my network. I knew that I wanted to be able to access the Wazuh dashboard remotely and I was not willing to do it insecurely. Before diving into Wazuh I installed suricata and configured some basic NIDS rules but, setting up dashboards and integrating them while, possible was out of the scope of time for what I wanted to do. 

## 2. Preparing for Installation
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
## 3. Installing Debian 12
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
## 4. Customization: Zsh and Neovim
### 4.1. Installing and Configuring Zsh
- Installing Zsh  
- Setting Zsh as the default shell  
- Customizing with Oh My Zsh (if applicable)  

### 4.2. Installing and Configuring Neovim
- Installing Neovim  
- Adding plugins and custom configurations  

## 5. Installing and Configuring Netbird
### 5.1. Overview of Netbird
- Purpose and use cases  

### 5.2. Installation Steps
- Downloading and installing Netbird  
- Configuring Netbird for secure remote access  

## 6. Installing and Configuring Wazuh
### 6.1. Overview of Wazuh
- Purpose and security benefits  

### 6.2. Installing the Wazuh Agent
- Steps for installation  
- Connecting to a Wazuh server  

### 6.3. Configuring and Testing Wazuh
- Ensuring proper log collection  
- Testing alerts and monitoring  

## 7. Finalizing the Setup
### 7.1. Security Hardening
- Basic security measures (firewall, SSH hardening, etc.)  

### 7.2. System Monitoring and Maintenance
- Regular updates  
- Monitoring system logs  

## 8. Conclusion and Future Enhancements
- Summary of the setup  
- Possible next steps for improvement  
