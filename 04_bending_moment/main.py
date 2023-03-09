from pprint import pprint

from profile import profiles


# Data

bending_moment = 200  # kNm
axial_force = 50  # kN
steel = 'S235'  # 'S235' or 'S355'

HEB = True  # True or False
HEA = True  # True or False
IPE = True  # True or False
RO = True  # True or False


p = profiles(axial_force=axial_force, bending_moment=bending_moment, steel_grade=steel, HEB=HEB, HEA=HEA, IPE=IPE, RO=RO)
pprint(p)


