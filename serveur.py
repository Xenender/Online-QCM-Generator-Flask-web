from flask import Flask,request,render_template,redirect,session
import csv
import hashlib #encrypt MD5
import os

import threading #stopper fonction si trop de temps à repondre

import random

from flask_socketio import SocketIO,join_room, leave_room,emit

#COR

import numpy as np #correcteur automatique
from collections import defaultdict
import math
import itertools #permutations


app = Flask(__name__)
app.config['SECRET_KEY'] = "P_as_swo-rd_Ap_p_S-e_c_r-e_t-K_e_y"
app.secret_key = "P_as_swo-rd_Ap_p_S-e_c_r-e_t-K_e_y" #pour pouvoir utilise session[]

socketio = SocketIO(app)


#CHANGEMENT !

def csvcount(file):#compte le nombre d'entrées dans un fichier csv

    i = 0
    for ligne in file:
        i += 1
    return i

#init
idQ=0
idS=0
username="null"


#tester si le fichier d'enregistrement des exercices existe
try:
    #le fichier existe

    #on trouve l'id le plus élevé
    max=0
    with open('exercices.csv', 'r') as file:
        reader = csv.reader(file)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(int(row[0]) > max):
                    max = int(row[0])

    idQ = max+1

    file.close()
except FileNotFoundError:
    #le fichier existe pas
    file = open('exercices.csv',"w",newline='') #création du fichier
    file.close()
    idQ=0



#tester si le fichier d'enregistrement des Comptes existe
try:
    #le fichier existe
    file = open('comptes.csv',"r")
    file.close()
except FileNotFoundError:
    #le fichier existe pas
    file = open('comptes.csv',"w",newline='') #création du fichier
    file.close()


try:
    #le fichier existe
    file = open('etiquettes.csv',"r")

    file.close()
except FileNotFoundError:
    #le fichier existe pas
    file = open('etiquettes.csv',"w",newline='') #création du fichier
    writers=csv.writer(file)
    for etiquette in ["Algorithmique","Web","Systeme"]: #etiquettes de base

        writers.writerow([etiquette])

    file.close()


try:
    #le fichier existe
    file = open('etudiants.csv',"r")
    file.close()
except FileNotFoundError:
    #le fichier existe pas
    file = open('etudiants.csv',"w",newline='') #création du fichier
    file.close()

file = open('direct.csv',"w",newline='') #création du fichier qui stocke les salles de questions directes ouvertes 
file.close()
    
 
 #tester si le fichier d'enregistrement des sequences existe
try:
    #le fichier existe

    #on trouve l'id le plus élevé
    max=0
    with open('sequences.csv', 'r') as file:
        reader = csv.reader(file)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(int(row[0]) > max):
                    max = int(row[0])

    idS = max+1

    file.close()
except FileNotFoundError:
    #le fichier existe pas
    file = open('sequences.csv',"w",newline='') #création du fichier
    file.close()
    idS=0



#fieldnames = ["id","title","username","tag","type","question","answer"]
    


@app.route('/')
def index():
    return render_template("main.html")


    

@app.route('/visu/<id>')
def aff(id):
    
    data={}
    with open("exercices.csv", 'r') as file:   
        reader = csv.reader(file)
        for ligne in reader:     #Pour chaques exos
            if ligne:
                row = [x for x in ligne] 
                r1=row[6][1:]         # on enlève les '[' et ']' pour la liste des réponses
                r2=r1[:-1]
                r2=r2.replace("'", '')  
                r3=r2.split(',')
                r4=[]
                for i in range(len(r3)):  #séparation de la question et de sa valeur (1 juste,0 faux)  question@1 et ajout dans un tableau
                    c=r3[i].split('@')
                    r4.append(c)


                

                data = {"id":row[0],"title": row[1], "username": row[2], "tag": row[3].split(','), "type": row[4], "question": row[5], "answer": r4}
                if row[0]==id:   #si id est égal à celui souhaité sur la route /visu/<id>
                    return render_template("affichage.html",username=session["username"],data=data)
                else: # on réinitialise data si pas correspondant
                    data={}
    return "erreur, l'exercice n'existe pas"  # cas ou on donne un id inexistant


@app.route('/visu/<id>/modif')
def modif(id):
    
    with open("exercices.csv", 'r') as file:

        data = []
        with open('exercices.csv', 'r') as file:
            reader = csv.reader(file)
            for ligne in reader:
                if(ligne):#Si la ligne existe
                    row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                    if(row[0]==id):
                        data = row #data est la ligne représentant l'exercice souhaité
        
        if(session["username"]==data[2]):#on teste si l'utilisateur qui demande la modification est le propriétaire de l'exercice
            r1=data[6][1:]# on enlève les '[' et ']' pour la liste des réponses
            r2=r1[:-1]

            r2=r2.replace("'", '')
            r3=r2.split(',')
            r4=[]
            for i in range(len(r3)):#séparation de la question et de sa valeur (1 juste,0 faux)  question@1 et ajout dans un tableau
                c=r3[i].split('@')
                r4.append(c)

            c1=data[3][1:]
            c2=c1[:-1]

            c2=c2.replace("'", '')#suppression des espaces et quote
            c2 = c2.replace(" ","")
            c3=c2.split(',')
            


        tabEti = []
        with open("etiquettes.csv","r") as file:  #on donne enh parametre de render_template le tableau des étiquettes pour que la page les affiches
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEti.append(row)


            
        return render_template("/modificationExo.html",data = data,reponses=r4,tags=c3,idExo=id,tabEti=tabEti)


