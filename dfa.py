import time

def citire_fisier(nume_fisier):
    try:
        f=open(nume_fisier,'r')
        dictionar={}
        for linie in f.readlines():
            linie = linie.strip() #in cazul in care am spatii in fata si in spate le scoate
            if ('#' not in linie) and (linie != ''): # verific daca nu cumva linia respectiva e comentariu
                if '[' and ']' in linie: #daca incepe si se termina cu '[]' atunci este cheie
                    dictionar[linie] = set() #declar un dictionar[linie] ca fiind un set pentru a putea face reuniuni si intesectii
                    if linie == '[Actiuni]' or linie == '[Stari]':  #caz special cand linia este Actiune sau Stari
                        dictionar[linie] = {} #dictionar de actiuni(o sa foloseasca mai incolo pentru a face dictionar in dictionar)
                    key = linie #salvez linia(care este sigur cheie) intr-o variabila pentru ca in loop sa pot sa am o referinta la baza
                else:
                    if key == '[Stari]': #cheia mea fiind stari o sa am mai departe toate starile posibile si proprietatiile lor
                        linie = linie.split(',')   #fac o lista in care o sa apara [qx, F/S , F/S] nu mereu o sa fie asa
                        if len(linie) == 1: #cazul in care starea mea nu e nici initiala nici finala
                            linie.append('T') # adaug de la mine identificatorul T(stare de tranzitie)
                        if linie[1] not in dictionar[key]: #daca in dictionarul de stari nu a fost initializata pana acum o stare de F/S/T atunci asta o sa fac
                            dictionar[key][linie[1]] = {linie[0]} #adaug in dictionar cheia noua linie[1] care poate sa fie S/F/T si valoare linie[0] (qx) forma key:value
                        else: #in cazul in care deja exista cheia respectiva o sa fac o reuniune(pentru a adauga noua stare in dictionar)[un fel de append, dar nu accepta dubluri]
                            dictionar[key][linie[1]] = dictionar[key][linie[1]].union({linie[0]}) 

                        try: #un try except pentru cazul particular daca exista o stare de forma [qx,S,F] pentru a o adauga in ambele sub-dictionare
                            if linie[2] not in dictionar[key]:
                                dictionar[key][linie[2]] = {linie[0]}
                            else:
                                dictionar[key][linie[2]] = dictionar[key][linie[2]].union({linie[0]})                            
                        except: #IndexError, asta e singurul lucru pe care pot sa il primesc
                            pass

                    elif key == '[Actiuni]':
                        linie = linie.split(',')
                        #o daca ce am transformat linie intr-o lista o sa incep sa lucrez cu ea
                        if (linie[1],linie[0]) not in dictionar[key]:  #daca cheia nu exista in dictionar o adaug dupa forma de mai jos
                            dictionar[key][(linie[1],linie[0])] = linie[2] #cheia este un tuplu(starea_curenta,caracter): starea_urmatoare
                            #Functia  f:Q x E -> Q, f(a,q_x) = q_y 
                         #nu exista un else pentru ca stim ca e un DFA

                    elif linie not in dictionar[key]: #ultimul caz mare in care key nu este nici [Stare] si nici [Actiuni] o sa se comporte normal is o sa o adauge.
                           dictionar[key]= dictionar[key].union({linie}) #dictionar[key] este un set() pentru a putea executa opereatie de reuniune
        
                    
        return dictionar
    except FileNotFoundError: #exceptia cand nu gaseste fisierul o sa returneze False
        return False
    
def check_state(dictionar): #functia de verificare a starilor
    if len(dictionar['[Stari]']['S']) == 0 or len(dictionar['[Stari]']['F']) == 0 or len(dictionar['[Stari]']['S']) > 1: 
        #un DFA este corect definit daca acesta are o stare de start si una sau mai multe stari finale
        return False 
    return True

def check_sigma(dictionar):
    if dictionar['[Alfabet]'] == {}:
        return False
    return True

def check_string(string,dictionar):
    string = [*string]
    for character in string:
        if character not in dictionar['[Alfabet]']:
            return False
    return True


def dfa_emulator(string,dictionar):
    start_state = next(iter(dictionar['[Stari]']['S'])) #iau primul element din set(), cu ajutoarul iteratorului care ma ajuta sa traversez tot set-ul.
    #returneaza un element, by default primul. Pot sa folosesc si next(iter(),i) unde i este pozitia.  
    for character in string: #iau caracter cu caracter din string 
       start_state = dictionar['[Actiuni]'].get((character,start_state))
       if start_state == None: #in cazul in care am un caracter care e in alfabet, dar nu face nimic in tranzitie cu starea curenta
           return False 
       #comada get cauta cheia din dictionar si returneaza valoarea
    #elementul din este este cel din dictionarul ['[Actiuni]'] si caut in el cheia care este un tuplu de forma (caracter,stare curenta):stare viitaore


    return dictionar['[Stari]']['F'].issuperset({start_state}) #returnez daca starea finala e submultime a lui F.



#main
dictionary = citire_fisier("catalin.txt")
string = "000"
stimp=time.time()
#print(dictionary)
for i in range(0,100000):
    if check_sigma(dictionary):
        if check_string(string,dictionary):    
            if dfa_emulator(string,dictionary):
                #print("Succes")
                pass
            else:
                #print("Fail")
                pass
        else:
            #print("String error!")
            pass
    else:
        #print("Alphabet error!")
        pass

print("---",(time.time()-stimp),"secunde ---")