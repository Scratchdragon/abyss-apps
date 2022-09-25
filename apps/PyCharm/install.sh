echo "Downloading PyCharm..."
wget -O /tmp/pycharm.tar.gz https://download.jetbrains.com/python/pycharm-community-${version}.tar.gz
echo "Extracting archive..."
tar -xvf /tmp/pycharm.tar.gz -C /opt/
rm /tmp/pycharm.tar.gz
mv /opt/pycharm* /opt/pycharm
echo "[Desktop Entry]
Type=Application
Name=PyCharm Community Edition
Icon=/opt/pycharm/bin/pycharm.png
Exec=bash /opt/pycharm/bin/pycharm.sh
Comment=Python IDE
Categories=Development;IDE;Programming;
Terminal=false
StartupWMClass=jetbrains-pycharm-ce
StartupNotify=true" > /usr/share/applications/jetbrains-pycharm.desktop
echo "Installation complete"