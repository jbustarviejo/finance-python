#Installation on ubuntu

git clone https://github.com/jbustarviejo/finance-django.git
sudo apt-get update
sudo apt install python3-pip
brew install pipenv

pipenv shell
pipenv install numpy PyMySQL lxml requests sklearn scipy

#Install Mysql. Dont forget specify the password
sudo apt-get install mysql-server

#Install Python
Install python3 from python.org
MAC: brew install python3

#Run all
./manage.py scrap_sectors
./manage.py scrap_industries
./manage.py scrap_companies
./manage.py scrap_companies_info


#Check some predictors

http://www.statsmodels.org/dev/install.html
https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/

* Mac:

The easiest way to install python is just downloading the package from its web.
```
sudo easy_install pip3
pip3 install virtualenv
brew install pipenv
```

Then just run:

```
virtualenv -p python3.8 venv
source venv/bin/activate
```

And finally

```
pipenv install --dev
```

NOTE: If something goes wrong and a package is not found, try to run this command to clear the cache first:

```
pipenv lock --clear
```

Install Django:

```
python -m pip install Django
python -m pip install psycopg2-binary
```

Install postgres from web


* To create an **superuser account**, use this command::

 ```
 $ ./manage.py createsuperuser
 ```
