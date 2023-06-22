## Wobot assignment

main.py is the main file to run in this project.

To run use below command:

uvicorn main:app --reload

### Creating virtual environment
1. To create virtual environment in windows,
Open windows powershell and execute below commands one by one.
--> py -m pip install --upgrade pip
--> py -m pip --version				[To check pip version]
--> py -m pip install --user virtualenv
--> py -m venv enn_env			   [py -m venv venv-name]
--> enn_env\Scripts\activate		[to activate venv]  [venv-name\Scripts\activate]

After activating virtual env Install all the required modules one by one or write all the modules name in requirements.txt and install using below command,

--> pip install -r requirements.txt


2. To create virtual environment in linus,
Open terminal/ubuntu and execute below commands one by one.
--> pip install virtualenv
--> sudo python3 -m venv likith      [sudo python3 -m venv (venv-name)]
--> source likith/bin/activate       [source (venv-name)/bin/activate]

After activating virtual env Install all the required modules one by one or write all the modules name in requirements.txt and install using below command,

--> pip3 install -r requirements.txt

