# wroclaw-portal

The wroclaw-portal web system is a complex and comprehensive tool to obtain all necessary information about relocating to Poland to work or study. It consists of several modules covering different functionalities whose work do not interfere with one another. Functionalities include university search engine, documents library, forum, maps, news, currencies and qa. The structure of the project allows work of multiple developers on chosen modules without the risk of violating structure of remaining parts. The project allows using docker and running the application using docker containers.

## Requirements
Installed [git](https://git-scm.com/download/win)

Installed docker, preferably [docker desktop](https://docs.docker.com/desktop/install/windows-install/)

Linux Kernel [update package](https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) installed

10GB of free disk space (docker containers eat up a lot of space)

Available port 3000 and 5000


## Installation

1. Clone project to the chosen git directory using
```bash
git clone https://github.com/bastava-maryna/wroclaw-portal.git
```
2. Open docker, preferably docker desktop
3. Open terminal and navigate to cloned repository
```bash
cd wroclaw-portal
```
4. Run docker compose up. It might take few minutes.
```bash
docker compose up
```
5. After the command will finish execution, there should be two new containers created running at the moment, visible in the docker desktop
6. To open application, open localhost:3000 on your browser. Sometimes, there might be a short delay before the frontend and backend container will start communication.
