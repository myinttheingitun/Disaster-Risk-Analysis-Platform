Connect to EC2 Instance via SSH:

Connect to Instance using Key pair and public IP.
Run below steps and command to setup application on the instance:
sudo yum update
sudo yum install python3-pip
yum install git
git clone https://github.com/invcble/WebApp_Python_Flask_Mysql.git
cd WebApp_Python_Flask_Mysql/
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
python3 app.py
nohup python3 app.py

Connect to your Application:
Navigate to the browser (public_ip:3000)
if there is any issue please check your SG rules.