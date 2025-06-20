from machine import Pin
import time

pinPul = Pin(12,Pin.OUT)
pinDir = Pin(4,Pin.OUT)
subdivision = 6400  #nombre de subdivision dans la rotation du moteur, donnée variable à changer manuellement
delais = 10 #delais de temps entre chaque cran quand le moteur tourne, à modifier en fonction de la subdivision pour éviter que ça soit trop lent ou trop rapide

pinPul.value(0)  #on initialise les dir et pul à 0
pinDir.value(0)
    

def verifAngle(angle): #fonction qui vérifie que l'angle est valide, on vérifie que c'est un multiple de la subdivision
    for i in range(subdivision):
        if (abs(i*(360/subdivision) - abs(angle)) <= 0.0001):
            return True
    return False

def listeAngle(): #liste des angles valides
    for i in range(subdivision+1):
        print(i*(360/subdivision))
    return


def tourner1CranHoraire():
    pinDir.value(1) #on apporte une impulsion elec à dir et pul
    pinPul.value(1)
    time.sleep_ms(delais) # 1ms correspond au temps nécéssaire pour faire avancer le moteur d'un cran, ici on choisi le temps entre chaque avancement d'un cran du moteur
    
    pinPul.value(0)
    pinDir.value(0)
    
    return

def tourner1CranAntiHoraire():
    pinPul.value(1) #on apporte une impulsion elec à pul
    time.sleep_ms(delais) # 1ms correspond au temps nécéssaire pour faire avancer le moteur d'un cran, ici on choisi le temps entre chaque avancement d'un cran du moteur
    
    pinPul.value(0)
    pinDir.value(0)
    return

def tournerCranHoraire(cran): #permet de tourner du nombre de cran qu'on veut en fct de la subdivision
    for i in range(cran):
        tourner1CranHoraire()
    return

def tournerCranAntiHoraire(cran): #permet de tourner du nombre de cran qu'on veut en fct de la subdivision
    for i in range(cran):
        tourner1CranAntiHoraire()
    return

def tournerAngle(angle):
    n = 0
    if (angle > 0): #angle horaire
        n = angle * subdivision / 360 #produit en croix pour trouver le nombre de subdivision pour l'angle voulu
        
        if (verifAngle(angle)) : #on vérifie que l'angle est dans l'ensemble valeurs
            tournerCranHoraire(n-1)
            print("Rotation effectuee")
            print(angle)
            return
        print("angle non atteignable")
        
    elif (angle < 0): #angle anti-horaire
        n = -angle * subdivision / 360 
        
        if (verifAngle(-angle)) :
            tournerCranAntiHoraire(n-1)
            print("Rotation effectuee")
            print(-angle)
            return
        print("angle non atteignable")
    return

def menu(): #menu pour faciliter l'utulisation du moteur
    angleActuel = 0
    reponse = 0
    
    while(reponse != 7):
        
        print("L'angle actuel vaut : " + str(angleActuel)+"\n")
        print("1 : Avancer d'un cran horaire \n")
        print("2 : Avancer d'un cran anti-horaire \n")
        print("3 : Avancer d'un angle précis \n")
        print("4 : Avancer d'un certain nombre de crans horaires \n")
        print("5 : Avancer d'un certain nombre de crans anti-horaires \n")
        print("6 : Remettre le moteur à angle 0 \n")
        print("7 : Quitter \n")
        
        reponse = int(input("Choix : "))
        
        if (reponse == 1):
            tourner1CranHoraire()
            angleActuel = angleActuel + (360/subdivision)
            
        elif (reponse == 2):
            tourner1CranAntiHoraire()
            angleActuel = angleActuel - (360/subdivision)
            
        elif (reponse == 3):
            print("Quel angle ? \n ")
            langle = float(input("Angle : "))
            if (verifAngle(langle)):
                angleActuel = angleActuel + langle
            tournerAngle(langle)
            
        elif (reponse == 4):
            print("Combien de crans horaire ? \n ")
            lcran = int(input("Nombre de crans : "))
            tournerCranHoraire(lcran)
            angleActuel = angleActuel + (360/subdivision) * lcran
            
        elif (reponse == 5):
            print("Combien de crans anti-horaire ? \n ")
            lcran = int(input("Nombre de crans : "))
            tournerCranHoraire(lcran)
            angleActuel = angleActuel + (360/subdivision) * lcran
        
        elif (reponse == 6):
            if (angleActuel != 0):
                tournerAngle(-angleActuel)
            angleActuel = 0
    
    
    return

menu()

#Rajouter le nombre de cran qu'on a fait deouis l'angle 0 affiché dans le menu en fct de la subdivision
#Coder une fct pas à pas
    
   