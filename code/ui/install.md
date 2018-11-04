# Team Cyber Docker Installation guide

### Clone the repository

```
$ git clone https://<username>@github.com/jnhunsberger/team_cyber.git
Cloning into 'team_cyber'...
remote: Enumerating objects: 197, done.
remote: Counting objects: 100% (197/197), done.
remote: Compressing objects: 100% (151/151), done.
remote: Total 283 (delta 63), reused 170 (delta 38), pack-reused 86
Receiving objects: 100% (283/283), 83.19 MiB | 3.64 MiB/s, done.
Resolving deltas: 100% (93/93), done.
$ ls
team_cyber
```

### cd to the ui folder

```
$ cd team_cyber/
$ ls
README.md	code		data		dns		gcp		papers
$ cd code/
$ ls
EDA_word_check.ipynb		cyber_eda.ipynb			download.py			merge.py
Model_LSTM_binary.ipynb		dnsutil.py			eda.py				saved_models
Model_LSTM_multiclass.ipynb	dnsutil_usage.ipynb		lstm_binary.py			test
__init__.py			docker_upload.py		merge.ipynb			ui
$ cd ui/
$ ls
backend			docker-compose.yml	frontend
```

### docker-compose

```
$ docker-compose build --no-cache
Building frontend
Step 1/9 : FROM node:8
 ---> 41a1f5b81103
Step 2/9 : RUN yarn global add @angular/cli@1.2.6
 ---> Running in 2b0d2f3f6329
yarn global v1.5.1
[1/4] Resolving packages...
warning @angular/cli > autoprefixer > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.
warning @angular/cli > cssnano > postcss-merge-rules > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.
warning @angular/cli > cssnano > postcss-merge-rules > caniuse-api > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.
warning @angular/cli > less > request > hawk > hoek@2.16.3: This version is no longer maintained. Please upgrade to the latest version.
warning @angular/cli > less > request > hawk > boom@2.10.1: This version is no longer maintained. Please upgrade to the latest version.
warning @angular/cli > less > request > hawk > boom > hoek@2.16.3: This version is no longer maintained. Please upgrade to the latest version.
warning @angular/cli > less > request > hawk > sntp > hoek@2.16.3: This version is no longer maintained. Please upgrade to the latest version.
warning @angular/cli > less > request > hawk > cryptiles@2.0.5: This version is no longer maintained. Please upgrade to the latest version.
warning @angular/cli > less > request > hawk > cryptiles > boom@2.10.1: This version is no longer maintained. Please upgrade to the latest version.
[2/4] Fetching packages...
info fsevents@1.2.4: The platform "linux" is incompatible with this module.
info "fsevents@1.2.4" is an optional dependency and failed compatibility check. Excluding it from installation.
[3/4] Linking dependencies...
warning "@angular/cli > @ngtools/webpack@1.5.5" has unmet peer dependency "enhanced-resolve@^3.1.0".
[4/4] Building fresh packages...
success Installed "@angular/cli@1.2.6" with binaries:
      - ng
Done in 26.33s.
Removing intermediate container 2b0d2f3f6329
 ---> fabf838dcfd0
Step 3/9 : WORKDIR /app
 ---> Running in b635e2981699
Removing intermediate container b635e2981699
 ---> aa303b8f0a49
Step 4/9 : COPY package.json /app
 ---> 7b73eaa6ade3
Step 5/9 : COPY yarn.lock /app
 ---> 02b0628d5255
Step 6/9 : RUN yarn install --pure-lockfile
 ---> Running in bd7ff33d8682
yarn install v1.5.1
warning package.json: No license field
warning Team-Cyber-WebApp@1.0.0: No license field
[1/4] Resolving packages...
[2/4] Fetching packages...
info fsevents@1.1.2: The platform "linux" is incompatible with this module.
info "fsevents@1.1.2" is an optional dependency and failed compatibility check. Excluding it from installation.
[3/4] Linking dependencies...
warning "@angular/cli > @ngtools/webpack@1.5.5" has unmet peer dependency "enhanced-resolve@^3.1.0".
[4/4] Building fresh packages...
Done in 21.07s.
Removing intermediate container bd7ff33d8682
 ---> d371efecd76a
Step 7/9 : COPY . /app
 ---> 7e54e7867556
Step 8/9 : CMD ng serve --host 0.0.0.0 --disable-host-check --proxy-config proxy.conf.dev.json
 ---> Running in 8b2fdc3ec322
Removing intermediate container 8b2fdc3ec322
 ---> 3cba3c5fdcba
Step 9/9 : EXPOSE 4200
 ---> Running in b8099cb5fb26
Removing intermediate container b8099cb5fb26
 ---> b9fd4e8f13d4
Successfully built b9fd4e8f13d4
Successfully tagged frontend-angular:latest
Building backend
Step 1/8 : FROM ubuntu:16.04
 ---> 0458a4468cbc
Step 2/8 : RUN apt-get update     && apt-get install -yq --no-install-recommends     python3     python3-pip
 ---> Running in 59a00539814d
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [107 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]
Get:3 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [101 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [109 kB]
Get:5 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [732 kB]
Get:6 http://archive.ubuntu.com/ubuntu xenial-backports InRelease [107 kB]
Get:7 http://archive.ubuntu.com/ubuntu xenial/universe Sources [9802 kB]
Get:8 http://security.ubuntu.com/ubuntu xenial-security/restricted amd64 Packages [12.7 kB]
Get:9 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [501 kB]
Get:10 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [3747 B]
Get:11 http://archive.ubuntu.com/ubuntu xenial/main amd64 Packages [1558 kB]
Get:12 http://archive.ubuntu.com/ubuntu xenial/restricted amd64 Packages [14.1 kB]
Get:13 http://archive.ubuntu.com/ubuntu xenial/universe amd64 Packages [9827 kB]
Get:14 http://archive.ubuntu.com/ubuntu xenial/multiverse amd64 Packages [176 kB]
Get:15 http://archive.ubuntu.com/ubuntu xenial-updates/universe Sources [287 kB]
Get:16 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [1126 kB]
Get:17 http://archive.ubuntu.com/ubuntu xenial-updates/restricted amd64 Packages [13.1 kB]
Get:18 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [901 kB]
Get:19 http://archive.ubuntu.com/ubuntu xenial-updates/multiverse amd64 Packages [18.8 kB]
Get:20 http://archive.ubuntu.com/ubuntu xenial-backports/main amd64 Packages [7965 B]
Get:21 http://archive.ubuntu.com/ubuntu xenial-backports/universe amd64 Packages [8532 B]
Fetched 25.7 MB in 6s (4267 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  ca-certificates dh-python libexpat1 libmpdec2 libpython3-stdlib
  libpython3.5-minimal libpython3.5-stdlib libsqlite3-0 libssl1.0.0
  mime-support openssl python-pip-whl python3-minimal python3.5
  python3.5-minimal
Suggested packages:
  libdpkg-perl python3-doc python3-tk python3-venv python3.5-venv
  python3.5-doc binutils binfmt-support
Recommended packages:
  file build-essential python3-dev python3-setuptools python3-wheel
The following NEW packages will be installed:
  ca-certificates dh-python libexpat1 libmpdec2 libpython3-stdlib
  libpython3.5-minimal libpython3.5-stdlib libsqlite3-0 libssl1.0.0
  mime-support openssl python-pip-whl python3 python3-minimal python3-pip
  python3.5 python3.5-minimal
0 upgraded, 17 newly installed, 0 to remove and 32 not upgraded.
Need to get 8074 kB of archives.
After this operation, 32.3 MB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libssl1.0.0 amd64 1.0.2g-1ubuntu4.13 [1083 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libpython3.5-minimal amd64 3.5.2-2ubuntu0~16.04.4 [523 kB]
Get:3 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libexpat1 amd64 2.1.0-7ubuntu0.16.04.3 [71.2 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 python3.5-minimal amd64 3.5.2-2ubuntu0~16.04.4 [1597 kB]
Get:5 http://archive.ubuntu.com/ubuntu xenial/main amd64 python3-minimal amd64 3.5.1-3 [23.3 kB]
Get:6 http://archive.ubuntu.com/ubuntu xenial/main amd64 mime-support all 3.59ubuntu1 [31.0 kB]
Get:7 http://archive.ubuntu.com/ubuntu xenial/main amd64 libmpdec2 amd64 2.4.2-1 [82.6 kB]
Get:8 http://archive.ubuntu.com/ubuntu xenial/main amd64 libsqlite3-0 amd64 3.11.0-1ubuntu1 [396 kB]
Get:9 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libpython3.5-stdlib amd64 3.5.2-2ubuntu0~16.04.4 [2132 kB]
Get:10 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 python3.5 amd64 3.5.2-2ubuntu0~16.04.4 [165 kB]
Get:11 http://archive.ubuntu.com/ubuntu xenial/main amd64 libpython3-stdlib amd64 3.5.1-3 [6818 B]
Get:12 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 dh-python all 2.20151103ubuntu1.1 [74.1 kB]
Get:13 http://archive.ubuntu.com/ubuntu xenial/main amd64 python3 amd64 3.5.1-3 [8710 B]
Get:14 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 openssl amd64 1.0.2g-1ubuntu4.13 [492 kB]
Get:15 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 ca-certificates all 20170717~16.04.1 [168 kB]
Get:16 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 python-pip-whl all 8.1.1-2ubuntu0.4 [1110 kB]
Get:17 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 python3-pip all 8.1.1-2ubuntu0.4 [109 kB]
debconf: delaying package configuration, since apt-utils is not installed
Fetched 8074 kB in 2s (3051 kB/s)
Selecting previously unselected package libssl1.0.0:amd64.
(Reading database ... 4768 files and directories currently installed.)
Preparing to unpack .../libssl1.0.0_1.0.2g-1ubuntu4.13_amd64.deb ...
Unpacking libssl1.0.0:amd64 (1.0.2g-1ubuntu4.13) ...
Selecting previously unselected package libpython3.5-minimal:amd64.
Preparing to unpack .../libpython3.5-minimal_3.5.2-2ubuntu0~16.04.4_amd64.deb ...
Unpacking libpython3.5-minimal:amd64 (3.5.2-2ubuntu0~16.04.4) ...
Selecting previously unselected package libexpat1:amd64.
Preparing to unpack .../libexpat1_2.1.0-7ubuntu0.16.04.3_amd64.deb ...
Unpacking libexpat1:amd64 (2.1.0-7ubuntu0.16.04.3) ...
Selecting previously unselected package python3.5-minimal.
Preparing to unpack .../python3.5-minimal_3.5.2-2ubuntu0~16.04.4_amd64.deb ...
Unpacking python3.5-minimal (3.5.2-2ubuntu0~16.04.4) ...
Selecting previously unselected package python3-minimal.
Preparing to unpack .../python3-minimal_3.5.1-3_amd64.deb ...
Unpacking python3-minimal (3.5.1-3) ...
Selecting previously unselected package mime-support.
Preparing to unpack .../mime-support_3.59ubuntu1_all.deb ...
Unpacking mime-support (3.59ubuntu1) ...
Selecting previously unselected package libmpdec2:amd64.
Preparing to unpack .../libmpdec2_2.4.2-1_amd64.deb ...
Unpacking libmpdec2:amd64 (2.4.2-1) ...
Selecting previously unselected package libsqlite3-0:amd64.
Preparing to unpack .../libsqlite3-0_3.11.0-1ubuntu1_amd64.deb ...
Unpacking libsqlite3-0:amd64 (3.11.0-1ubuntu1) ...
Selecting previously unselected package libpython3.5-stdlib:amd64.
Preparing to unpack .../libpython3.5-stdlib_3.5.2-2ubuntu0~16.04.4_amd64.deb ...
Unpacking libpython3.5-stdlib:amd64 (3.5.2-2ubuntu0~16.04.4) ...
Selecting previously unselected package python3.5.
Preparing to unpack .../python3.5_3.5.2-2ubuntu0~16.04.4_amd64.deb ...
Unpacking python3.5 (3.5.2-2ubuntu0~16.04.4) ...
Selecting previously unselected package libpython3-stdlib:amd64.
Preparing to unpack .../libpython3-stdlib_3.5.1-3_amd64.deb ...
Unpacking libpython3-stdlib:amd64 (3.5.1-3) ...
Selecting previously unselected package dh-python.
Preparing to unpack .../dh-python_2.20151103ubuntu1.1_all.deb ...
Unpacking dh-python (2.20151103ubuntu1.1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Setting up libssl1.0.0:amd64 (1.0.2g-1ubuntu4.13) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.22.1 /usr/local/share/perl/5.22.1 /usr/lib/x86_64-linux-gnu/perl5/5.22 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl/5.22 /usr/share/perl/5.22 /usr/local/lib/site_perl /usr/lib/x86_64-linux-gnu/perl-base .) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Setting up libpython3.5-minimal:amd64 (3.5.2-2ubuntu0~16.04.4) ...
Setting up libexpat1:amd64 (2.1.0-7ubuntu0.16.04.3) ...
Setting up python3.5-minimal (3.5.2-2ubuntu0~16.04.4) ...
Setting up python3-minimal (3.5.1-3) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Selecting previously unselected package python3.
(Reading database ... 5744 files and directories currently installed.)
Preparing to unpack .../python3_3.5.1-3_amd64.deb ...
Unpacking python3 (3.5.1-3) ...
Selecting previously unselected package openssl.
Preparing to unpack .../openssl_1.0.2g-1ubuntu4.13_amd64.deb ...
Unpacking openssl (1.0.2g-1ubuntu4.13) ...
Selecting previously unselected package ca-certificates.
Preparing to unpack .../ca-certificates_20170717~16.04.1_all.deb ...
Unpacking ca-certificates (20170717~16.04.1) ...
Selecting previously unselected package python-pip-whl.
Preparing to unpack .../python-pip-whl_8.1.1-2ubuntu0.4_all.deb ...
Unpacking python-pip-whl (8.1.1-2ubuntu0.4) ...
Selecting previously unselected package python3-pip.
Preparing to unpack .../python3-pip_8.1.1-2ubuntu0.4_all.deb ...
Unpacking python3-pip (8.1.1-2ubuntu0.4) ...
Setting up mime-support (3.59ubuntu1) ...
Setting up libmpdec2:amd64 (2.4.2-1) ...
Setting up libsqlite3-0:amd64 (3.11.0-1ubuntu1) ...
Setting up libpython3.5-stdlib:amd64 (3.5.2-2ubuntu0~16.04.4) ...
Setting up python3.5 (3.5.2-2ubuntu0~16.04.4) ...
Setting up libpython3-stdlib:amd64 (3.5.1-3) ...
Setting up openssl (1.0.2g-1ubuntu4.13) ...
Setting up ca-certificates (20170717~16.04.1) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.22.1 /usr/local/share/perl/5.22.1 /usr/lib/x86_64-linux-gnu/perl5/5.22 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl/5.22 /usr/share/perl/5.22 /usr/local/lib/site_perl /usr/lib/x86_64-linux-gnu/perl-base .) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Setting up python-pip-whl (8.1.1-2ubuntu0.4) ...
Setting up dh-python (2.20151103ubuntu1.1) ...
Setting up python3 (3.5.1-3) ...
running python rtupdate hooks for python3.5...
running python post-rtupdate hooks for python3.5...
Setting up python3-pip (8.1.1-2ubuntu0.4) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Processing triggers for ca-certificates (20170717~16.04.1) ...
Updating certificates in /etc/ssl/certs...
148 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
Removing intermediate container 59a00539814d
 ---> 34c82b7e54eb
Step 3/8 : RUN pip3 install --upgrade pip==9.0.3     && pip3 install setuptools
 ---> Running in d9a379c7a60a
Collecting pip==9.0.3
  Downloading https://files.pythonhosted.org/packages/ac/95/a05b56bb975efa78d3557efa36acaf9cf5d2fd0ee0062060493687432e03/pip-9.0.3-py2.py3-none-any.whl (1.4MB)
Installing collected packages: pip
  Found existing installation: pip 8.1.1
    Not uninstalling pip at /usr/lib/python3/dist-packages, outside environment /usr
Successfully installed pip-9.0.3
You are using pip version 9.0.3, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Collecting setuptools
  Downloading https://files.pythonhosted.org/packages/82/a1/ba6fb41367b375f5cb653d1317d8ca263c636cff6566e2da1b0da716069d/setuptools-40.5.0-py2.py3-none-any.whl (569kB)
Installing collected packages: setuptools
Successfully installed setuptools-40.5.0
You are using pip version 9.0.3, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container d9a379c7a60a
 ---> 2942b57978a4
Step 4/8 : EXPOSE 8082
 ---> Running in 6dcf8a2f8382
Removing intermediate container 6dcf8a2f8382
 ---> f025fda15bee
Step 5/8 : WORKDIR /app
 ---> Running in 45bb019ae9fc
Removing intermediate container 45bb019ae9fc
 ---> 48cc20bf841b
Step 6/8 : COPY requirements.txt /app/
 ---> bed660b8c2d1
Step 7/8 : RUN pip3 install -r /app/requirements.txt
 ---> Running in 3dc600d69363
Collecting flask (from -r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
Collecting flask-restful (from -r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/47/08/89cf8594735392cd71752f7cf159fa63765eac3e11b0da4324cdfeaea137/Flask_RESTful-0.3.6-py2.py3-none-any.whl
Collecting scikit-learn[alldeps] (from -r /app/requirements.txt (line 3))
  Downloading https://files.pythonhosted.org/packages/dc/8f/416ccf81408cd8ea84be2a38efe34cc885966c4b6edbe705d2642e22d208/scikit_learn-0.20.0-cp35-cp35m-manylinux1_x86_64.whl (5.3MB)
Collecting pandas (from -r /app/requirements.txt (line 4))
  Downloading https://files.pythonhosted.org/packages/5d/d4/6e9c56a561f1d27407bf29318ca43f36ccaa289271b805a30034eb3a8ec4/pandas-0.23.4-cp35-cp35m-manylinux1_x86_64.whl (8.7MB)
Collecting numpy (from -r /app/requirements.txt (line 5))
  Downloading https://files.pythonhosted.org/packages/86/04/bd774106ae0ae1ada68c67efe89f1a16b2aa373cc2db15d974002a9f136d/numpy-1.15.4-cp35-cp35m-manylinux1_x86_64.whl (13.8MB)
Collecting tensorflow (from -r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/3d/f1/6acf8dddd9831282cb4044a3a789c6234d6174b4b1165f31baaf788ade29/tensorflow-1.11.0-cp35-cp35m-manylinux1_x86_64.whl (63.0MB)
Collecting Keras (from -r /app/requirements.txt (line 7))
  Downloading https://files.pythonhosted.org/packages/5e/10/aa32dad071ce52b5502266b5c659451cfd6ffcbf14e6c8c4f16c0ff5aaab/Keras-2.2.4-py2.py3-none-any.whl (312kB)
Collecting click>=5.1 (from flask->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl (81kB)
Collecting Jinja2>=2.10 (from flask->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
Collecting itsdangerous>=0.24 (from flask->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/76/ae/44b03b253d6fade317f32c24d100b3b35c2239807046a4c953c7b89fa49e/itsdangerous-1.1.0-py2.py3-none-any.whl
Collecting Werkzeug>=0.14 (from flask->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/20/c4/12e3e56473e52375aa29c4764e70d1b8f3efa6682bef8d0aae04fe335243/Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
Collecting pytz (from flask-restful->-r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/f8/0e/2365ddc010afb3d79147f1dd544e5ee24bf4ece58ab99b16fbb465ce6dc0/pytz-2018.7-py2.py3-none-any.whl (506kB)
Collecting aniso8601>=0.82 (from flask-restful->-r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/69/9b/f2ae61c0c90181b62e15ca09d283d2aab42c7c2c3bbd7c548dd0cfd8bf3e/aniso8601-4.0.1-py2.py3-none-any.whl
Collecting six>=1.3.0 (from flask-restful->-r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl
Collecting scipy>=0.13.3 (from scikit-learn[alldeps]->-r /app/requirements.txt (line 3))
  Downloading https://files.pythonhosted.org/packages/cd/32/5196b64476bd41d596a8aba43506e2403e019c90e1a3dfc21d51b83db5a6/scipy-1.1.0-cp35-cp35m-manylinux1_x86_64.whl (33.1MB)
Collecting python-dateutil>=2.5.0 (from pandas->-r /app/requirements.txt (line 4))
  Downloading https://files.pythonhosted.org/packages/74/68/d87d9b36af36f44254a8d512cbfc48369103a3b9e474be9bdfe536abfc45/python_dateutil-2.7.5-py2.py3-none-any.whl (225kB)
Collecting setuptools<=39.1.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/8c/10/79282747f9169f21c053c562a0baa21815a8c7879be97abd930dbcf862e8/setuptools-39.1.0-py2.py3-none-any.whl (566kB)
Collecting tensorboard<1.12.0,>=1.11.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/9b/2f/4d788919b1feef04624d63ed6ea45a49d1d1c834199ec50716edb5d310f4/tensorboard-1.11.0-py3-none-any.whl (3.0MB)
Collecting absl-py>=0.1.6 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/0c/63/f505d2d4c21db849cf80bad517f0065a30be6b006b0a5637f1b95584a305/absl-py-0.6.1.tar.gz (94kB)
Collecting wheel>=0.26 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/5a/9b/6aebe9e2636d35d1a93772fa644c828303e1d5d124e8a88f156f42ac4b87/wheel-0.32.2-py2.py3-none-any.whl
Collecting astor>=0.6.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/35/6b/11530768cac581a12952a2aad00e1526b89d242d0b9f59534ef6e6a1752f/astor-0.7.1-py2.py3-none-any.whl
Collecting keras-applications>=1.0.5 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/3f/c4/2ff40221029f7098d58f8d7fb99b97e8100f3293f9856f0fb5834bef100b/Keras_Applications-1.0.6-py2.py3-none-any.whl (44kB)
Collecting termcolor>=1.1.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/8a/48/a76be51647d0eb9f10e2a4511bf3ffb8cc1e6b14e9e4fab46173aa79f981/termcolor-1.1.0.tar.gz
Collecting protobuf>=3.6.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/bf/d4/db7296a1407cad69f043537ba1e05afab3646451a066ead7a314d8714388/protobuf-3.6.1-cp35-cp35m-manylinux1_x86_64.whl (1.1MB)
Collecting grpcio>=1.8.6 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/75/8b/b8db0b4a855b1b959313fe4aa6e0704e2c05bef00e47d7b563112e40a704/grpcio-1.16.0-cp35-cp35m-manylinux1_x86_64.whl (9.7MB)
Collecting gast>=0.2.0 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/5c/78/ff794fcae2ce8aa6323e789d1f8b3b7765f601e7702726f430e814822b96/gast-0.2.0.tar.gz
Collecting keras-preprocessing>=1.0.3 (from tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/fc/94/74e0fa783d3fc07e41715973435dd051ca89c550881b3454233c39c73e69/Keras_Preprocessing-1.0.5-py2.py3-none-any.whl
Collecting h5py (from Keras->-r /app/requirements.txt (line 7))
  Downloading https://files.pythonhosted.org/packages/d9/0a/f0dd6d533d6b5bd4c1ca186af2792186885a90b84df41f3e6867466761fc/h5py-2.8.0-cp35-cp35m-manylinux1_x86_64.whl (2.8MB)
Collecting pyyaml (from Keras->-r /app/requirements.txt (line 7))
  Downloading https://files.pythonhosted.org/packages/9e/a3/1d13970c3f36777c583f136c136f804d70f500168edc1edea6daa7200769/PyYAML-3.13.tar.gz (270kB)
Collecting MarkupSafe>=0.23 (from Jinja2>=2.10->flask->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz
Collecting markdown>=2.6.8 (from tensorboard<1.12.0,>=1.11.0->tensorflow->-r /app/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/7a/6b/5600647404ba15545ec37d2f7f58844d690baf2f81f3a60b862e48f29287/Markdown-3.0.1-py2.py3-none-any.whl (89kB)
Installing collected packages: click, MarkupSafe, Jinja2, itsdangerous, Werkzeug, flask, pytz, aniso8601, six, flask-restful, numpy, scipy, scikit-learn, python-dateutil, pandas, setuptools, wheel, markdown, grpcio, protobuf, tensorboard, absl-py, astor, h5py, keras-applications, termcolor, gast, keras-preprocessing, tensorflow, pyyaml, Keras
  Running setup.py install for MarkupSafe: started
    Running setup.py install for MarkupSafe: finished with status 'done'
  Found existing installation: setuptools 40.5.0
    Uninstalling setuptools-40.5.0:
      Successfully uninstalled setuptools-40.5.0
  Running setup.py install for absl-py: started
    Running setup.py install for absl-py: finished with status 'done'
  Running setup.py install for termcolor: started
    Running setup.py install for termcolor: finished with status 'done'
  Running setup.py install for gast: started
    Running setup.py install for gast: finished with status 'done'
  Running setup.py install for pyyaml: started
    Running setup.py install for pyyaml: finished with status 'done'
Successfully installed Jinja2-2.10 Keras-2.2.4 MarkupSafe-1.0 Werkzeug-0.14.1 absl-py-0.6.1 aniso8601-4.0.1 astor-0.7.1 click-7.0 flask-1.0.2 flask-restful-0.3.6 gast-0.2.0 grpcio-1.16.0 h5py-2.8.0 itsdangerous-1.1.0 keras-applications-1.0.6 keras-preprocessing-1.0.5 markdown-3.0.1 numpy-1.15.4 pandas-0.23.4 protobuf-3.6.1 python-dateutil-2.7.5 pytz-2018.7 pyyaml-3.13 scikit-learn-0.20.0 scipy-1.1.0 setuptools-39.1.0 six-1.11.0 tensorboard-1.11.0 tensorflow-1.11.0 termcolor-1.1.0 wheel-0.32.2
You are using pip version 9.0.3, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container 3dc600d69363
 ---> d42f46f3df56
Step 8/8 : CMD python3 /app/ui/backend/app.py
 ---> Running in 6fbc5e9ee432
Removing intermediate container 6fbc5e9ee432
 ---> 2b52693fe6fa
Successfully built 2b52693fe6fa
Successfully tagged backend-flask:latest
```

