import sys 

stdoutOrigin=sys.stdout 
sys.stdout = open("log.txt", "w")

#!/usr/bin/env python
# coding: utf-8

# ## BIBLIOTEKI

# In[1]:


#import win32com.client
import numpy as np
#sp.init_printing(use_latex="mathjax")
import math as mt
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import itertools
from matplotlib.path import Path
import matplotlib.patches as patches

import array
import pyzwcad as zw
acad = zw.ZwCAD()
acad.prompt("PYTHON PRZEJMUJE ZWCADA! ")

from math import sqrt

from IPython.display import display

#app = win32com.client.GetActiveObject("ZWCAD.Application")
#ms = app.ActiveDocument
from statistics import mean


# ### DANE GEOMETRYCZNE

# In[2]:


D = 3 #m Głębokość posadowienia
r = 1.3 #m Głębokość działania sił poziomych
h = 1.7 #m Wysokość fundamentu
ex = 0 #m mimośród siły pionowej wzdłuż osi x
ey = 0 #m mimośród siły pionowej wzdłuż osi y

gamma_bet = 25 #kN/m3
gamma_zasypki_śr = 19 #kN/m3
q_tech_posadzki = 30 #kN/m2
Współ_część_konstrukcji = 1.35
Współ_część_posadzka = 1.5
Współ_część_gruntu = 1.35

## List1
Name = ['Głębokość posadowienia', 'Głębokość działania sił poziomych',
'Wysokość fundamentu', 'mimośród siły pionowej wzdłuż osi x',
'mimośród siły pionowej wzdłuż osi y', 'Ciężar betonu', 'uśredniony ciężar zasypki',
'obciążenie tech. posadzki']
   
# List2
zmienna = [D, r, h, ex, ey, gamma_bet, gamma_zasypki_śr, q_tech_posadzki]
   
# get the list of tuples from two lists.
# and merge them by using zip().
list_of_tuples = list(zip(Name, zmienna))

dane = pd.DataFrame(list_of_tuples,
                  columns = ['Opis', 'Wartość'])


# ## Pobieranie danych z autocad'a

# In[3]:


index = 0
lista = []
#Pobranie współrzędnych
for circle in acad.iter_objects('circle'):
    lista +=circle.center
    index +=1
#Zaokrąglenie do 3 miejsca po przecinku                
lista = [round(num, 3) for num in lista]
# Wyrzucenie współrzędnych zetowych
del lista[2::3]

#lista po X
xs = lista[::2]
#lista po Y
ys = lista[1::2]
#liczba pali
n=len(lista)/2

'''
points_double = array.array("d", lista)
acad.model.AddLightWeightPolyline(points_double)
'''
lista2=[]
for polyline in acad.iter_objects('polyline'):
    if polyline.ObjectName == "AcDbPolyline":
        lista2+=polyline.coordinates

#zamknięta polilinia
#lista2.append(lista2[0])
#lista2.append(lista2[1])
#print(lista2)

#pole powierzchni fundementu
for polyline in acad.iter_objects('polyline'):
    if polyline.ObjectName == "AcDbPolyline":
        A=polyline.Area
print('Współrzędne pali:')
print('')
print(F'X: {xs}\nY: {ys}')
print('')

# ## Rysunek pali - definicja

# In[4]:


def rysunek(xs, ys):   
    

    area = 200  # rozmiar


    '''

    # fundament
    plt.gca().add_patch(Rectangle((-(L/2),-(B/2)),L,B,linewidth=3,edgecolor='b',facecolor='none'))

    
    ax = plt.gca()
    ax.set_xlim([-0.5*L-1,0.5*L+1 ])
    ax.set_ylim([-0.5*B-1, 0.5*B+1])
    

    '''
    for i_x, i_y in zip(xs, ys):
        i_x= np.round(i_x, decimals=2)
        i_y= np.round(i_y, decimals=2)
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
        
  

    plt.title("ROZMIESZCZENIA PALI")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    
   
    plt.scatter(xs, ys, s=area, alpha=0.5, color='red')

    #plt.show()
    plt.savefig('foo.png')
    return 
#rysunek(xs, ys)


# ## SIŁY 

# In[9]:


