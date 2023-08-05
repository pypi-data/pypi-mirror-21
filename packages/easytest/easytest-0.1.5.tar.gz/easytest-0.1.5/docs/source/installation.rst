Installation
============

There are different methods to install `easytest`.

Using conda (not working yet)
-----------------------------

The `easytest`package can be installed using conda as::

    conda install [-n YOURENV] -c conda-forge easytest

This will resolve also automatically for any potential dependencies.


Using pip
---------

The `easytest` package is provided on `pip <https://pypi.python.org/pypi/easytest>`_. Installation is as easy as::

    pip install easytest    
    

The standard python way
-----------------------

You can also download the source code package from the `project website <https://pypi.python.org/pypi/easytest>`_ or from `pip <https://pypi.python.org/pypi/easytest>`_. Unpack the file you obtained into some directory (it can be a temporary directory) and then run::

    python setup.py install

If might be that you might need administrator rights for this step, as the program tries to install into system library pathes. To install into a user specific directory you can just do

    python setup.py install --home=xxxxxxxxxx

From code repository
--------------------

Installation from the most recent code repository is also very easy in a few steps::

    # get the code
    cd /go/to/my/directory/
    git clone git@github.com:pygeo/easytest.git .

    # set the python path (consider putting these commands into your .bashrc)
    export PYTHONPATH=`pwd`:$PYTHONPATH
    echo PYTHONPATH


Test installation sucess
------------------------
Independent how you installed `easytest`, you should test that it was sucessfull by the following tests::

    python -c "import easytest"

If you don't get an error message, the module import was sucessfull.



