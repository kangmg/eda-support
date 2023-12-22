import glob

def xyz_head_remove(data):
    lines = data.split('\n')
    first_line_split = lines[0].strip().split()
    if len(first_line_split) == 1:
        return 'yes_head'
    elif len(first_line_split) == 4:
        return 'no_head'
    else: 
        print('Check your xyz file format!')

def input_maker(coordinate,basis):
        
    DFT_format_631g =f'''
 $CONTRL SCFTYP={method} RUNTYP=EDA dfttyp={DFT} icharg={charge} mult={nmul} $END
 $SYSTEM  mwords=150 memddi=150 $END
 $BASIS gbasis=n31 ngauss=6 ndfunc=1 $END
 $LMOEDA MATOM(1)={matom} MCHARG(1)={mcharge} MMULT(1)={mmult} edatyp=gks $end
 $scf DIIS=.TRUE. ETHRSH=2.0 SWDIIS=0.005 $end 
 $data
 EDA calculation with XEDA 1.0
 c1
{coordinate}
 $end
'''

    DFT_format_aug_cc_pVTZ =f'''
 $CONTRL SCFTYP={method} RUNTYP=EDA dfttyp={DFT} ispher=1 icharg={charge} mult={nmul} $END
 $SYSTEM  mwords=150 memddi=150 $END
 $BASIS gbasis=accd $END
 $LMOEDA MATOM(1)={matom} MCHARG(1)={mcharge} MMULT(1)={mmult} edatyp=gks $end
 $scf DIIS=.TRUE. ETHRSH=2.0 SWDIIS=0.005 $end
 $data
 EDA calculation with XEDA 1.0
 c1
{coordinate}
 $end
'''
    if basis == '1':
        return DFT_format_631g.ltrip('\n')
    elif basis == '2':
        return DFT_format_aug_cc_pVTZ.lstrip('\n')
    else:
        print('invalid basis option')



def coordi_adapt_gamess(xyz_data):
    gamess_format = ""
    
    lines = xyz_data.split('\n')
    
    for line in lines:
        if line.strip() == '':
            continue  # Skip empty lines
        elements = line.split()
        element_symbol = elements[0]
        coordinates = [float(coord) for coord in elements[1:]]
        
        atomic_number = element_dict.get(element_symbol)
        
        if atomic_number is not None:
            gamess_format += f"{element_symbol:2} {atomic_number:2d}" + ''.join([f"{coord:16.10f}" for coord in coordinates]) + '\n'
    
    return gamess_format.strip()


charge_list = ["0","+1","-1","+2","-2","+3","-3"]

t_multiplicity = ["1","2","3"]

m_multiplicity = ["1","2","3","-1","-2","-3"]

element_dict = {
    'H': 1,
    'He': 2,
    'Li': 3,
    'Be': 4,
    'B': 5,
    'C': 6,
    'N': 7,
    'O': 8,
    'F': 9,
    'Ne': 10,
    'Na': 11,
    'Mg': 12,
    'Al': 13,
    'Si': 14,
    'P': 15,
    'S': 16,
    'Cl': 17,
    'Ar': 18,
    'K': 19,
    'Ca': 20,
    'Ga': 31,
    'Ge': 32,
    'As': 33,
    'Se': 34,
    'Br': 35
}


# inplements for XEDA 1.0
print("")
print("            XEDA 1.0 input generator            ")
print("")
print("    Type ^C to exit this script    ")
print("")


    
print("")
method = input(" Your Method? : ")    
print(f'You entered: {method}')
print("")
print("")

    
basis = input("Basis Function \n Now two basis types are available.\n\n 1 : 6-31G* \n 2 : aug-cc-pVTZ \n\n Your Basis? : ")
print(f'You entered: {basis}')
print("")
print("")


charge = input(" Total charge : ")
print(f'You entered: {charge}')
print("")
print("")


nmul = input(" Spin multiplicity : ")
print(f'You entered: {nmul}')
print("")
print("")


DFT = input(" Your DFT functional? e.g. B3LYP \n DFT functional : ")
print(f'You entered: {DFT}')
print("")
print("")

    

xyz_files = glob.glob('coordinates/*.xyz')
xyz_data ={}



for i, xyz_file in enumerate(xyz_files):
    file_name = xyz_file.split('/')[-1]
    xyz_files[i] = file_name.split('.')[0]


for xyz_file in xyz_files:  
    with open(f'coordinates/{xyz_file}.xyz', 'r') as file:
        content_bc = file.read()
        content = content_bc.strip()
        flag = xyz_head_remove(content)
        if flag == 'yes_head':
            lines = content.splitlines()[2:]
        elif flag == 'no_head':
            lines = content.splitlines()
        else:
            print('flag_error')
        content = '\n'.join(lines)
        xyz_data[xyz_file] = content



atoms_head_data = xyz_data[xyz_files[0]]
atoms = [line.split()[0] for line in atoms_head_data.strip().split('\n')]



print("")
print("")
nmol = input(" Number of monomers? e.g. 2 (up to 10) \n Number of monomers : ")
print(f'You entered: {nmol}')
print("")
print("")


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

        
print("")
print("")
matom = input(" Define your fragments. e.g. '4 3' [4 atoms] [3 atoms] \n Fragments : ")

frags = matom.split()
frag_check = len(frags)
        
if int(nmol) == frag_check:
    print(f'You entered: {matom}')
else:
    print(f"Error: '{matom}' is not possible value")
print("")
print("")


    
mmult = input(" Spin multiplicities of monomer. \n \n e.g. 2 for doublet state of alpha spin  \n     -2 for doublet state of beta spin \n \n     Input format : n m   e.g. 2 -2 \n \n Spin multiplicities : ")
nums = mmult.split()
nums_check = len(nums)
if int(nmol) == nums_check:
    is_in_m_multiplicity = all(num in m_multiplicity for num in nums)
    if is_in_m_multiplicity:
        print(f'You entered: {mmult}')
else:
    print(f"Error: '{mmult}' is not possible value")
print("")
print("")



mcharge = input(" Charges of monomer. \n \n Input format : n m   e.g. 0 0  \n \n Charges : ")
numbs = mcharge.split()
numbs_check = len(numbs)
if int(nmol) == numbs_check:
    is_in_charge_list = all(numb in charge_list for numb in numbs)
    if is_in_charge_list:
        print(f'You entered: {mcharge}')
else:
    print(f"Error: '{mcharge}' is not possible input")
print("")
print("")


for xyz_file in xyz_files:
    coordi_gamess_format = coordi_adapt_gamess(xyz_data[f'{xyz_file}'])
    with open(f'input/{xyz_file}.inp', 'w') as file: 
        file.write(input_maker(coordi_gamess_format,basis))