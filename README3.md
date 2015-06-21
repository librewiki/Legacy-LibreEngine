1. install pypandoc first. (https://pypi.python.org/pypi/pypandoc/)

	Ubuntu/Debian		:	sudo apt-get install pandoc

	Fedora/Redhat		:	sudo yum install pandoc

	Mac OS X with Homebrew	:	brew install pandoc

	machine with Haskell	:	cabal-install pandoc

	Windows					:	follow this link http://pandoc.org/installing.html

	FreeBSD port 			:	follow this linkhttp://www.freshports.org/textproc/pandoc/

	Or See http://johnmacfarlane.net/pandoc/installing.html

2.	install pypandoc using pip

	pip install pypandoc

	To use pandoc filters, you must have the relevant filter installed on your machine


3.	Great Job!. Now, All the thing you need to do is copy and paste :)



git clone https://hub.librewiki.net/librewiki-dev/libreengine.git

virtualenv --python=/usr/local/bin/python3 libreengine

cd libreengine

source bin/activate



(venv) ~$ pip install -r requirements.txt

