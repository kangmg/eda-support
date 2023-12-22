import glob


def xyz_head_remove(data):
    lines = data.split('\n')
    first_line_split = lines[0].strip().split()
    if len(first_line_split) == 1:
        return 'yes_head'
    elif len(first_line_split) == 4:
        return 'no_head'
    else: 
        print('Check your xyz data files!')

def input_maker(coordinate, HForDFT):
        
    HF_format =f"""
$CTR
METHOD={method} BASIS={basis}
NMUL={nmul} CHARGE={charge}
MAX_ITER={max_iter}
$END
$GEO
{coordinate}
$END
$EDA
NMOL = {nmol}
MATOM = {matom}
MMULT = {mmult}
MCHARGE = {mcharge}
$END
"""

    DFT_format =f"""
$CTR
METHOD={method} BASIS={basis}
NMUL={nmul} CHARGE={charge}
DFT={DFT}
MAX_ITER={max_iter}
$END
$GEO
{coordinate}
$END
$EDA
NMOL = {nmol}
MATOM = {matom}
MMULT = {mmult}
MCHARGE = {mcharge}
$END
"""

    
    if HForDFT == "HF":
        return HF_format
    elif HForDFT == "DFT":
        return DFT_format
    else:
        "Valid input : 'HF' or 'DFT'"
  




#------------------- list --------------------#
    

method_list = ["RHF", "UHF", "ROHF"]

#basis_set_list = ["3-21G","6-31G","6-311G","3-21G*","6-31G*","6-311G*","3-21+G","6-31+G","6-311+G","3-21+G*","6-31+G*","6-311+G*","cc-pVDZ","cc-pVTZ","cc-pVQZ","aug-cc-pVDZ","aug-cc-pVTZ","aug-cc-pVQZ","def2-SVP","def2-SVPP","def2-TZVP","def2-TZVPP","def2-QZVP","def2-QZVPP","def2-QZVPD"]
# to be fix

charge_list = ["0","+1","-1","+2","-2","+3","-3"]

t_multiplicity = ["1","2","3"]

m_multiplicity = ["1","2","3","-1","-2","-3"]

DFT_functional = ["B3LYP","BLYP","B3LYP-D3","B3LYP-D3BJ","CAM-B3LYP","PBE","PBE0","M06-2X","wB97XD"]

#basis_help = [ "-----Pople's basis-----", " # with suffix * for polarization functions"," # with suffix + for diffusion functions","3-21G","6-31G","6-311G","","-----Dunning-type correction consistent basis-----"," # with prefix aug- for diffusion functions","cc-pVDZ","cc-pVTZ","cc-pVQZ","aug-cc-pVDZ","aug-cc-pVTZ","aug-cc-pVQZ","","-----def2 basis-----","def2-SVP","def2-SVPP","def2-TZVP","def2-TZVPP","def2-QZVP","def2-QZVPP","def2-QZVPD"]
basis_help = ['Plz check the XEDA manual','https://xacs.xmu.edu.cn/docs/xeda/content.html#eda-section']

iteration_range = list(range(10,100,1)) # 값 수정 가능
iteration_range = [str(ele) for ele in iteration_range]

monomer_range = list(range(1,10,1))
monomer_range = [str(elem) for elem in monomer_range]



DFT_help = """
# Keyword #     # Functional #

BLYP            BLYP
B3LYP           B3LYP
B3LYP-D3        B3LYP with D3 dispersion correction
B3LYP-D3BJ      B3LYP with D3BJ dispersion correction
CAM-B3LYP       CAM-B3LYP
PBE             PBE
PBE0            Hybrid PBE with 25% HF exchange
M06-2X          M06-2X
wB97XD          B97X-D
"""

#----------------------------------------------------#

# inplements for XEDA 2.0
print("")
print("            XEDA 2.0 input generator            ")
print("")
print("    Type ^C to exit this script    ")
print("")



    
    # CTR section #

                # method #
    
print("Type 'help' for help")

while True:
    print("")
    method = input(" Your Method? : ")
    
    if method in method_list:
        print(f'You entered: {method}')
        break
    elif method == "help":
        print("")
        for item in method_list:
            print(item)
    else:
        print(f"Error: '{method}' is not possible input")
        print("Type 'help' for help")
print("")
print("")


                # basis #
    
while True:
    print("")
    basis = input(" Your Basis? : ")
    
    if basis == "help":
        print("")
        for item in basis_help:
            print(item)
    else:
        print(f'You entered: {basis}')
        break
print("")
print("")


                # total charge #
    
while True:
    print("")
    charge = input(" Total charge : ")
    
    if charge in charge_list:
        print(f'You entered: {charge}')
        break
    elif charge == "help":
        print("")
        print(" e.g \n #  0 for neutral species \n #  +1 for positively charged species")
    else:
        print(f"Error: '{charge}' is not possible value")
        print("Type 'help' for help")
print("")
print("")


                # multiplicity of supermolecule ; NMUL #
    
