from pprint import pprint

from profile import profiles


# Data
print('insert bending moment') 
bending_moment = int(input())  # kNm
print('insert axial force') 
axial_force = int(input())  # kN
print('insert steel grade: S235 or S235') 
steel = input()  # 'S235' or 'S355'

HEB = True  # True or False
HEA = True  # True or False
IPE = True  # True or False
RO = True  # True or False


p = profiles(axial_force=axial_force, bending_moment=bending_moment, steel_grade=steel, HEB=HEB, HEA=HEA, IPE=IPE, RO=RO)
pprint(p)


