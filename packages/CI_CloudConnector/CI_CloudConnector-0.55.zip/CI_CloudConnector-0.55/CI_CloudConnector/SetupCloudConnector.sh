echo updating libraries
sudo apt-get update
sudo apt-get install python-dev
sudo pip install CI_CloudConnector

echo create project folder
sudo mkdir /home/pi/ci_cc

echo copy run script
sudo cp /usr/local/lib/python2.7/dist-packages/CI_CloudConnector/runCloudConnector.sh /home/pi/ci_cc

sudo chmod 755 /home/pi/ci_cc/runCloudConnector.sh
#sudo chown root:root /home/pi/ci_cc/runCloudConnector.sh

echo copy autostart Script to init.d
sudo cp /usr/local/lib/python2.7/dist-packages/CI_CloudConnector/ci_cloudConnectorService /etc/init.d
sudo chmod 755 /etc/init.d/ci_cloudConnectorService
#sudo chown root:root /etc/init.d/ci_cloudConnectorService
sudo update-rc.d ci_cloudConnectorService  remove
sudo update-rc.d ci_cloudConnectorService defaults

echo ---------------------------------------------------------
echo Done setup , running application first time to set config
sudo python /usr/local/lib/python2.7/dist-packages/CI_CloudConnector.py Config
echo Complete setu up restart machine

# change root password - needed for Team Viewer
# sudo passwd root 

# Set Time Zone Manually
# sudo dpkg-reconfigure tzdata 