while True:
    print("")
    nmul = input(" Spin multiplicity : ")
    
    if nmul in t_multiplicity:
        print(f'You entered: {nmul}')
        break
    elif nmul == "help":
        print("")
        print(" 1 for singlet \n 2 for doublet \n 3 for triplet")
    else:
        print(f"Error: '{nmul}' is not possible value")
        print("Type 'help' for help")
print("")
print("")


                # DFT #
print("")                
YorN = input(" 'HF' or 'DFT'? : ")
while True:
    if YorN == "HF":
        print(f'You entered: {YorN}')
        DFT = ""
        print("")
        print("")
        break
    elif YorN == "DFT":
        while True:
            print("")
            DFT = input(" Your DFT functional? e.g. B3LYP or PBE, wB97X-D \n DFT functional : ")
    
            if DFT in DFT_functional:
                print(f'You entered: {DFT}')
                break
            elif DFT == "help":
                print("")
                print(DFT_help)
            else:
                print(f"Error: '{DFT}' is not possible input")
                print("Type 'help' for help")
        print("")
        print("")
        break
    else:
        print(f"Error: '{YorN}' is not possible input")
        print("Type 'HF' or 'DFT'")



                # max interation #
    
while True:
    print("")
    max_iter = input(" Max interation : ")
    
    if max_iter in iteration_range:
        print(f'You entered: {max_iter}')
        break
    elif max_iter == "help":
        print("")
        print("possible value 10 < iteration < 100")
    else:
        print(f"Error: '{max_iter}' is not possible value")
        print("Type 'help' for help")
print("")
print("")


    # GEO section



xyz_files = glob.glob('coordinates/*.xyz')
xyz_data ={}

for i, xyz_file in enumerate(xyz_files):
    file_name = xyz_file.split('/')[-1]
    xyz_files[i] = file_name.split('.')[0]



for xyz_file in xyz_files:  
    with open(f'coordinates/{xyz_file}.xyz', 'r') as file:
        content = file.read()
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





    # EDA section

                # number of monomer #

while True:
    print("")
    nmol = input(" Number of monomers? e.g. 2 (up to 10) \n Number of monomers : ")
    
    if nmol in monomer_range:
        print(f'You entered: {nmol}')
        break
    elif nmol == "help":
        print("")
        print(" 2 < # of monomer < 10 ")
    else:
        print(f"Error: '{nmol}' is not possible input")
        print("Type 'help' for help")
print("")
print("")


                # define monomers #

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

        
while True:
    print("")
    matom = input(" Define your fragments. e.g. '4 3' [4 atoms] [3 atoms] \n Fragments : ")

    frags = matom.split()
    frag_check = len(frags)
        
    if int(nmol) == frag_check:
        print(f'You entered: {matom}')
        break
    elif matom == "help":
        print("")
        print("""
        e.g.
        
        1 H
        2 O
        3 O
        4 H
    
        Type '2 2' for [HO] [OH]          Number of monomers = 2
        Type '1 2 2 1 for [H] [OO] [H]    Number of monomers = 3
        """)
    else:
        print(f"Error: '{matom}' is not possible value")
        print("Type 'help' for help")
print("")
print("")


                # multiplicities of monomer ; mmult #
    
while True:
    print("")
    mmult = input(" Spin multiplicities of monomer. \n \n e.g. 2 for doublet state of alpha spin  \n     -2 for doublet state of beta spin \n \n     Input format : n m   e.g. 2 -2 \n \n Spin multiplicities : ")

    nums = mmult.split()
    nums_check = len(nums)

    
    if int(nmol) == nums_check:
        is_in_m_multiplicity = all(num in m_multiplicity for num in nums)
        if is_in_m_multiplicity:
            print(f'You entered: {mmult}')
            break
    elif mmult == "help":
        print("")
        print("""
    *---------------*
    N for alpha spin
    -N for beta spin
    *---------------*
     e.g.  '1  1' for two water molecules in water dimer
           '2 -2' for seperated two methyl radicals in ethane molecule
        
        """)
    else:
        print(f"Error: '{mmult}' is not possible value")
        print("Type 'help' for help")
print("")
print("")


                # charges of monomer ; mcharge #

while True:
    print("")
    mcharge = input(" Charges of monomer. \n \n Input format : n m   e.g. 0 0  \n \n Charges : ")

    numbs = mcharge.split()
    numbs_check = len(numbs)

    
    if int(nmol) == numbs_check:
        is_in_charge_list = all(numb in charge_list for numb in numbs)
        if is_in_charge_list:
            print(f'You entered: {mcharge}')
            break
    elif mcharge == "help":
        print("")
        print("""

     e.g.  '0  0' for two water molecules in water dimer
           '0  0' for homolytic cleavage of ethane C-C bond
           '1 -1' for heterolytic cleavage of ethane C-C bond
        
        """)
    else:
        print(f"Error: '{mcharge}' is not possible input")
        print("Type 'help' for help")
print("")
print("")





for xyz_file in xyz_files:
    with open(f'input/{xyz_file}.inp', 'w') as file: 
        file.write(input_maker(xyz_data[f'{xyz_file}'], YorN))
