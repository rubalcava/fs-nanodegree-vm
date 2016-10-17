fullstack nanodegree
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

### Prerequisites for all projects

- Virtualbox, which is available here: https://www.virtualbox.org/wiki/Downloads
- Vagrant, which is available here: https://www.vagrantup.com/


### Prerequisite steps to run all projects

- Clone or download this project. If you've downloaded it, unzip the project to a location of your choice. If you clone the project, clone it to the location of your choice.

- Once you have the project on your local machine, fire up your terminal and navigate to the project folder. If you see a file named README.md and a folder named vagrant, you are in the right place.

- In your terminal, navigate to the vagrant folder. You'll see folders called catalog, forum, and tournament, among other files. You MUST be in the vagrant folder for the rest of this to work.

- In your terminal, enter following command and press the enter key: vagrant up

- If you don't already have a vagrant VM installed, it will take some time to download. Once you are back at your terminal prompt, move on to the next step.

- Type the following command: vagrant ssh

- Once you see the following prompt, you are ready to continue: vagrant@vagrant-ubuntu-trusty-32:~$


### Next steps to run the place catalog

- In your terminal type the following and then press the enter key: cd /vagrant/catalog

- Your terminal prompt should look like this: vagrant@vagrant-ubuntu-trusty-32:/vagrant/catalog$

- Now it's time to initialize the database. In your terminal, type the following and press the enter key: python database_setup.py

- Now it's time to populate the database with some initial data. In your terminal, type the following and press the enter key: python addsuperradplaces.py

- The place catalog can now be run. In your terminal, type the following and press the enter key: python project.py

- Your terminal should show the following:  
    * Running on http://0.0.0.0:5000/
    * Restarting with reloader

- Fire up your browser and navigate to http://localhost:5000

- Use the site!

- When you're done, close your browser and head back to the terminal. Press ctrl+c to end the webserver. You should now be back at the VM'm prompt.


### Next steps to run the swiss tournament

- In your terminal type the following and then press the enter key: cd /vagrant/tournament

- Your terminal prompt should look like this: vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$

- Now it's time to initialize the database. In your terminal, type the following and press the enter key: psql

- You are now in psql and your prompt should look like this: vagrant=>

- From here, type the following command and press enter: \i tournament.sql

- You should then see the following prompt: tournament=>

- Type the following command and press the enter key to get back to your VM's prompt: \q

- To run the swiss tournament tests, enter the following command and press the enter key: python tournament_test.py

- The output will display the results of the test, and will put you back at the VM's prompt.


### Final steps to shutdown the VM once you're done

- To get out of the VM, type the following command and press the enter key: exit

- To show down the VM, type the following command and press the enter key: vagrant halt

- Thanks for trying my projects!
