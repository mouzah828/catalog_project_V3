#catalog project
##This project is a website showing video games category with their games for each category, allowing athourized user to add, delete and update their items and category

##In order to run this project you have to follow this steps:
1. you nedd to have virtual machine installed in your PC, so install VirtualBox
2. Install Vagrant
3. Download the VM configuration  form https://github.com/udacity/fullstack-nanodegree-vm, save and unzip the FSND-Virtual-Machine.zip to your machine
4. After Finish installation, start the virtual machine by opening your terminal such as Git Bash

### before run this command change your directory into inside the vagrant subdirectory, and run the following command in order:
5. vagrant up
6. vagrant ssh
7. place my project folder "catalog" in vagrant directory
8. cd /vagrant
9. change your directory to my project by run this command: cd catalog
10. run the database_setup code to create the database , by this command:python database_setup.py
11. run the lotsofmenus code to insert more items and data to your database , by this command: python lotsofmenus.py
12. run the python code that is inside project folder by this command: python application.py
13. run this command $pip freeze > requirements.txt fro generating requirements.txt which includes all imports files
14. run $pip install -r requirements.txt to install required import files to run this application
15. Go to your browser and write the this url:http://localhost:5000/catalog/
16. Go to this url http://localhost:5000/catalog.json to view database in JSON format