@app.route('/visu/<id>/delete')
def delete(id):
    
    
    data = []
    with open('exercices.csv', 'r') as file:
        reader = csv.reader(file)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(row[0]==id):
                    data = row
    
    if(session["username"]==data[2]):#on teste si l'utilisateur qui demande la modification est le propriétaire de l'exercice

        lines = []
        with open('exercices.csv', 'r') as file:#on recréé le fichier exercice sans la ligne réprésentant l'exercice à supprimer
            reader = csv.reader(file)
            for ligne in reader:
                if(ligne):
                    row = [x for x in ligne]
                    if(row[0]!=id):
                        lines.append(row)
                    

        with open('exercices.csv', 'w',newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        return redirect("/hub")
            
@app.route('/hubEtu')
def hubEtu():
    return render_template("hubEtu.html")

@app.route('/hub',methods=['GET', 'POST'])
def hub():
   
   #récupération des étiquettes
    with open("etiquettes.csv", 'r') as file:
        reader= csv.reader(file)
        tab=[]
        for ligne in reader:
            if ligne:
                tab.append(ligne)

    etiquette=[]
    for i in range(len(tab)):
        etiquette.append(tab[i][0])

    
    #récupération des exercices
    with open('exercices.csv',"r") as file:
        reader= csv.reader  (file)
        tab=[]
        
        for ligne in reader:
            if(ligne):
                row=ligne  # on enlève les [ ] du tableau des tags
                r1=row[3][1:]
                r2=r1[:-1]
                r2=r2.replace("'", '')
                r3=r2.split(',')
                tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": r3, "type": row[4], "question": row[5], "answer": row[6]})

        

    if request.method == "POST":   # cas ou on souhaite trier
        eti = request.form.get("etiquette")   
        return render_template("hub.html",eti=eti,tab=tab,username=session["username"],etiquette=etiquette)
    else:
        return render_template("hub.html",tab=tab,username=session["username"],etiquette=etiquette)  #cas de base



# controle
@app.route('/controle')
def controle():

    tabEti = []
    with open("etiquettes.csv","r") as file:  #on donne le tableau des étiquettes pour que la page les affiches
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEti.append(row)

    return render_template('controle.html',tabEti=tabEti)


def GenereExamens(exercices,etiquettes,nbSujets,nbExercices,shuffle,resultat,timeout_event):

    TTL = 2000
    expired = False

    #todo: tester si c'est possible : assez d'exercices avec etiquette demandée , assez de sujet possibles

    def nombreParTag():
        nbQ=0
        nbParTag = [-1 for x in etiquettes]#nbParTag[0] contient le nombre d'exercice avec le premier tag (etiquette[0])
        while nbQ != nbExercices:
            for i in range(len(etiquettes)):
                etiq = etiquettes[i]
                for tag,bornes in etiq.items():
                    nbParTag[i] = random.randint(bornes[0],bornes[1])

            nbQ = sum(nbParTag)
        return nbParTag


    listeDeSujet = []
    
    while len(listeDeSujet) != nbSujets:
        

        nbParTag = nombreParTag()
        #à partir de là on sais combien d'exercices par tag on aura dans le sujet 

        sujetPret = False
        
        while not sujetPret:
            expired = False
            sujet = []

            indiceTabParTag = 0
            cpNbParTag = [x for x in nbParTag]
            #not shuffle
            while sum(cpNbParTag) != 0:#tant qu'on a pas mis tous les exercices

                TTL = TTL - 1
                if(TTL <0):
                    expired = True
                    TTL = 2000
                    nbParTag = nombreParTag()
                    break

                if(shuffle):
                    indiceTabParTag = random.randint(0,len(cpNbParTag)-1)#l'indice est choisi au hasard et si c'est 0 on recommence

                if(cpNbParTag[indiceTabParTag] == 0):

                    if(not shuffle):
                        indiceTabParTag += 1
                    continue

                else:
                    tag = list(etiquettes[indiceTabParTag].keys())[0]
                    choix = random.choice(exercices[tag])
                    if(not choix in sujet):
                        sujet.append(choix)
                        cpNbParTag[indiceTabParTag] =cpNbParTag[indiceTabParTag] -1
            

            if expired:#TTL a expiré
                continue

            if not sujet in listeDeSujet:
                listeDeSujet.append(sujet)
                sujetPret = True


    resultat.append(listeDeSujet)
    timeout_event.set()
    



class TimeoutException(Exception):
    pass

def executer_fonction_timeout(exercices,etiquettes,nbSujets,nbExercices,shuffle,timeout=3):
    resultat=[]
    timeout_event = threading.Event()
    thread = threading.Thread(target=GenereExamens, args=(exercices, etiquettes,nbSujets,nbExercices,shuffle,resultat,timeout_event))
    thread.start()
    timeout_event.wait(timeout) # la fonction doit se terminer en moins de 5 secondes
    if timeout_event.is_set():
        # la fonction s'est terminée normalement avant le timeout
        return resultat[0]
    else:
        # le timeout a été dépassé, on interrompt l'exécution de la fonction
        raise TimeoutException("La fonction a pris trop de temps à s'exécuter.")

        




@app.route('/creeControle',methods=['GET','POST'])
def creeControle():


    anonyme=(request.form.get('anonyme'))
    if(anonyme != None):
        anonyme = True
    else:
        anonyme = False

    nbExercices=int(request.form.get('nbrQuestions'))
   
    nbSujets=int(request.form.get('nbrSujets'))

    shuffle=(request.form.get('entrelace'))
    if(shuffle != None):
        shuffle = True
    else:
        shuffle = False

    etiquettes = []  #etiquette sous la bonne forme : etiquettes = [{"web":[1,2]},{"systeme":[0,6]}] par exemple
    exercices = {}

    tabTag = []
    for tag in zip(request.form.getlist("tag")):
        
        tabTag.append(tag[0])
    
    tabTag = list(set(tabTag)) #supprime les doublons

    for e in tabTag:#met etiquettes sous le bon format + initialise le dictionnaire "exercices"
        tabE = []
        for x in zip(request.form.getlist(e)):
            
            tabE.append(int(x[0]))
        newTabE = []
        newTabE.append(tabE[0])
        newTabE.append(tabE[1])#pour etre sur d'avoir un tableau de 2 elements
        etiquettes.append({e:newTabE})
        exercices[e] = []

    #exercices sous la forme : exercices = {"web":[1,4,7,9,11],"systeme":[3,5,12]}

   
    with open('exercices.csv', 'r') as file:
        reader = csv.reader(file)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                c1=row[3][1:]
                c2=c1[:-1]

                c2=c2.replace("'", '')#suppression des espaces et quote
                c2 = c2.replace(" ","")
                tabEtique=c2.split(',')
                for key in exercices.keys(): #on ajoute l'exercice pour toutes les etiquettes qu'il contient
                    if(key in tabEtique):
                        exercices[key].append(row[0])


    #les tests pour savoir si la demande est possible
    nbExoDispo = 0
    ExoDispo = []
    for v in exercices.values():
        for x in v:
            if not x in ExoDispo:
                ExoDispo.append(x)
                nbExoDispo += 1



    sub_lists = list(itertools.combinations(ExoDispo, nbExercices))
    NbSujetMax = math.factorial(len(ExoDispo))   

    NbSujetPossible = NbSujetMax/math.factorial(len(ExoDispo)-int(nbExercices)) 

    print("sujets possibles",NbSujetPossible)


    with open('exercices.csv', 'r') as file:
        reader = csv.reader(file)
        tab=[]
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row=ligne  # on enlève les [ ] du tableau des tags
                r1=row[6][1:]         # on enlève les '[' et ']' pour la liste des réponses
                r2=r1[:-1]
                r2=r2.replace("'", '')  
                r3=r2.split(',')
                r4=[]
                for i in range(len(r3)):  #séparation de la question et de sa valeur (1 juste,0 faux)  question@1 et ajout dans un tableau
                    c=r3[i].split('@')
                    r4.append(c)
                tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": row[3], "type": row[4], "question": row[5], "answer": r4})



    tabEti = []
    with open("etiquettes.csv","r") as file:  #on donne le tableau des étiquettes pour que la page les affiches
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEti.append(row)


    if(nbSujets > NbSujetPossible):

        return render_template('controle.html',tabEti=tabEti,compatible1=0)
    


    
    #appel de la fonction de génératon : si l'execution depasse les 3 secondes, on abandonne

    try:
        sujetsControle= executer_fonction_timeout(exercices,etiquettes,nbSujets,nbExercices,shuffle)
        
        return render_template('affichageControle.html',ListSujet=sujetsControle,tab=tab,anonyme=anonyme)

    except TimeoutException as e:
        print("La fonction a pris trop de temps à s'exécuter.")
        

        return render_template('controle.html',tabEti=tabEti,compatible1=0)


@app.route('/addexo',methods=['GET', 'POST'])
def addexo():    
    global idQ
    tabEti=[]

    #COR

    with open("exercices.csv","a",newline='') as file:

        if request.method == "POST":
            
            typeExo = request.form.get("type")

            title = request.form.get('title')
            title.replace('"','\"') #protection on echappe les charactères dangereux
            question = request.form.get('question')
            question.replace('"','\"')

            #récupération de tous les POST reçus
            tabTag = []
            for tag in zip(request.form.getlist("tag")):
                
                tabTag.append(tag[0])
        
            if(typeExo == "open"):
                tabAnswer="no responses@0"
                
            
            else:
                tabCheck = []
                for check in zip(request.form.getlist("checkboxvalue")):
                    
                    if(check[0]=="on"):

                        tabCheck.append(check[0])

                    else:
                        tabCheck.append("off")
                    

                tabAnswer = []
                i=0
                for ans in zip(request.form.getlist("answer")):
                
                    chaine = ans[0]
                    #on formate la réponse sous le bon format : "texteReponse@valeurVérité"
                    if(tabCheck[i]=="on"):#si la réponse est cochée
                        chaine = chaine + "@1"
                    else:
                        chaine = chaine + "@0"
                    i+=1

                    tabAnswer.append(chaine)
            
            

            
            

            #avec les valeurs post reçus on remplis ce dictionnaire
            dico = {
                "id":idQ,
                "title":title,
                "username":session["username"],
                "tag":tabTag,
                "type":typeExo,
                "question":question,
                "answer":tabAnswer

            }
            idQ+=1
            
        
            fieldnames = ["id","title","username","tag","type","question","answer"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(dico)#écriture du dictionnaire dans le fichier csv
       
            if(request.form.get("modif")!="null"):#si la requette viens de mofifExo, on supprime l'ancien exercice en ajoutant le nouveau modifié
                delete(request.form.get("modif"))

        

        with open("etiquettes.csv","r") as file:  #ajout des étiquettes créés au fichier csv si elles n'existes pas déjà
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEti.append(row)
        
        with open("etiquettes.csv","a",newline='') as file:
            for etiquette in tabTag:
                if(etiquette): #AJ
                    if [etiquette] not in tabEti:
                        writers=csv.writer(file)
                        writers.writerow([etiquette])

    return redirect('/hub')

    
@app.route('/addSequence',methods=['GET','POST'])
def addSequence():
    global idS
    seq=""
    #récupération des exercices qui ont étés sélectionnés pour faire la séquence
    
    for check in zip(request.form.getlist("checkboxvalue")):
        if(check[0]!="null"):#si l'exercice est coché

            seq=seq+check[0]+";"#on stocke les exercice séparés par un point virgule sous le format d'une chaine de caractères

    seq = seq[:-1]#on enleve le dernier ";"
    
    nameSeq = request.form.get("nameSeq")

    with open("sequences.csv","a",newline='') as file:#écrire de la nouvelle séquence dans le fichier csv
            
                
        writers=csv.writer(file)
        writers.writerow([idS,nameSeq,seq])
    idS+=1



    return redirect('/hub')



@app.route('/sequences',methods=['GET', 'POST'])
def sequences():
    #on récupère les étiquettes
    with open("etiquettes.csv", 'r') as file:#pour trier les exercice dans la page de création de sequence (non implémenté)
        reader= csv.reader(file)
        tab=[]
        for ligne in reader:
            if ligne:
                tab.append(ligne)

    etiquette=[]
    for i in range(len(tab)):
        etiquette.append(tab[i][0])

    

    with open('exercices.csv',"r") as file:#on récupère les exercices
        reader= csv.reader  (file)
        tab=[]
        
        for ligne in reader:
            if(ligne):
                row=ligne  # on enlève les [ ] du tableau des tags
                r1=row[3][1:]
                r2=r1[:-1]
                r2=r2.replace("'", '')
                r3=r2.split(',')
                tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": r3, "type": row[4], "question": row[5], "answer": row[6]})

        

    if request.method == "POST":
        eti = request.form.get("etiquette")   
        return render_template("sequences.html",eti=eti,tab=tab,username=session["username"],etiquette=etiquette)
    else:
        return render_template("sequences.html",tab=tab,username=session["username"],etiquette=etiquette)  #cas de base


@app.route('/listSeq')
def seq():
    with open('sequences.csv',"r") as file:#récupération des séquences depuis le fichier csv
        reader=csv.reader(file)
        tab=[]
        for ligne in reader:
            if(ligne):
                tab.append({"id":ligne[0],"title":ligne[1]})


    return render_template('listSeq.html',tab=tab)


@app.route('/seqDel/<id>')
def seqDel(id):
    lines = []
    with open('sequences.csv', 'r') as file:#on recréé le fichier exercice sans la ligne réprésentant l'exercice à supprimer
        reader = csv.reader(file)
        for ligne in reader:
            if(ligne):
                row = [x for x in ligne]
                if(row[0]!=id):
                    lines.append(row)                

    with open('sequences.csv', 'w',newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    return redirect("/hub")


@app.route('/visu/seq/<id>')
def visuSeq(id):
    seq={}
    with open('sequences.csv','r') as file:#on remplis le dictionnaire "seq" avec les valeurs récupérés dans le fichier "sequence.csv"
        reader=csv.reader(file)
        for ligne in reader:
            if(ligne):
                row = [x for x in ligne]
                if(row[0]==id):
                    seq["title"]=row[1]
                    seq["question"]=row[2].split(";")
    
    with open('exercices.csv',"r") as file:#pon récupère également les exercices
        reader= csv.reader  (file)
        tab=[]
        
        for ligne in reader:
            if(ligne):
                row=ligne  # on enlève les [ ] du tableau des tags
                r1=row[3][1:]
                r2=r1[:-1]
                r2=r2.replace("'", '')
                r3=r2.split(',')
                tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": r3, "type": row[4], "question": row[5], "answer": row[6]})


    return render_template('visuSeq.html',id=id,seq=seq,tab=tab,username=session["username"])


@app.route('/logProf')
def logProf():
      return render_template('login.html')

@app.route('/logEtu')
def logEtu():
      return render_template('loginEtu.html')





@app.route('/modifMdp',methods=['GET', 'POST']) # modification mdp des étudiants 
def modifMdp():
    info=[]
    with open("etudiants.csv","r") as file:
            reader=csv.reader(file)
            for ligne in reader: 
                if ligne:
                    user = [x for x in ligne]
                    if user[0]==session["username"]:
                        info=user
                        break

    if request.method == "POST":
        old=request.form.get("old")
        new=request.form.get("new")

        if hashlib.md5(old.encode("utf-8")).hexdigest()==info[3]:  #on verifie que l'ancien mdp est bien égal a l'actuelle avant de la  changer 
            info[3]=hashlib.md5(new.encode("utf-8")).hexdigest()
            tab=[]
            with open("etudiants.csv","r") as file:
                reader=csv.reader(file)
                for ligne in reader:
                    if ligne:
                        user = [x for x in ligne]
                        if user[0]==session["username"]:
                            pass
                        else:
                            tab.append(user)

                tab.append(info)

            with open("etudiants.csv","w") as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(tab)
            return redirect("/hubEtu")


        else:
            return render_template("modifMdp.html",erreur=True) 
    else:
        return render_template("modifMdp.html")








@app.route('/loginProf', methods=['GET', 'POST'])
def loginProf():
   user=[]
   mdps=[]
   retour=1
   with open("comptes.csv","r") as file:        
      if request.method == "POST":
         utilisateur=request.form.get('utilisateur')
         mdp=request.form.get('mdp')
         reader=csv.reader(file)
         for ligne in reader:
            if ligne:
               row = [x for x in ligne]
               user.append(row[0])
               mdps.append(row[1])  
         for elem in range(len(user)):
            if utilisateur==user[elem]:
               #Encrypt MD5
               mdpHash = hashlib.md5(mdp.encode("utf-8")).hexdigest()

               if mdpHash==mdps[elem]:#test si le mot de passe convient
                  session["username"] = utilisateur
                  
                  #username=utilisateur
                  return redirect("/hub")
      
   retour=0
   return render_template("login.html" ,retour=retour)




@app.route('/loginEtu', methods=['GET', 'POST'])
def loginEtu():
   user=[]
   mdps=[]
   retour=1
   with open("etudiants.csv","r") as file:        
      if request.method == "POST":
         num=request.form.get('num')
         mdp=request.form.get('mdp')
         reader=csv.reader(file)
         for ligne in reader:
            if ligne:
               row = [x for x in ligne]
               user.append(row[0])
               mdps.append(row[3])  
         for elem in range(len(user)):
            if num==user[elem]:
               #Encrypt MD5
               mdpHash = hashlib.md5(mdp.encode("utf-8")).hexdigest()

               if mdpHash==mdps[elem]:#test si le mot de passe convient
                  session["username"] = num
                  
                  #username=utilisateur
                  return redirect("/hubEtu")
      
   retour=0
   return render_template("loginEtu.html" ,retour=retour)







@app.route("/logout")
def logout():
    
    session["username"] = None
    return redirect('/')

@app.route('/newcompt')
def new():
      return render_template('new.html')

@app.route('/addcompt',methods=['GET', 'POST'])
def addCompt():#création d'un nouveau compte
   user=[]
   retour=1
   with open("comptes.csv","r") as file:  
      reader=csv.reader(file)
      i=0
      for ligne in reader:
         if ligne:
            row = [x for x in ligne]
            user.append(row[0])
            i+=1
   with open("comptes.csv","a",newline='') as file:         
      if request.method == "POST":
         utilisateur=request.form.get('utilisateur')
         mdp=request.form.get('mdp')
         #Encrypt MD5
         mdpHash = hashlib.md5(mdp.encode("utf-8")).hexdigest() #stockage du mot de passe encrypté
         

         dicoCompt={
            "utilisateur":utilisateur,
            "mot de passe":mdpHash
         }
         for i in range(len(user)):
            if dicoCompt["utilisateur"]==user[i]:
               retour="0"
               return render_template("new.html" ,retour=retour)
      fieldnames = ["utilisateur","mot de passe"]
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writerow(dicoCompt)
      session["username"] = utilisateur

      return redirect("/hub")


@app.route('/exo')
def add():
    tabEti = []
    with open("etiquettes.csv","r") as file:  #on donne le tableau des étiquettes pour que la page les affiches
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEti.append(row)
    return render_template("exo.html",tabEti = tabEti)



@app.route('/addEtu')
def addEtu():
    return render_template("ajoutEtu.html")


@app.route('/addEtudiant',methods=['GET', 'POST'])  #ajout d'etus a partir d'un csv
def addEtudiant():
    if request.method == "POST":  #on a donné un fichier 
        f = request.files['fichier']  # on récupére toutes les infos du fichier 
        nom_fichier = f.filename
        chemin=os.getcwd()+"/download"   
        f.save(os.path.join(chemin,nom_fichier))
        tab=[]
        with open(os.path.join(chemin,nom_fichier),"r") as fileRecup:
            reader=csv.reader(fileRecup)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    row.append(hashlib.md5(row[0].encode("utf-8")).hexdigest())
                    tab.append(row)

        os.remove(os.path.join(chemin,nom_fichier))

        
        chemin=os.getcwd()+"\statistiques"    
        for etu in tab:   # on vérifi pour chaques étudiant dans csv données qu'il n'existe pas déjà
            nom=etu[0]+".csv"

            with open("etudiants.csv","r") as file:
                reader=csv.reader(file)
                present=False
                for ligne in reader:
                    if ligne:
                        if etu[0] in ligne:
                            present=True 
                if present==False:  #si etu non présent, on le rajoute a partir des infos données + on lui donne mot de passe encrypté qui correspond au départ a son num etu
                    fichier = open(os.path.join(chemin,nom), "w")  #on créé également un fichier stat pour cet etu
                    fichier.close()
                    with open("etudiants.csv","a") as ajout:
                        writers=csv.writer(ajout)
                        writers.writerow(etu)
    return redirect("/hub")

 
@app.route('/rejoindre',methods=['GET', 'POST'])  # rejoindre salle en direct
def rejoindre():
    if request.method == "POST":
        id=request.form.get('idSalle')
       
        with open("direct.csv", "r") as f:
            reader=csv.reader(f) 
            for ligne in reader:
                    if ligne:
                        if id in ligne:
                            return redirect("/direct/"+id)   
    return render_template("hubEtu.html",pasLa=True)


@app.route('/createRoom')
def createRoom():
    print("creation de room")
    #genere un id room aléatoire
    idRoom = str(random.randint(10000,99999))
    nomHost = session["username"]
    #Creer la room dans un fichier csv coté serveur : format = [id_room,nom_host]

  
    with open("direct.csv","a") as f:
        writers=csv.writer(f)
        writers.writerow([idRoom,nomHost,""])

    #rejoindre la room dans "direct.html"
    
    #renvoyer template avec l'id room
    return redirect("/direct/"+idRoom)



def modifJoinedFromDirect(idRoom,username):
    with open("direct.csv","r") as f:
        reader = csv.reader(f)
        allLines = []
        for ligne in reader:
            if(ligne):
                if(ligne[0]==idRoom):
                    newligne = [ligne[0],ligne[1],ligne[2]+username+";"]
                    allLines.append(newligne)
                else:
                    allLines.append(ligne)
    
    with open("direct.csv","w") as f:
        writer = csv.writer(f)
        writer.writerows(allLines)


@app.route('/direct/<idRoom>')
def direct(idRoom):
    #verifier si la salle existe
    
    #on écrit le nom de celui qui rejoint dans le fichier direct.csv
    modifJoinedFromDirect(idRoom,session["username"])

    with open("direct.csv","r") as f:
        reader = csv.reader(f)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(row[0]==idRoom): #si ça existe on rejoint la salle
                    host = row[1]

                    #envoie d'un message aux client comme quoi un nouveau joueur a rejoint
                    #dans direct.html lorsque quelqu'un rejoint la page
                    
                    joined = ligne[2].split(";")
                    

                    return render_template("direct.html",idRoom = idRoom,host = host, username = session["username"],joined = joined)

                else:
                    pass



@app.route('/stat',methods=['GET', 'POST'])   # affichage des stats d'un étu a partir de son num étudiant 
def stat():
    if request.method == "POST":  #on a donnée un num etu
        numEtu=request.form.get("numEtu")
       
        name=numEtu+".csv"
        chemin=os.getcwd()+"/statistiques"  

        tabEtu=[]
        with open("etudiants.csv","r") as file: # ouverture du fichier stat de cet etu
            reader=csv.reader(file)
            for ligne in reader:
                if ligne:
                    row = [x for x in ligne]
                    tabEtu.append(row[0])
        
        if numEtu in tabEtu:  #vérification que l'etu existe 

            tab=[]

            with open(os.path.join(chemin,name),"r") as file:
                reader=csv.reader(file)
                for ligne in reader:
                    if ligne:
                        row = [x for x in ligne]
                        tab.append(row)
            return render_template("stat.html", tab=tab)
        else:
            return render_template("stat.html", erreur="true")   # si exite pas on affiche un msg erreur




    else:
        return render_template("stat.html")





        
    

##SOCKETIO


@socketio.on('joinRoom')
def onjoin(data):

    print('received message: ' + data["idRoom"])
    join_room(data["idRoom"])

@socketio.on('newPlayer')
def newP(idRoom):
    joined = []
    with open("direct.csv","r") as f:
        reader = csv.reader(f)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(row[0]==idRoom): #si ça existe on rejoint la salle
                
                    joined = ligne[2].split(";")

    emit("actuNewPlayer",joined,to=idRoom)


@socketio.on('askQ')   #récupe du tableau de toutes les questions
def askQ(idRoom):
    with open('exercices.csv',"r") as file:
        reader= csv.reader  (file)
        tab=[]
        
        for ligne in reader:
            if(ligne):
                row=ligne  # on enlève les [ ] du tableau des tags
                r1=row[3][1:]
                r2=r1[:-1]
                r2=r2.replace("'", '')
                r3=r2.split(',')
                tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": r3, "type": row[4], "question": row[5], "answer": row[6]})
    emit("listeQ",tab,to=idRoom)

  
@socketio.on('Qid')   # recup d'une question a partir de son id
def Qid(idroom,id):
    with open('exercices.csv',"r") as file:
        reader= csv.reader  (file)
        tab=[]
        
        for ligne in reader:
            if(ligne):
                row=ligne  # on enlève les [ ] du tableau des tags
                print(int(row[0]),id)
                if(int(row[0])==int(id)):
                    
                    r1=row[3][1:]
                    r2=r1[:-1]
                    r2=r2.replace("'", '')
                    r3=r2.split(',')
                    tab.append({"id":row[0],"title": row[1], "username": row[2], "tag": r3, "type": row[4], "question": row[5], "answer": row[6]})
                    emit("questionParId",tab,to=idroom)


@socketio.on('fin')
def fin(idroom):
    emit("finDeRep",to=idroom)


@socketio.on('repQCM') # étudiant a répondu a question qcm on ajoutes stats avec addStat puis envois msg a touts les membres  de la room pour actualiser affichages 
def repQCM(idroom,selected,question):
    addStat(selected,question)
    emit("afficheResultQCM",selected,to=idroom)


@socketio.on('rep')  # étudiant a répondu a question str ou num on ajoutes stats avec addStat puis envois msg a touts les membres  de la room pour actualiser affichages 
def repQCM(idroom,selected,question):  
    addStat(selected,question)

    emit("afficheResult",selected,to=idroom)  


#COR



@socketio.on('repOuverte')
def repOuverte(idRoom,value):

    #creation d'une room juste pour l'utilisateur qui fait la requete pour renvoyer la reponse qu'à lui
    #le client va devoir faire un requette : deleteNewRoom pour supprimer cette nouvelle room
    roomRandom = str(random.randint(1,9999999999))

    join_room(roomRandom)

    #ALGO DE CORRECTEUR ORTHOGRAPHIQUE

    combinaison = False #si c'est une phrase avec plusieurs mot ayan tla même distance d'édition
    phrase = False

    v = value.strip()
    v = v.split(" ")
    
    tabVal=[""]
    #on applique le correcteur sur tous les mots de la phrase

  
    if(len(v)>1):#est ce que c'est une phrase ?
        phrase = True
  
    for i in range(len(v)):#pour chaque mot de la phrase
        
        word = v[i]
        dictionary = load_dictionary("static/dicoProg.txt")
        closest_words = correct_spelling(word, dictionary)
        
        if closest_words is None:
            
           
            for i in range(len(tabVal)):
                tabVal[i] = tabVal[i] + word + " "
        else:
            
            if(len(closest_words)>1):#plusieurs mots avec la meme distance
                
                # if(phrase):
                newTabVal=[]
                combinaison = True
                for i in range(len(tabVal)):
                    for j in range(len(closest_words)):
                        newTabVal.append(tabVal[i]+closest_words[j]+" ")
                        print(newTabVal)
                tabVal=newTabVal

            else:#une seule possibilité
                for i in range(len(tabVal)):
                    tabVal[i] = tabVal[i] + closest_words[0] + " "
  
    if(not(combinaison)):
        val = tabVal[0].strip()
        emit("retourOuverte",[val,roomRandom],to=roomRandom)
    else:
        for i in range(len(tabVal)):
            tabVal[i] = tabVal[i].strip()
        emit("multiPos",[tabVal,roomRandom],to=roomRandom)


def addStat(selected,question):  # ajout des statitiques pour étudiant, selected = réponses données a la question , question = tableau contenant toutes les infos de la question répondu 

    chemin=os.getcwd()+"/statistiques"
    nom=session["username"]+".csv"  
    tab=[]

    with open(os.path.join(chemin,nom),"r") as fileRecup: # ouverture du fichier des statitiques de l'étudiant
        reader=csv.reader(fileRecup)  
        for ligne in reader:  # ajout dans tab stats de chaques questions différente de celle a laquelle etu vient de répondre
            if ligne:
                row = [x for x in ligne]
                if(row[0]==question[0]['id']):
                    pass           
                else:
                    tab.append(row)   

    
    #mise en forme de la chaine que l'on va rajouté dans le CSV des stats pour la question répondue 
    rajout=[]
    rajout.append(question[0]['id'])
    rajout.append(question[0]['title'])
    rajout.append(question[0]['type'])
    rajout.append(question[0]['question'])  


    if question[0]['type']=="qcm":  #cas QCM 

        reponseStr=question[0]['answer']  # récupérations de toutes les réponses possible sous forme de str
        
        
        rep=reponseStr.split(',')  # traitement de la chaine pour obtenir tableau
        reponses=[]
        for elem in rep:
            reponses.append(elem.replace("'","").replace("[","").replace("]","").strip())
        tabBonneRep=[]

        for elem in reponses:
            tabBonneRep.append(elem.split("@"))

        pareil="vrai"  #on vérifie pour chaques réponses données si celle ci est identique a la bonne réponses , si non  pareil=faux 
        for i in range(len(tabBonneRep)):
           
            if int(tabBonneRep[i][1]) != int(selected[i][1]):
                pareil="faux"

        
        rajout.append(pareil)   # ajout a la fin de rajout si  bonne réponse ou non
        tab.append(rajout)


        with open(os.path.join(chemin,nom),"w") as file:  # réécriture des stat de l'étudiant a partir du tableau tab contenant toutes les stats 
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(tab)  

    else:  #cas str ou num similaire a qcm sauf qu'on vérifie qu'une réponse


        reponseStr=question[0]['answer']
        rep=reponseStr.replace('[','').replace(']','').replace("'","")
        rep=rep.split('@')
        pareil="vrai"
        if str(selected) != str(rep[0]):
                pareil="faux"


        rajout.append(pareil)
        tab.append(rajout)


        with open(os.path.join(chemin,nom),"w") as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(tab)




    
@socketio.on('closeRoom')
def closeRoom(idRoom):

    #supprimer room du fichier pour qu'on puisse plus rejoindre
    with open("direct.csv","r") as f:
        reader = csv.reader(f)
        allLines = []
        for ligne in reader:
            if(ligne):
                if not(ligne[0]==idRoom):
                    allLines.append(ligne)
    with open("direct.csv","w") as f:
        writer = csv.writer(f)
        writer.writerows(allLines)

    # #envoyer message de depart à tous les joueurs
    # emit("startingGame",to=idRoom)


@socketio.on('AskLstSequence')
def askSequence(idRoom):

    with open("sequences.csv","r") as f:
        allSeq = []
        reader = csv.reader(f)
        for ligne in reader:
            if(ligne):
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                allSeq.append(row)
    
    emit("showSeq",allSeq,to=idRoom)

@socketio.on('actuRep')
def actuRep(rep,idRoom):
    emit("afficheRep",rep,to=idRoom)


@socketio.on('askExoInSeq')
def askExoInSeq(idSeq,idRoom):

    with open("sequences.csv","r") as f:
        tabExo=[]
        reader = csv.reader(f)
        for ligne in reader:
            if(ligne):
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(row[0] == idSeq):
                    tabExo = row[2].split(";")
    
    emit("askExoInSeqAnswer",tabExo,to=idRoom)


@socketio.on('deleteRoom')
def deleteRoom(idRoom):
    emit("leaveRoom",to=idRoom)


@socketio.on('leaveRoom')
def leaveRoom(idRoom,idClient):
    role = 1 #1 = etudiant, 0 = professeur

    roomRandom = str(random.randint(1,9999999999))
    
    leave_room(idRoom)
    join_room(roomRandom)

    with open("comptes.csv","r") as f:
        reader = csv.reader(f)
        for ligne in reader:
            if(ligne):#Si la ligne existe
                row = [x for x in ligne]#on créé une liste contenant les valeurs de la ligne
                if(row[0] == idClient): #c'est un professeur
                    role = 0
                    

   
    emit("leaveRoomRole",[role,roomRandom],to=roomRandom)


@socketio.on('deleteNewRoom')
def deleteRoomNew(idRoom):
    print("la nnouvelle room :"+idRoom)
    leave_room(idRoom)



#COR


def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    d = np.zeros((m+1, n+1), dtype=int)
    for i in range(m+1):
        d[i][0] = i
    for j in range(n+1):
        d[0][j] = j
    for j in range(1, n+1):
        for i in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j] + 1,  # suppression
                              d[i][j-1] + 1,  # insertion
                              d[i-1][j-1] + 1)  # substitution
    return d[m][n]

def load_dictionary(file_path):
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()

def correct_spelling(word, dictionary):
    tabMotMin = [word]
    min_distance = float("inf")
    for dict_word in dictionary:
        distance = levenshtein_distance(word, dict_word)
        if distance == min_distance:
            tabMotMin = tabMotMin + [dict_word]

        if distance < min_distance:
            min_distance = distance
            tabMotMin = [dict_word]
    
    return tabMotMin


if __name__ == '__main__':
   #app.run(port=5000,debug=True)

    #CHANGEMENT

   socketio.run(app,port=5000,debug=True)