df = pd.read_excel (r'forces.xlsx', sheet_name='1')
#display(df.head())
V = df['Rz']
Hx= df['Rx'] #kN
Hy= df['Ry'] #kN
Mx= df['Mx'] #kN
My= df['My'] #kN
n_komb = len(df)
print('')
print(f'Liczba kombinacji: {n_komb}')
print('')

# In[10]:


#Wx = L*B**2/6
#Wy = B*L**2/6

#print(F"Pole powierzchni: {A} m2")
Obj_fund = A * h
#print(F"Objętość fundamentu: {Obj_fund} m3")
Obj_gruntu_posadzki = A*(D-h)
#print(F'Objętość gruntu: {Obj_gruntu_posadzki} m3')
R =D-r #m ramie sił 
Obc_użyt_skup = A * q_tech_posadzki * Współ_część_posadzka
#print(f'Obciązenie użytkowe skupione: {Obc_użyt_skup} kN')
G1 = gamma_bet*Obj_fund*Współ_część_konstrukcji
#print(f'Ciężar stopy G1: {G1} kN')
G2=gamma_zasypki_śr*Obj_gruntu_posadzki * Współ_część_gruntu
#print(f'Ciężar obsypki G2: {G2} kN')
OBC_dod = round(Obc_użyt_skup + G1 + G2)
#print(F'Obciążenie dodatkowe pochodzące d stopy, gruntu i obciążenia: {OBC_dod} kN')
Mxey = V*ey
Myex = V*ex
MyHx = Hx * R
MxHy = -Hy * R
#print(Mx,My)
Mx = Mxey+MxHy+Mx
My = Myex+MyHx+My
#print(f'moment Mx: {Mx}, moment My: {My}')

## List1
Name = ['Pole powierzchni','Objętość fundamentu','Objętość gruntu',
        'Obciązenie użytkowe skupione','Ciężar stopy G1','Obciążenie dodatkowe']
   
# List2
zmienna = [Obj_fund,Obj_gruntu_posadzki,R,G1,G2,OBC_dod]
   
# get the list of tuples from two lists.
# and merge them by using zip().
list_of_tuples = list(zip(Name, zmienna))

dane2 = pd.DataFrame(list_of_tuples,
                  columns = ['Opis', 'Wartość'])


# In[22]:


def Siły(V,Hx,Hy,Mx,My):
    #xs = np.array([1,1,-1,-1])
    #ys=np.array([1,-1,1,-1])
    #k=np.array([1,1,1,1])

    
    #środek ciężkości
    x0 = mean(xs)
    y0 = mean(ys)
    x0=xs-x0
    y0=ys-y0
    
    x2 = x0**2
    y2 = y0**2
    xy = x0*y0
    V_n = (OBC_dod+V)/n
    
    
    Ix0 = sum(y2)
    Iy0 = sum(x2)
    I_xy = sum(xy)
    N_Mx = -(My*I_xy+Mx*Iy0)/(Ix0*Iy0-I_xy**2)*y0
    N_My = (Mx*I_xy+My*Ix0)/(Ix0*Iy0-I_xy**2)*x0
    Ni=list(V_n+N_Mx+N_My)
    df4=pd.DataFrame()
    df4['x']=xs
    df = pd.DataFrame(list(zip(xs,ys,N_Mx,N_My,Ni,x0,y0,x2,y2,xy)),
               columns =['x','y','N_Mx','N_My','Ni','x0','y0','x2','y2','xy'])
    df.round(2)
    #display(df)
    return Ni
    return df
xs = np.array(xs)
ys = np.array(ys)
H_śr =round(max(((Hx**2+Hy**2)**0.5)/n),1)


# In[23]:



display(df)
print('')
print(f'Ilość pali: {n}')
print('')
display(dane)
print('')
display(dane2)

rysunek(xs, ys)
wyniki=[]
for i in range(0,n_komb):
    wyniki.append(Siły(V[i],Hx[i],Hy[i],Mx[i],My[i]))
wyniki = pd.DataFrame(wyniki)
wyniki.index.name = 'Numer kombinacji'
print('')
display(round(wyniki,2))
print(F'Max siła pionowa: {wyniki.max()} kN\nMin siła pionowa: {min(wyniki)} kN\nŚrednia siła pozioma: {H_śr} kN')

sys.stdout.close()
sys.stdout=stdoutOrigin
# %%
