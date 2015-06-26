리브레위키 구성요소
├── LibreEngine
│   ├── conf <= 리브레엔진의 설정파일이 위치하는 폴더입니다.
│   ├── files <= ? 
│   ├── include <= 리브레엔진의 백엔드를 구동하는 핵심코드들이 위치하는 폴더입니다.
│   ├── lib <= 리브레엔진을 구동하는데 필요한 라이브러리들이 위치하는 폴더입니다.
│   ├── static <= CSS, JS, 이미지파일등 웹페이지의 구성요소들이 위치하는 폴더입니다.
│   ├── templates <= 리브레엔진의 프론트엔드 구성요소들이 위치하는 폴더입니다.
│   └── __init__.py <= 
├── server.py

파일들에대한 설명
libreengine/Libreengine/conf/config.py <= 서버를 구동할때 호스트주소, 포트, 페이지이름 등을 지정할수 있는 파일. Flask의 run옵션을 조정하기위한 파일입니다. 이 파일은 서버구동파일인 server.py와 직접적인 연관이 있습니다.
libreengine/Libreengine/conf/database.py <= 데이터베이스 서버를 접속할때 쓰이는 설정을 지정하기위한 파일. 이 파일은 ../include/dbConnect.py와 관련이 있습니다.
libreengine/Libreengine/include/models.py <= ./include/route.py파일을 간결하게 작성하기위해 자주쓰이는 함수들을 정의하기위해 만들어진 파일입니다.
libreengine/Libreengine/include/routes.py <= 서버의 가장 중요한 백엔드 파일입니다. 
libreengine/Libreengine/__init__.py <= 서버의 구동설정파일인 ./conf/config.py파일을 로드하고 ./include/routes.py 파일을 로드하여 플라스크 프레임워크의 틀을 만들어주는 파일입니다.
libreengine/Libreengine/templates/* ##추가해야함##
libreengine/server.py <= 서버의 구동파일. ./Libreengine폴더의 요소들로 구동됩니다.




1. install pandoc to use pypandoc. ref.(https://pypi.python.org/pypi/pypandoc/)
    pypandoc라이브러리 사용을 위해 pandoc을 설치합니다. 

	Ubuntu/Debian		:	sudo apt-get install pandoc

	Fedora/Redhat		:	sudo yum install pandoc

	Mac OS X with Homebrew	:	brew install pandoc

	machine with Haskell	:	cabal-install pandoc

	Windows					:	follow this link http://pandoc.org/installing.html

	FreeBSD port 			:	follow this linkhttp://www.freshports.org/textproc/pandoc/

	Or See http://johnmacfarlane.net/pandoc/installing.html

2.	install pypandoc using pip
    pip을 이용하여 pypandoc을 설치합니다.

	pip install pypandoc

	To use pandoc filters, you must have the relevant filter installed on your machine


3.	Great Job!. Now, All the thing you need to do is copy and paste :)
    잘하셨습니다!. 이제 아래 커맨드를 커맨드라인에 복사&붙여넣기 할일만 남았어요! ㅎ_ㅎ
    
    
   

#git에서 리브레엔진 재배포패키지를 다운받습니다.
git clone https://hub.librewiki.net/librewiki-dev/libreengine.git

#virtialenv환경을 세팅하여 환경설정을 시작할 준비를 합니다.
virtualenv --python=/usr/local/bin/python3 libreengine

# :D
cd libreengine

# virtualenv환경 구동 커맨드
source bin/activate


# requirement.txt 파일에 기록되어있는 필수패키지를 설치합니다.
(venv) ~$ pip install -r requirements.txt


pypy server.py
