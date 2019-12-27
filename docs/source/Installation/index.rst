Installation Guide
===============

Pulling this project to your computer is not enough to run it. You should install some python packages in addition to the python. 
1. First you should install pyhton (>=3.4)  
A useful source for this : http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

2. You should install flask, we have used this framerk.

.. code-block:: console

    pip3 install -U flask

3. You should install Psycopg2 which is Python-PostgreSQL Database Adapter.

.. code-block:: console

    pip3 install -U psycopg2-binary

4. You shuold install a few packages which are reqiured.

.. code-block:: console

    pip3 install flask-login
    pip3 install passlib==1.7.2
    pip3 install gunicorn>=19.9
    pip3 install Flask-WTF==0.14
    pip3 install WTForms-Components==0.10.4
    pip3 install colour==0.1.5


5.Lastly, You can run this project in your local host, a link will be given to you (http://127.0.0.1:5000/) 
.. code-block:: console

   python server.py

