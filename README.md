# Online-QCM-Generator-web

## What is this project?

This is a website developed in html/css and Flask for the server part. This site performs a connection management, it allows a connection as a student or teacher.
Teachers can create MCQ/Numeric/String/Open questions type questions. They can also create sequences of questions / add student accounts / view student statistics / delete questions among others.
Students only have access to one page to join a live question waiting room.
Indeed teachers can create a live question room, in this room, students can join and then the teacher will send them questions to answer.



## Structure of the project:

     -server.py -> web application server written in Flask

     - Template folder -> contains the different html pages of the site
     content:
         *main.html -> home page, returned on the '/' route.
         *login.html -> login page, returned on route '/logpage'.
         *new.html -> account creation page, returned on the '/newcompt' route.
         *hub.html -> main page of the site, groups together all the exercises already created and a button to create new ones, sent to the '/hub' route.
         *exo.html -> exercise creation page, returned on the '/exo' route.
         *display.html -> display of an exercise, possibility to try the exercise by choosing an answer, possibility to modify the exercise and to delete it if the user is the one who created it, sent back on the road '/visu/:idExercice'.
         *modificationExo.html -> exercise modification page, same exercise creation page but fill in the fields with the exercise data, returned on the route '/visu/:idExercice/modif'
         *additionEtu.html -> page for adding students from a csv file, returned on the '/addEtu' route.
         *direct.html -> adaptive live question room for host and clients, returned on route '/direct/:idsalle'.
         *hubEtu.html -> student home page, allows to join a room, sent to the '/hubEtu' route.
         *listSeq.html -> visualization of sequences, returned on the '/listSeq' route.
         *loginEtu.html -> student login page, returned on the '/loginEtu' route.
         *modifMdp.html -> page for modifying a student's password, returned on the '/modifMdp' route.
         *sequences.html -> page dec creation of a sequence, returned on the '/sequences' route.
         *stat.html -> student statistics, returned on the '/stat' route.
         *visuSeq.html -> visualization of exercises in a sequence, returned on the route '/visu/seq/:idSeq'.


     -Static Folder -> contains the different styles of html pages
     content:
         *hub.css -> style of hub.html
         *login.css -> style of login.html
         *main.css -> styling of main.html
         *new.css -> style of new.html
         *display.css -> style of display.html
         *addEtu.css -> style of addEtu.html
         *direct.css -> style of direct.html
         *stat.css -> style of stat.html

     -Download folder -> mandatory for proper operation.

     -Statistics folder -> contains the statistics files of each student in a file named with their student number


     -Files created by the server and stored on the server side:
         *Accounts.csv -> contains the different user accounts created in the form:
             "login,password" -> 'login' being a unique identifier and 'password' being the MD5 hashed password.
        
         *exercises.csv -> contains the different exercises created in the form:
             "id,title,owner,labels[],type,statement,answers[]" 'id' a unique identifier, 'owner' the creator of the exercise, labels an array of labels, type the type of question: qcm or other, answers an array of strings in the form: "answer@truthValue" truthValue=0: false; truthValue=1: true.
        
         *labels.csv -> contains the different labels created in the form:
             "label", base contains 3 default labels: "Web", "System", "Algorithmic"

         *direct.csv -> contains the rooms created, deletion of the room from the file when you can no longer join it
             "roomid,roomhost,members"

         *students.csv -> contains students added by a teacher
             "numStudent,surname,firstname,password"

         *sequences.csv -> contains the different sequences created as well as the exercises they contain
             "seqid,seqname,exercise1;exercise2;..."

         *:numEtudiant:.csv -> contains student statistics in the form:
             "idQuestion,titleQuestion,typeQuestion,statementQuestion,TruthValue(True/False)"

## How to use it ?
Server launch:

     The project was created under linux so the manipulations are not the same under windows:
     we advise you to set up your own working environment by downloading Flask and copying the project files inside to avoid any problems


     install the necessary Libraries (see "Libraries used")


     Under linux:
         In the tree at 'server.py', run:

         source venv/bin/activate
         python3 server.py
    
         Then go to the local server on the port: 5000 -> localhost:5000

    
     under windows:
         -set up your Flask environment
         -copy the project code files and folder in your environment: (server, template folder, static folder)
         -start the server: python3 server.py
         -go to localhost:5000


## Implemented features:

     -User identification and account creation: accounts are stored in 'accounts.csv'.
     - Creation of exercises.
     -Modification and deletion of exercises, management of permissions so that only the owner of the file can modify it.
     - Markdown and its functional visualization.
     - Markdown supplement: Code coloring and functional visualization.
     -Tag management, add custom tags, sort exercises by tags.

     -Connection management /!\ the connection is managed at the level of session cookies, so you have to open two different browsers to connect to two accounts at the same time on the same pc /!\

     -Creation of student account by teachers with csv file
     -different types of exercises (numerical, MCQ, character string)
     -Student statistics
     -Live question

## Features not implemented:

     - Markdown supplement: LateX, graphics.
     - Page generation that matters.


     -Small bug for the moment, do not put a comma in an answer field when creating an exercise (can be fixed very easily)
    


## Libraries used:

     python:
         -flask
         -csv
         -hashlib
         -bone
         -random
         -flask-socketio
         -simple-websocket

    
     JavaScript:
         -jquery
         -marked
         -highlight
         -mermaid (non-functional use)
         -socketio
    

## Webography:

     -ChatGPT (To answer questions but no code from it).
     -StackOverFlow
