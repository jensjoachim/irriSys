all:
	# Install nessesary packages
	sudo apt-get update
	sudo apt-get -y upgrade
	sudo apt-get -y install arduino
	sudo apt-get -y install python-dev
	sudo apt-get -y install python-setuptools
	# Get ino project and make
	cd ../; git clone git://github.com/amperka/ino.git
	cp ino_make ../ino/Makefile
	cd ../ino; make
	# Start a new uno project
	cd ../ino/; mkdir workspace;
	cd ../ino/workspace; ino init -t blink;
	cd ../ino/workspace; ino build;
	# Copy original project and build
	cp -r arduino_code/* ../ino/workspace/
	cd ../ino/workspace; ino build;
	# Copy wifi settings
	sudo cp network/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
	sudo reboot
