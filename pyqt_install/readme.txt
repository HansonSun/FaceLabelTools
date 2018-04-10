安装SIP

从 http://www.riverbankcomputing.co.uk/software/sip/download 下载压缩包 sip-4.19.tar.gz 解压
cd /home/PyQt/sip-4.19
sudo python configure.py  
sudo make install  
 

安装Qt4依赖的库

sudo apt-get install qt4-dev-tools qt4-doc qt4-qtconfig qt4-demos qt4-designer  
sudo apt-get install libqwt5-qt4 libqwt5-qt4-dev  



安装PyQt4


tar zxvf PyQt4_gpl_x11-4.12.tar.gz -C /home/PyQt  
cd /home/PyQt/PyQt4_gpl_x11-4.12 
sudo python configure.py  
sudo make  
sudo make install  
 