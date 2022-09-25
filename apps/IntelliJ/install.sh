echo "Downloading IntelliJ..."
wget -O /tmp/intellij.tar.gz https://download.jetbrains.com/idea/ideaIC-${version}.tar.gz
echo "Extracting archive..."
tar -xvf /tmp/intellij.tar.gz -C /opt/
rm /tmp/intellij.tar.gz
mv /opt/idea* /opt/intellij
echo "[Desktop Entry]
Type=Application
Name=IntelliJ IDEA
Icon=/opt/intellij/bin/idea.png
Exec=bash /opt/intellij/bin/idea.sh
Comment=Java IDE
Categories=Development;IDE;Programming;
Terminal=false
StartupWMClass=jetbrains-intellij-idea
StartupNotify=true" > /usr/share/applications/jetbrains-intellij.desktop
echo "Installation complete"