Development
===========

Initial installation
--------------------

#. Install prerequisites::

    sudo apt-get install python-dev build-essential pkg-config python-pip
    sudo apt-get install libssl-dev libffi-dev

#. Make sure that Python 2.7.12 is installed::

    python --version

#. Install and configure git::

    sudo apt-get install git
    git config --global user.name 'Firstname Lastname'
    git config --global user.email 'youremail@youremail_domain.com'

#. Fork https://github.com/dmugtasimov/dmu-utils repository

#. Clone forked repository (replace <username> with your github account name)::

    git clone git@github.com:<username>/dmu-utils.git
    cd dmu-utils

#. Create .gitignore::

    cat << EOF >> .gitignore
    .gitignore
    *.py[cod]
    /local/
    # insert personal development environment entries here
    EOF

#. Install virtualenvwrapper::

    sudo pip install virtualenv
    sudo pip install setuptools
    pip install --user virtualenvwrapper
    cat << EOF >> ~/.bashrc
    export WORKON_HOME=$HOME/.virtualenvs
    source ~/.local/bin/virtualenvwrapper.sh
    EOF

    export WORKON_HOME=$HOME/.virtualenvs
    source ~/.local/bin/virtualenvwrapper.sh

#. Create virtualenv::

    mkvirtualenv dmu-utils

#. Install Python prerequisites::

    pip install setuptools==34.3.3
    pip install pip==9.0.1

#. Continue with `Upgrade`_ section

Upgrade
-------

#. Install dmu-utils in development mode::

    cd dmu-utils
    workon dmu-utils
    pip install -e .[dev]


Run tests
---------

#. Activate virtual env::

    cd dmu-utils
    workon dmu-utils

#. With pytest::

    pytest
    # or
    mkdir tmp
    pytest --cov-report annotate:./tmp/cov_annotate --cov=dmu_utils

Various tasks
-------------

#. Remove all .pyc and .pyo files::

    find . -name '*.pyc' -delete
    find . -name '*.pyo' -delete