### Run the containers (Ignore the frontend container errors for now)
```
$ docker-compose up
Recreating cyber-backend  ... done
Recreating cyber-frontend ... done
Attaching to cyber-backend, cyber-frontend
cyber-backend | 2018-11-04 21:32:38.213810: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
cyber-backend | SAVED MODEL IS NOW LOADED!
cyber-backend |  * Serving Flask app "app" (lazy loading)
cyber-backend |  * Environment: production
cyber-backend |    WARNING: Do not use the development server in a production environment.
cyber-backend |    Use a production WSGI server instead.
cyber-backend |  * Debug mode: on
cyber-backend | Using TensorFlow backend.
cyber-backend |  * Running on http://0.0.0.0:8082/ (Press CTRL+C to quit)
cyber-backend |  * Restarting with stat
cyber-frontend | Cannot read property 'config' of null
cyber-frontend | TypeError: Cannot read property 'config' of null
cyber-frontend |     at Class.run (/app/node_modules/@angular/cli/tasks/serve.js:21:63)
cyber-frontend |     at check_port_1.checkPort.then.port (/app/node_modules/@angular/cli/commands/serve.js:110:26)
cyber-frontend |     at <anonymous>
cyber-frontend |     at process._tickCallback (internal/process/next_tick.js:188:7)
cyber-frontend exited with code 1
cyber-backend | 2018-11-04 21:32:41.163311: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
cyber-backend | Using TensorFlow backend.
cyber-backend |  * Debugger is active!
cyber-backend |  * Debugger PIN: 200-875-271
```
### Launch a rest query from postman

Note that you will need to use a api port number that is exposed outside the container. The committed docker-compose file has external port number 18082 mapped to 8082.

```
127.0.0.1:18082/?query=google.com
127.0.0.1:18082/?query=netflix.com
127.0.0.1:18082/?query=zcsfsdferewrewrw.com
```

### Alternatively, you can use curl

```
$ curl "127.0.0.1:18082/?query=news.google.com"
{
    "type": "Benign",
    "url": "news.google.com"
}
```
### you will see logs like this on docker-compose window
```
cyber-backend | 172.27.0.1 - - [04/Nov/2018 21:56:41] "GET /?query=google.com HTTP/1.1" 200 -
cyber-backend | 172.27.0.1 - - [04/Nov/2018 21:56:52] "GET /?query=netflix.com HTTP/1.1" 200 -
cyber-backend | 172.27.0.1 - - [04/Nov/2018 21:57:11] "GET /?query=zcsfsdferewrewrw.com HTTP/1.1" 200 -
cyber-backend | 172.27.0.1 - - [04/Nov/2018 23:02:45] "GET /?query=news.google.com HTTP/1.1" 200 -
```
