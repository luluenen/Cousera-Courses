# Only works for Ubuntu debian
pip install 'ripe.atlas.cousteau<=1.2.9'
apt-get install python-graph-tool
apt-get install libjpeg libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
pip install PIL
echo "deb http://downloads.skewed.de/apt/trusty trusty universe" | tee -a /etc/apt/sources.list
echo "deb-src http://downloads.skewed.de/apt/trusty trusty universe" | tee -a /etc/apt/sources.list



