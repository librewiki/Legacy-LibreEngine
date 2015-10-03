# 리브레 엔진
리브레 위키의 새로운 엔진이다.

이슈는 [리브레 위키 이슈 트래커](https://issue.librewiki.net)로 제출해 주세요.

# 안까먹게 적어두자 / Ubuntu 14.04 개발환경 갖추기

sudo apt-get install python3-setuptools

sudo apt-get install python3-pip

sudo pip3 install virtualenv

폴더 하나 생성해서 들어간뒤

virtualenv venv

. venv/bin/activate

새로운 패키지를 추가하려면

(env) ~$ pip install package

프로젝트를 클론해서 다시 구축할 때에는

(env) ~$ pip install -r requirements.txt
