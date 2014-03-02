threadable-pygments
===================

Add syntax highlighting to your incoming emails

To run your own instance for highlighting code with Threadable, install the Heroku toolbelt. Then:

    git co https://github.com/otherio/threadable-pygments.git
    cd threadable-pygments
    heroku create
    git push heroku master

To run locally for development on osx:

  - install pip and virtualenv

    `sudo easy_install pip`
    `sudo pip install virtualenv`

  - set up a virtual enviroment

    `virtualenv venv --distribute`
    `source venv/bin/activate`

  - install dependencies

    `pip install -r requirements.txt`

  - start the app

    `foreman start`

Testing:

    python highlight_tests.py

