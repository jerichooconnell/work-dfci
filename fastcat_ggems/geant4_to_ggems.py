# %% [markdown]
# ## Notebook that parses geant4_materials.txt and outputs files in a materials script for topas

# %%
import re

names = []
weights = []
elements = []
density = []

element_number = []
# element_density = []

with open('geant4_materials.txt','r') as f:
    
    lines = f.readlines()
        
    for ii in range(len(lines)):
        
        line = lines[ii]
        
        if ' AddMaterial' in line:
            
            seps = line.split('"')
            
            if len(seps) > 1:
                
                if len(seps[1]) > 5:
                    
                    jj = ii + 1
                    
                    if ' AddElementByAtom' in lines[jj]:
                        continue
                    
                    weight = []
                    element = []
                    
                    while ' AddElementByWeightFraction' in lines[jj]:
                        
                        numbers = re.split('[\(\)]',lines[jj])[1].split(',')
                        
                        element.append(int(numbers[0]))
                        weight.append(float(numbers[1]))
                        
                        jj += 1
                    
                    elements.append(element)
                    weights.append(weight)    
                    names.append(seps[1])
                    
                    density.append(float(seps[2].split(',')[1]))
                    
                else:
                    element_number.append(int(seps[2].split(',')[2]))
#                     element_density.append(float(seps[2].split(',')[1]))

# %%
# names_mod = [name if name[ii][1:2] == 'G4' for name in names]
names_mod = [(name) for name in names if name[:2]!="G4"]
inds_mod = [(ii) for ii,name in enumerate(names) if name[:2]!="G4"]

# %%
_elements = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen',
             'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine',
             'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron',
             'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton',
             'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium',
             'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon',
             'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium',
             'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium',
             'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury',
             'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium',
             'Thorium', 'Protactinium', 'Uranium']

# %%
colours = ["TransparentBlack","blue","orange","yellow","skyblue","white","grey","green","red"]

# %%
with open('custom_materials_topas.txt','w') as f:
    for ind in range(len(names)):
        
        if '-' in names[ind]:
            continue
        f.writelines('sv:Ma/' + 'XCAT_' + names[ind] + '/Components = ' + str(len(elements[ind]))
               + ' "' + '" "'.join([_elements[element-1] for element in elements[ind]]) + '"' + '\n')
        f.writelines('uv:Ma/' + 'XCAT_' + names[ind] + '/Fractions = ' + str(len(elements[ind]))
               + ' ' + ' '.join([str(weight) for weight in weights[ind]])+ '\n')
        f.writelines('d:Ma/' + 'XCAT_' + names[ind] + '/Density = ' + str(density[ind]) + ' g/cm3 \n')
        f.writelines('s:Ma/' + 'XCAT_' + names[ind] + '/DefaultColor = "' + colours[ind%len(colours)] + '"\n' )
        f.writelines('\n')

# %%
# Do the same for the material but in a format that looks like the gate materials files i.e.:
'''
CsI: d=4.51 g/cm3; n=2;  state=solid
    +el: name=Caesium ; f=0.512
    +el: name=Iodine ; f=0.488

Aluminium: d=2.699 g/cm3; n=1;
	+el: name=Aluminium ; f=1.0

Copper: d=8.96 g/cm3; n=1;  state=solid
    +el: name=Copper ; f=1
'''

with open('custom_materials_ggems.txt','w') as f:
    for ind in range(len(names)):
        
        if '-' in names[ind]:
            continue
        f.writelines(names[ind] + ': d=' + str(density[ind]) + ' g/cm3; n=' + str(len(elements[ind])) + ';  state=solid\n')
        for ii in range(len(elements[ind])):
            f.writelines('    +el: name=' + _elements[elements[ind][ii]-1] + ' ; f=' + str(weights[ind][ii]) + '\n')
        f.writelines('\n')