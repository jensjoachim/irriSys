all:
	sudo apt-get update
	sudo apt-get -y install arduino
	sudo apt-get -y install python-dev
	sudo apt-get -y install python-setuptools
	cd ../; git clone git://github.com/amperka/ino.git
	cp ino_make ../ino/Makefile
	cd ../ino; make
	cd ../ino/; mkdir test;
	cd ../ino/test; ino init -t blink;
	cd ../ino/test; ino build;
