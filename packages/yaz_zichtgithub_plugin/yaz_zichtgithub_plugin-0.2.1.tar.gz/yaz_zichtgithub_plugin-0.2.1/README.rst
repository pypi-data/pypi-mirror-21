=======================
A github plugin for YAZ
=======================

TODO: Short description here


Installing
----------

    .. code-block:: bash

        pip3 install --upgrade yaz_zichtgithub_plugin

        # Call the installed script
        yaz-zichtgithub


Developing
----------

    .. code-block:: bash

        # Get the code
        git clone git@github.com:boudewijn-zicht/yaz_zichtgithub_plugin.git
        cd yaz_zichtgithub_plugin

        # Ensure you have python 3.5 or higher and yaz installed
        python3 --version
        pip3 install --upgrade yaz

        # Setup your virtual environment
        virtualenv --python=python3 env
        source env/bin/activate

        # Run tests
        python setup.py test

        # Or run nosetests directly (allows coverage report)
        nosetests --with-cover --cover-html --cover-package yaz_zichtgithub_plugin

        # Upload a new release to pypi
        python setup.py sdist upload --repository pypi

        # Once you are done... exit your virtual environment
        deactivate


Maintainer(s)
-------------

- Boudewijn Schoon <boudewijn@zicht.nl>
