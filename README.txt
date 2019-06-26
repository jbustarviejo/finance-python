#Installation on ubuntu

git clone https://github.com/jbustarviejo/scrap-python2.git
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
