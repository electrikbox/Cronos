<img src="https://i.imgur.com/Zauoeua.png" alt="Cronos Logo" width="100%"/>

<h2 align="center">Portfolio Project 2024</h2>

# 💡 Introducing CronOS

## 🕝 Welcome to the CronOS project

**CronOS** is the result of the collaboration of **Olive t'Servrancx** & **Valentine Quignon** for our end-of-first-year portfolio at Holberton School, in Lille FRANCE. Before everything, you can take a loot at our [landing page](https://valpumpkins.github.io/cronos_landing_page/)

Very briefly, **CronOS** aims to simplify the management of crons in order to open up this great functionality to a public unfamiliar with this automated tasks system.

Our team set about designing and developing this platform with the mission of simplifying IT processes for everyone, while guaranteeing a fluid and secure user experience.

We're already thinking about some next features, update some part and make this project even better in the futur.

## 🌏 How does it works

<img src="https://i.imgur.com/zzrQ7In.png" width="100%"/>

# 📡 Technologies used
## ➡️ Website
### Back-End

- <img src="https://i.imgur.com/CqMCoWI.png" width="30" height="30"> **DJANGO** : Python-based web development framework
- <img src="https://i.imgur.com/dSF9etv.png" alt="python" width="30" height="30"/> **PYTHON** : Main programming language
- <img src="https://i.imgur.com/aqTejpA.png" width="30" height="30"> **MySQL** : Database management system

### Front-end

- <img src="https://i.imgur.com/arVuW8o.png" width="30" height="30"> **HTML5** : Web content
- <img src="https://i.imgur.com/GoyGoKG.png" width="30" height="30"> **CSS3** : Stylesheet language to format the HTML document
- <img src="https://i.imgur.com/3vcMsBk.png" width="30" height="30"> **JavaScript** : Programming language to make web pages interactive

## ➡️ Application client

### Back-End

- <img src="https://i.imgur.com/dSF9etv.png" alt="python" width="30" height="30"/> **PYTHON** : Main programming language
- <img src="https://i.imgur.com/381E7uL.png" width="30" height="30" style="background-color:#c6c6c6"> **SHELL** : used to create shell script

### Front-end
- <img src="https://i.imgur.com/YRfTk5i.png" width="30" height="30"> **FLET** : used to create UI directly in Python

# How to install

First of all, create a viryual env and call it '.venv'
```
python3 -m venv .venv
```
Go to Cronos dir and activate the new virtual env
```
source .venv/bin/activate
```
Install the requirements
```
pip install -r requirements.txt
```
Deactivate venv (the launch script will activate it automatically)
```
deactivate
```
Before starting the server you will need to create 2 files:
- .env
- .my.cnf

### .env
First create a Django secret key with this tool : https://djecrety.ir/<br>
.env content
```
DJANGO_TOKEN='your django secret key'
DB_NAME='your database name'
DB_USER='your mysql user name'
DB_PASS='your mysql password'
DB_LOGS_TABLE='your sql cronos_logs table'
MAIL_CRONOS = 'your_email@mail.com'
MAIL_PASS = 'your email password'
```
### .my.cnf
.my.cnf content
```
[client]
host=your_host_name (localhost or 127.0.0.1 for local)
user=yourmysql_user_name
password=your mysql user_passwword
```
You can then go the `utils` directoy and launch the server by using this command in your terminal :
```
./server_launch.sh
```
and finally go to your **[http://localhost:8000/](http://localhost:8000/)**

### Usage

Once you're on the landing page, you can register. Be sure to check your e-mail to finalize your registration. Once you've completed these steps, you can log in and take advantage of our service

# 👁️ Demo-Day

For an overview of the project itself, please, take a look at **[this presentation](https://docs.google.com/presentation/d/11BWmuIlNjddTg8-kmVquacEXgRPU0YQoUmFQcpKq9H0/edit?usp=sharing)**. You can also take a look at our **[Landing page](https://valpumpkins.github.io/cronos_landing_page/)** and at our **[video-demo](https://www.youtube.com/watch?v=8pNNHtyUKQk)**

# 👥 Team

Please, do not hesitate to contact us :

🥁 **Olive t'Servrancx** on [Linkedin](https://www.linkedin.com/in/olivier-tservrancx/) and on [Github](https://github.com/electrikbox)

🥦 **Valentine Quignon** on [Linkedin](https://www.linkedin.com/in/valentine-quignon/) and on [Github](https://github.com/ValPumpkins)

# 🙏 Acknowledgements

To all the C21 cohort : ❤️ Christophe and Cassandra, Lucie and Michael ❤️ Thanks for this year with you all !

To our friends and family, who have supported us in every sense of the word (special thanks to **🎃 Mary Pumpkins** for help with the logo)

To the staff at Holberton France: thanks for the help and the croissants
