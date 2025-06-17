from machine import Pin
import time

pinPul = Pin(12,Pin.OUT)
pinDir = Pin(4,Pin.OUT)
subdivision = 800

#tableau des angles possibles en fonction de la subdivision
valeurs = {i+(j/10) for i in range(360) for j in range(9) if (abs((i+(j/10)) * subdivision / 360  - int((i+(j/10)) * subdivision / 360 )) <= 0.00001)}

pinPul.value(0)  #on initialise les dir et pul à 0
pinDir.value(0)

def tourner1CranHoraire():
    pinDir.value(1) #on apporte une impulsion elec à dir et pul
    pinPul.value(1)
    time.sleep_ms(1) # 1ms correspond au temps nécéssaire pour faire avancer le moteur d'un cran
    
    pinPul.value(0)
    pinDir.value(0)
    
    return

def tourner1CranAntiHoraire():
    pinPul.value(1) #on apporte une impulsion elec à pul
    time.sleep_ms(1) # 1ms correspond au temps nécéssaire pour faire avancer le moteur d'un cran
    
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
        
        if (angle in valeurs) : #on vérifie que l'angle est dans l'ensemble valeurs
            tournerCranHoraire(n-1)
            print("Rotation effectuee")
            print(angle)
            return
        print("angle non atteignable")
        
    elif (angle < 0): #angle anti-horaire
        n = -angle * subdivision / 360 
        
        if (-angle in valeurs) :
            tournerCranAntiHoraire(n-1)
            print("Rotation effectuee")
            print(-angle)
            return
        print("angle non atteignable")
    return



   