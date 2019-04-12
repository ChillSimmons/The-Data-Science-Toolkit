# The-Data-Science-Toolkit

## 1. SSH Keys

SSH (Secure Shell) Keys allow access to SSH Protocol. Key Pairs, including the public and private keys, provide for interaction, remotely logging in to various systems, managing infrastructure, etc. 

SSH keys can be created by making a .ssh directory in a Terminal `$ mkdir -p .ssh`.
- The **-p**, serves as a command to interpret .ssh
- The Key Pairs are generated `$ ssh-keygen`
- The Public Key can be displayed `$ cat ~/.ssh/id.rsa.pub`

We needed to sync these keys with GitHub.

A Copy of the Public Key was set to our Desktop.
- `$ cat ~/.ssh/id.rsa.pub | pbcopy`, produces a clipboarded copy
- `$ cp ~/.ssh/id_rsa.pub ~/Desktop`, places the copy on the Desktop

- `$ ssh git@github.com`

**ssh** is used to log and execute commands into remote machines.


## 2. Amazon EC 2

Amazon Web Services (AWS) provides EC2 (Elastic Compute Cloud) services. EC2 can be used to build servers, and provide alternate cloud computing services.

From the * *EC2 Dashboard* * click * *Launch Instance* *
Choose an Amazon Machine image (ami) and software configuration.

We selected the (free) * *Ubuntu Server 16.04 LTS (HVS), SSD Volume type - ami ba602bc2* *
- The number represents the year (2016); odd #'s are in development
- The ami (Amazon Machine Image) is a fully configured (non-running) server
  - Through the ami, we will run the Image (Instance - Ubuntu 16.04)

Next we chose a t2.micro type virtual server (Instance)
- This option comes with 1 CPU and 1 GiB Memory with our Free Tier Service

We adjusted the GiB Size (in the Next tab), increasing it from 8 to 20.

We did Not add Tags.

We Reviewed, associating our Existing Key Pair, checking our security group, and in this case selected an existing group. 

We then * *Launch* * the Instance

For future purposes, we clicked the * *View Instances* * section, then the * *Description* * section,

and we Copied the * *IPv4 Pubilic IP* * address


## 3. Security Groups

We assigned an * *Existing Security Group* *
- Which we created and named earlier
  - GitHub --> * *SSH and GPG Keys* * --> Name, Key, click * * Add SSH Key* *
- with Inbound Support from HTTP, HTTPS, SSH, PostgreSQL, and a Custom TCP Rule
  - corresponding to the ports 80, 443, 22, 27016, 5432 (respectively) 
  
  Jupyter runs on HTTPS (443). 
  
  
 ## 4. AWS Operating System
  
  After selecting the Ubuntu Server 16.04 LTS (HVS), SSD Volume type - ami ba602bc,
  
  we chose a t2.micro type virtual server (Instance).
  - with our free tier service, this option comes with 1 CPU and 1 GiB Memory
  
  We return to our Terminal, and execute the `$ ssh git@github.com` command. 
  We then execute the remote command to our Terminal's IP `$ ubuntu@_ip.address_`
  
  
 ## 5. Docker Installation
  
  Again, we should have already returned to the Terminal and typed `$ ubuntu@_ip.address_`
  
  if asked permission to Continue, type **yes**
  
  Create the Docker Group, by typing `$ curl -sSL https://get.docker.com | sh`
  
  Add our Ubuntu User to the Docker Security Group (without doing this, we would have to put **sudo** in front of Docker every time we use it), by typing `$ sudo usermod -aG docker ubuntu`
  
  Then, type **exit**
  - Leaving our Instance, and returning to Local
    - Then, Log back in. Type **!!**, to get back to Ubuntu
  
  This was necessary to load our new security. 
  
  Docker performers containerization (operating-system-level virtualization). It runs containers, or software packages. If you preveiously exited the shell (which again, may be necessary to re-evaluate group membership), you can return with, 
  - `$ ssh ubuntu@_ip.address_`
  
  You then enter a new shell, by typing `$ tmux`
  - tmux allows returnt to Terminals you left, without interrupting the running processes, while accessing multiple separate Terminal sessions. 
  - as a shell-server, it jumps to a (more) stable AWS stash, and runs as a software.
  
  
  ## 6. Obtaining the Correct Docker Image
  
  Confirm that following Installation, you can run Docker commands without sudo. 
  
  Access `$ docker pull jupyter/datascience-notebook`
  
  
  ## 7. Running the Correct Docker Image as a Container 
  
  We ran this rather long command more succinctly, 
  - `$ docker run \ `
  - `$ -d \ `
  - `$ -p 443:8888 \ `
  - `$ -v /home/ubuntu:home/jovyan jupyter/datascience-notebook`
    - there are NO spaces after the forward slash when executing the command
    
  We can retrieve the Token, which will be used later from the Container.
  - `$ docker ps`
  - `$ docker exec _containerID(or first 4 digits)_ jupyter notebook list`
  
  Go to _ip.address:443_ in Google.
  - Insert the Token into the space and Login
  - New Jupyter launched
    - Change the Name to _Whatever You Like_
  
  
  ## 8. Jupyter Notebook Security Concerns
  
  The two-way connection established by the command `$ -v /home/ubuntu:home/jovyan jupyter/datascience-notebook` allows for deletion in the Terminal of the shell, while still being able to access the notebook file as it exits in multiple places. 
  
  Virtually all IP addresses are constantly pinged for lack of security. 
  
  
  ## 9. Anything Forgotten
  
  Another way to abbreviate the image as a Container, would be to use the command,
   `$ echo 'alias j="docker run -d -p 443:8888 -v /home/unbuntu:/home/jovyan jupyter/datascience-notebook"'>>profile`, reducing the larger command to an alias j. 
   
   
   ## 10. Create at least one diagram of your overall system
   
   ![Alt Text](https://github.com/ChillSimmons/Wk-4---The-Data-Science-Toolkit/blob/master/HW%204%20-%20Diagram.JPG)
   
   ## 11. Detailed budget of the costs of running a Jupyter Data Science Notebook Server for 3 Months using at least 3 different kinds of EC2 Instances
   
   The Instance running t2.2xlarge
   - 8 CPUs, 32 GiB Memory, Variable ECU, EBS Only
   - $0.3712 per hour
   - $0.3712 per hour, times 24 hours a day, times 90 days = $801.79
   
   The Instance running m5d.large
   - 2 CPUs, 8 GiB Memory, 8 ECU, 1 x 75 NVMe SSD
   - $0.113 per hour
   - $0.113 per hour, times 24 hours a day, times 90 days = $244.08
   
   The Instance running Compute Optimized, c5.18xlarge
   - 72 CPUs, 144 GiB Memory, 218 ECU, EBS Only, 25 gigabit
   - Recommended for CPU-bound scale out operations
   - $3.06 per hour
   - $3.06 per hour, times 24 hours a day, times 90 days = $6609.60
   
   We chose the Free version, t2.micro
   - 1 CPU, 1 GiB Memory, EBS only
