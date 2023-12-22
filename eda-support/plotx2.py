import glob
import re
import os
import math
import numpy as np
import matplotlib.pyplot as plt

#----------------------------#

        # coordi. extract ftn # - collects n-th atom xyz data

#XEDA 2.0
def cef(n):   # coord_extract_ftn
    with open('path.txt', 'r') as p:
        line = p.readline()
        path_str = line.split()

    coord_series_str = []

    for name in path_str:
        with open(f'output/{name}.log', 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith('$GEO'):  
                    coord = lines[i+n].strip().split()[1:]
                    break
            globals()[f'coord_{name}'] = coord
        coord_series_str.append(globals()[f'coord_{name}'])

    for coord_name in coord_series_str:
        for j in range(len(coord_name)):
            coord_name[j] = float(coord_name[j])

    coord_series = coord_series_str

    return coord_series

#XEDA 1.0
#def cef(n):   # coord_extract_ftn
#    with open('path.txt', 'r') as p:
#        line = p.readline()
#        path_str = line.split()
#
#    coord_series_str = []
#
#    for name in path_str:
#        with open(f'output/{name}.log', 'r') as file:
#            lines = file.readlines()
#            for i, line in enumerate(lines):
#                if line.startswith(' INPUT CARD> $data') or line.startswith(' INPUT CARD> $DATA'):
#                    coord = lines[i+n+2].strip().split()[3:]
#                    break
#            globals()[f'coord_{name}'] = coord
#        coord_series_str.append(globals()[f'coord_{name}'])
#
#    for coord_name in coord_series_str:
#        for j in range(len(coord_name)):
#            coord_name[j] = float(coord_name[j])
#
#    coord_series = coord_series_str
#
#    return coord_series




#----------------------------#

        # distance ftn #

def distance(atom1_coord, atom2_coord):
    x1, y1, z1 = atom1_coord
    x2, y2, z2 = atom2_coord
    
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance


def dis_axis(atom1_idx, atom2_idx):
    a1cs = cef(atom1_idx) #atom1_coord_series
    a2cs = cef(atom2_idx) #atom2_coord_series

    two_atoms_dis_series = []
    
    for i, name in enumerate(path_str):
        globals()[f'two_atoms_dis_{name}'] = distance(a1cs[i], a2cs[i])
        two_atoms_dis_series.append(globals()[f'two_atoms_dis_{name}'])
    return two_atoms_dis_series

#----------------------------#

        # angle ftn #

def angle(atom1_coord, atom2_coord, atom3_coord): 
    vector1 = np.array(atom1_coord) - np.array(atom2_coord)
    vector3 = np.array(atom3_coord) - np.array(atom2_coord)

    dot_product = np.dot(vector1, vector3)
    magnitude1 = np.linalg.norm(vector1)
    magnitude3 = np.linalg.norm(vector3)

    angle_radians = np.arccos(dot_product / (magnitude1 * magnitude3))
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees


def ang_axis(atom1_idx, catom_idx, atom2_idx):
    a1cs = cef(atom1_idx)
    a2cs = cef(atom2_idx)
    cacs = cef(catom_idx)

    atoms_angle_series = []

    for i, name in enumerate(path_str):
        globals()[f'atoms_angle_series_{name}'] = angle(a1cs[i],cacs[i], a2cs[i])
        atoms_angle_series.append(globals()[f'atoms_angle_series_{name}'])

    return atoms_angle_series

#----------------------------#

        # dihedral ftn #

def dihedral_angle(atom1, atom2, atom3, atom4):
    b1 = np.array(atom2) - np.array(atom1)
    b2 = np.array(atom3) - np.array(atom2)
    b3 = np.array(atom4) - np.array(atom3)

    v1 = np.cross(b1, b2)
    v2 = np.cross(b2, b3)

    angle = np.arctan2(np.linalg.norm(np.cross(v1, v2)), np.dot(v1, v2))
    angle_degrees = np.degrees(angle)

    if angle_degrees < 0:
        angle_degrees += 360.0

    return angle_degrees


def dihd_axis(atom1_idx, catom1_idx, catom2_idx, atom2_idx):
    a1cs = cef(atom1_idx)
    c1cs = cef(catom1_idx)
    c2cs = cef(catom2_idx)
    a2cs = cef(atom2_idx)

    dihedral_angle_series = []

    for i, name in enumerate(path_str):
        globals()[f'dihedral_angle_series_{name}'] = dihedral_angle(a1cs[i],c1cs[i],c2cs[i], a2cs[i])
        dihedral_angle_series.append(globals()[f'dihedral_angle_series_{name}'])

    return dihedral_angle_series

#----------------------------#

        # calculate relative energy #

def rel(lst, n):
    return [x - lst[n] for x in lst]


#----------------------------#



        # input checker #

print("")
directory_log_list = glob.glob('output/*.log')
log_name_list = [os.path.basename(file) for file in directory_log_list]
directory_txt_list = glob.glob('*.txt')


if 'path.txt' in directory_txt_list:
    print("Your path.txt file : ")
else:
    print("There are no path.txt file in this directory.")

with open('path.txt', 'r') as p:
    path_line = p.readline()
    path_str = path_line.split()
    path = [float(x) for x in path_str]
print(path)

print("")
print("Your output *.log file list :")
for item in log_name_list:
    print(item)

#----------------------------#


        # collects coordi data for each geometry #

#XEDA 1.0
#for var in path_str:
#    with open(f'output/{var}.log') as f:
#        geometry_str = ''
#        for line in f:
#            if re.search('\\$data|\\$DATA', line):
#                geometry_str = ''
#                break
#        for line in f:
#            if re.search('\\$end|\\$END', line):
#                geometry_str = geometry_str.replace('INPUT CARD>', '')
#                break
#            geometry_str += line
#    str_lines = geometry_str.split('\n')
#    str_lines = str_lines[2:]
#    modified_lines = ['    '.join(line.split()[0:1] + line.split()[2:]) for line in str_lines]
#    geometry_str = '\n'.join(modified_lines)
#    geometry_list = [[float(coord) for coord in line.split()[1:]] for line in geometry_str.strip().split('\n')]
#    globals()[f'mol_geo_{var}'] = geometry_list



# XEDA 2.0
for var in path_str:
    with open(f'output/{var}.log', 'r') as file:
        geometry_str = ""
        lines = file.readlines()
        capture = False

        for line in lines:
            if line.startswith('$GEO'): 
                capture = True
                continue

            if capture:
                if line.startswith('$END'): 
                    break

                geometry_str += line
        geometry_list = [[float(coord) for coord in line.split()[1:]] for line in geometry_str.strip().split('\n')]
        globals()[f'mol_geo_{var}'] = geometry_list




        # atoms list #

# XEDA 1.0
#first_geo_idx = path_str[0]
#with open(f'output/{first_geo_idx}.log', 'r') as f:
#    f_geometry_str = ''
#    for line in f:
#        if re.search('\\$data|\\$DATA', line):
#            f_geometry_str = ''
#            break
#    for line in f:
#        if re.search('\\$end|\\$END', line):
#            f_geometry_str = f_geometry_str.replace('INPUT CARD>', '')
#            break
#        f_geometry_str += line
#str_lines = f_geometry_str.split('\n')
#str_lines = str_lines[2:]
#modified_lines = ['    '.join(line.split()[0:1] + line.split()[2:]) for line in str_lines]
#first_geometry_str = '\n'.join(modified_lines)
#
#
#atoms = [line.split()[0] for line in first_geometry_str.strip().split('\n')]


# XEDA 2.0
first_geo_idx = path_str[0]
with open(f'output/{first_geo_idx}.log', 'r') as file:
    first_geo_coord = ""
    lines = file.readlines()
    capture = False
    for line in lines:
        if line.startswith('$GEO'): 
            capture = True
            continue
        if capture:
            if line.startswith('$END'): 
                break
            first_geo_coord += line

atoms = [line.split()[0] for line in first_geo_coord.strip().split('\n')]


#----------------------------#

        # show your molecule info. #

print("""
*--------------------------------*
         Your molecule
*--------------------------------*
""")
for i, item in enumerate(atoms):
    print(i+1, item)
print("""
*--------------------------------*
""")


#----------------------------#

        # x-axis type? #

angle_image="""
    ex) input = 1 2 3

            [1]
       [2]< )   angle(deg)
            [3]

"""

distance_image="""
    ex) input = 1 2
    
     [1] --- [2]
          distnace(angs)

"""

dihedral_image="""
    ex) input = 1 2 3 4
    
               [1]
              /                 [1]
      [3]--[2]      =    [2,3]< )   angle(deg)
     /                          [4]
  [4]

"""

while True:
    print("Possible x-axis types : ")
    print(' \n distance \n angle \n dihedral angle \n IRC \n ')
    type = input("Your x-axis type? : ")
    if type == 'distance':
        print("")
        print(distance_image)
        print("")
        two_atoms = input(" Two atoms. a b : ")
        tw = [int(x) for x in two_atoms.split()]
        dis_axis_series = dis_axis(tw[0]+1, tw[1]+1)
        x_axis = dis_axis_series
        print(f" Distance btw. {tw} : \n ")
        print(x_axis)
        print("")
        max = max(x_axis)
        min = min(x_axis)
        print(f" Max value : {max}")
        print(f" Min value : {min}")
        break

    elif type == 'angle':
        print("")
        print(angle_image)
        print("")
        three_atoms = input(" Three atoms. a b c : ")
        thr = [int(x) for x in three_atoms.split()]
        ang_axis_series = ang_axis(thr[0]+1, thr[1]+1, thr[2]+1)
        x_axis = ang_axis_series
        print(f" Angle btw. {thr} : \n ")
        print(x_axis)
        print("")
        max = max(x_axis)
        min = min(x_axis)
        print(f" Max value : {max}")
        print(f" Min value : {min}")
        break

    elif type == 'dihedral angle':
        print("")
        print(dihedral_image)
        print("")
        four_atoms = input(" Four atoms. a b c d : ")
        fr = [int(x) for x in four_atoms.split()]
        dihd_axis_series = dihd_axis(fr[0]+1, fr[1]+1, fr[2]+1, fr[3]+1)
        x_axis = dihd_axis_series
        print(f" Dihedral angle btw. {fr} : \n ")
        print(x_axis)
        print("")
        max = max(x_axis)
        min = min(x_axis)
        print(f" Max value : {max}")
        print(f" Min value : {min}")
        break
    
    elif type == 'IRC':
        x_axis = path_str
        break
        
    else:
        print(" Error: Invalid input")

        
#----------------------------#

        # collects each energy series # 

ES_series_str = []
EX_series_str = []
REP_series_str = []
POL_series_str = []
CORR_series_str = []
E_int_series_str = []

for output in path_str:
    with open(f'output/{output}.log', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(' ELECTROSTATIC ENERGY'):
                ES_value = line.strip().split()[-1]
                globals()[f'ES_value_{output}'] = ES_value
            if line.startswith(' EXCHANGE ENERGY'):
                EX_value = line.strip().split()[-1]
                globals()[f'EX_value_{output}'] = EX_value
            if line.startswith(' REPULSION ENERGY'):
                REP_value = line.strip().split()[-1]
                globals()[f'REP_value_{output}'] = REP_value
            if line.startswith(' POLARIZATION ENERGY'):
                POL_value = line.strip().split()[-1]
                globals()[f'POL_value_{output}'] = POL_value
            if line.startswith(' ELECTRON CORRELATION'):
                CORR_value = line.strip().split()[-1]
                globals()[f'CORR_value_{output}'] = CORR_value
            if line.startswith(' TOTAL INTERACTION ENERGY'):
                E_int_value = line.strip().split()[-1]
                globals()[f'E_int_value_{output}'] = E_int_value
    ES_series_str.append(globals()[f'ES_value_{output}'])
    EX_series_str.append(globals()[f'EX_value_{output}'])
    REP_series_str.append(globals()[f'REP_value_{output}'])
    POL_series_str.append(globals()[f'POL_value_{output}'])
    CORR_series_str.append(globals()[f'CORR_value_{output}'])
    E_int_series_str.append(globals()[f'E_int_value_{output}'])


#----------------------------#

        # str to float #

ES_series = [float(x) for x in ES_series_str]
EX_series = [float(x) for x in EX_series_str]
REP_series = [float(x) for x in REP_series_str]
POL_series = [float(x) for x in POL_series_str]
CORR_series = [float(x) for x in CORR_series_str]
E_int_series = [float(x) for x in E_int_series_str]


#----------------------------#

        # get rel_idx # ; relative energy about local minima

# 만약 initial geometry에 대한 rel. energy를 얻고 싶다면,
# for 문을 지우고 ' rel_idx = 0 ' 활성화


#-------------------#   # inactivate below block!
min_value = float('inf')
rel_idx = -1

for i, num in enumerate(E_int_series):
    if num < min_value:
        min_value = num
        rel_idx = i
#-------------------#

# rel_idx = 0           # activate here!

#-------------------#

#----------------------------#

        # get rel. energy #

ES_series_rel = rel(ES_series, rel_idx)
EX_series_rel = rel(EX_series, rel_idx)
REP_series_rel = rel(REP_series, rel_idx)
POL_series_rel = rel(POL_series, rel_idx)
CORR_series_rel = rel(CORR_series, rel_idx)
E_int_series_rel = rel(E_int_series, rel_idx)


#----------------------------#

        # plot section #

plt.figure(1)

plt.plot(x_axis,ES_series_rel,label='ES',color='blue',linestyle='-',marker='*')
plt.plot(x_axis,EX_series_rel,label='EX',color='green',linestyle='--',marker='o')
plt.plot(x_axis,REP_series_rel,label='REP',color='red',linestyle='-.',marker='s')
plt.plot(x_axis,POL_series_rel,label='POL',color='cyan',linestyle='dotted',marker='D')
plt.plot(x_axis,CORR_series_rel,label='CORR',color='magenta',linestyle='dashdot',marker='+')
plt.plot(x_axis,E_int_series_rel,label='E_int',color='black',linestyle='dashed',marker='x')

print("")
plt.title(input(" Title : "))
plt.xlabel(input(" x-label : "))
plt.ylabel(input(" y-label : "))

while True:
    if type == 'IRC':
        break
    elif type != 'IRC':
        print("")
        print(" x-axis range? Format 'x1 < x < x2' ")
        print("")
        range_str = input(" Format x1 x2 : ")
        range = [float(x) for x in range_str.split()]
        isinstance(range, list)
        plt.xlim(range)
        break
    else:
        print(" What is wrong? ")

plt.legend(loc=2)

#----------------------------#

        # sub plot # ; path vs. x-axis

plt.figure(2)

plt.title("path vs. x-axis")
plt.xlabel("path")
plt.ylabel(f"your x-axis : {type}")
plt.plot(path_str, x_axis,color='black',linestyle='dashed',marker='o')

plt.show()




