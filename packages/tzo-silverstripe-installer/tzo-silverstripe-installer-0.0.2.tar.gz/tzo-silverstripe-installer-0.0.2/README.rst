==========================
tzo-silverstripe-installer
==========================

Automation script to create new Silverstripe site.

Installation
------------

.. code:: shell

    pip install tzo-silverstripe-installer
| Please note it require python version >=3.5. For some environment, you might need to use "pip3" instead of "pip".

Usage
-----
.. code:: shell

    tzo-create new-site
    
How it works
------------
| It will ask you some information of the project. Input then hit enter key.
| The Gitlab private token will need to be entered only the first time. Then it will be saved to the file "$YOUR_HOME/.tzo_credentials".
| For windows user, it is recommended to use git-bash terminal to use this.