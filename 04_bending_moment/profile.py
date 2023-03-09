from _operator import truediv
import json
from pprint import pprint


def profiles(bending_moment, axial_force, steel_grade, HEB, IPE, RO, HEA):
    steel_grade = steel_grade
    M_Ed = bending_moment  # kNm
    N_Ed = axial_force  # kN
    fy = int(steel_grade.split(sep="S")[1])
    print(steel_grade, fy)
    # fd = fy / 1.15
    min_value = 70

    profile = []
    if HEB:
        with open("HEB.json") as f:
            HEB = json.load(f)
        profile += HEB
    if IPE:
        with open("IPE.json") as f:
            IPE = json.load(f)
        profile += IPE

    if RO:
        with open("RO.json") as f:
            RO = json.load(f)
        profile += RO

    if HEA:
        with open("HEA.json") as f:
            HEA = json.load(f)
        profile += HEA

    M_Rd = [(profile[_].get('Wx') * fy / 1000) for _ in range(0, len(profile))]
    N_Rd = [round(profile[_].get('A') * fy / 10) for _ in range(0, len(profile))]
    M_Ed_list = [M_Ed for _ in range(0, len(profile))]
    N_Ed_list = [N_Ed for _ in range(0, len(profile))]

    # division of lists
    # using map()

    ULS_M_Rd = list(map(truediv, M_Ed_list, M_Rd))
    ULS_N_Rd = list(map(truediv, N_Ed_list, N_Rd))

    # sum using zip
    ULS = [(a + b) * 100 for a, b in zip(ULS_M_Rd, ULS_N_Rd)]  # units [%]

    wynik = {}

    # wynik = {
    #     "HEB200": 97,
    #     "HEB300": 95 }

    for x in ULS:
        if (x < 100) and (x > min_value):
            wynik[profile[ULS.index(x)].get("name")] = f'{round(x)} %'
    return wynik

#
# p = profiles(300, 100, 'S355', True, True, True, True)
# pprint(p)
