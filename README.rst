=====================
django-project-layout
=====================

django-project-layout은 Django 1.5 기반으로 프로젝트 생성시, 실제 사용에 편리한 레이아웃을 만들어주는 템플릿입니다.

이걸 왜 쓰나요?
=========

Django의 기본 레이아웃을 그냥 사용하면, 로컬 테스트에서는 쓸만하지만, 소스코드를 관리하면서 개발환경, 테스트환경, 운영환경 등을 구분해주기 쉽지 않습니다.

하지만 이걸 쓰신다면 상황에 따라 분리된 환경을 구축해놓고 시작하실 수 있습니다.

설정 파일도 각 환경별로 나누어서, 기본 설정인 ``settings.base``\ 를 확장해 각각의 환경에 맞는 세팅을 선택해서 사용할 수 있습니다. ::

   $ ./manage.py runserver --settings=project_name.settings.spy_dev
   # 또는
   $ export DJANGO_SETTINGS_MODULE=project_name.settings.spy_dev
   $ ./manage.py runserver

이런 식으로 테스트 서버를 돌릴때도 직접 세팅파일을 설정해서 각 개발자가 자신에 환경에 맞출 수 있습니다.

* ``manage.py``\ 는 디폴트로 ``<project_name>.settings.local`` 모듈을 참조하도록 되어 있습니다. 프로젝트 전체에 공유되는 설정이 아니라 개발 환경에서만 사용되는 설정은 ``<project_name>/settings/local.py`` 파일을 수정해서 사용하세요.

가상환경 설정하기
=========

Python 프로젝트를 진행하실때는 가상환경을 만들어서 하시는게 좋습니다.

`pythonbrew`_\ 를 이용해서 가상환경을 만드시길 추천합니다.
만드는 방법은 `여기`_\ 를 참조하시면 편합니다만 간략하게 정리해드리겠습니다. ::

   # 설치
   $ curl -kL http://xrl.us/pythonbrewinstall | bash

   # 프로필 설정 (.bashrc, .profile 등)
   $ vi ~/.bash_profile

   이것을 추가하세요
   [[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc

   # 현재 설치된 pythonbrew 버전 확인
   $ pythonbrew --version

   # pythonbrew에 설치된 python 버전별 목록 확인
   $ pythonbrew list -k

   # python 2.7.3 인스톨 하기
   $ pythonbrew install 2.7.3

   # 사용할 python 버전 선택하기
   $ pythonbrew switch 2.7.3

   # 가상환경을 만들기 위한 초기화(현재 사용중인 python버전별로 한번만 실행해주면 됩니다.)
   $ pythonbrew venv init

   # 가상환경 생성
   $ pythonbrew venv create venv_name

   # 가상환경 이용
   $ pythonbrew venv use venv_name

   # 가상환경에서 빠져나오기
   $ deactivate

   # 가상환경 삭제
   $ pythonbrew venv delete venv_name

   # 현재 만들어져있는 가상환경 목록 확인
   $ pythonbrew venv list

pythonbrew가 맘에 안드신다면 `virtualenvwrapper`_\ 를 사용해 가상화 환경을 구축할 수 있습니다. ::

   # 설치
   $ sudo pip install virtualenvwrapper

   # 가상환경 생성
   $ mkvirtualenv venv_name

   # 가상환경 이용
   $ workon venv_name

   # 가상환경에서 빠져나오기
   $ deactivate

   # 가상환경 삭제
   $ rmvirtualenv venv_name

   # 현재 만들어져있는 가상환경 목록 확인
   $ lsvirtualenv
   또는
   $ workon

보다 자세한 내용은 `virtualenvwrapper installation`_\ 을 참고하세요.

.. _여기: http://suvashthapaliya.com/blog/2012/01/sandboxed-python-virtual-environments/
.. _pythonbrew: https://github.com/utahta/pythonbrew
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _virtualenvwrapper installation: http://virtualenvwrapper.readthedocs.org/en/latest/install.html


Django 설치하기
===========

``django-admin.py`` 명령을 실행하기 위해, 먼저 Django를 설치해야 합니다. ::

   # Django 1.5 설치
   $ pip install django

프로젝트 만들기
========

'**icecream**' 이라는 이름의 Django프로젝트를 django-project-layout을 이용해 만드려면 다음 명령을 실행하세요. ::

    $ django-admin.py startproject --template=https://github.com/smartstudy/django-project-layout/zipball/v1.11 \
                                   --extension=py,rst,html,in,gitignore \
                                   icecream

다른 이름의 프로젝트를 만드시려면 '**icecream**' 부분만 바꾸고 그대로 쓰시면 됩니다.

패키지 설치하기
========

프로젝트를 만든 후 프로젝트에 기본적으로 사용되는 패키지를 설치해야 합니다. 다음과 같이 간단하게 설치할 수 있습니다. ::

   # 개발환경
   $ pip install -e .[local]

   # 운영환경
   $ pip install .
   # 또는
   $ python setup.py install

운영환경을 위한 환경변수 설정
================

SECRET_KEY가 소스상에 노출되지 않게 하기 위해, 환경변수에 SECRET_KEY를 등록하여 읽어옵니다.
bash 쉘을 기준으로, .bashrc, .bash_profile, .profile 등 프로필 파일을 찾아 다음과 같은 방식으로 등록합니다. ::

   export SECRET_KEY=s6m437a7r3t_s7tu75d4y4

SECRET_KEY는 절대 노출되서는 안됩니다. Django 1.5부터 SECRET_KEY가 설정되어 있지 않으면 서버가 실행되지 않습니다.

잘 되는지 확인하기
==========

django-project-layout으로 생성된 프로젝트를 잘 되는지 확인해보려면 다음 내용을 진행해보세요. ::

   # runserver 실행을 하기 위해서는 admin 모듈이 활성화 되어있기에 syncdb 해야합니다. 
   $ python manage.py syncdb
   
   # runserver 실행 (local 세팅이 기본적으로 사용됩니다.)
   $ python manage.py runserver

이제 브라우저로 확인하시면 됩니다.
