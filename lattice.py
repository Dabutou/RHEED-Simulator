from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator

import math

class Lattice():
    processed_files = {}
    all_sublattice_slabs = {}

    def __init__(self, file_name):
        self.struct = Structure.from_file(file_name)
        self.elements = self.struct.composition.elements
        if file_name not in Lattice.processed_files:
            Lattice.processed_files[file_name] = "check"
            for i in range(len(self.elements)):
                struct_copy = self.struct.copy()
                elements_copy = self.elements.copy()
                element = elements_copy.pop(i)
                struct_copy.remove_species(elements_copy)
                for h in range(2):
                    for k in range(2):
                        for l in range(2):
                            if (h == k == l == 0) or (math.gcd(math.gcd(h,k),l)>1):
                                continue
                            else:
                                slabgen = SlabGenerator(struct_copy,
                                                        miller_index = (h,k,l),
                                                        min_slab_size = 10,
                                                        min_vacuum_size = 10)
                                slab_key = f'{file_name} {element} {h}{k}{l}'
                                if slab_key not in Lattice.all_sublattice_slabs:
                                    Lattice.all_sublattice_slabs[slab_key] = slabgen.get_slab()
        print('file loaded')


        

            


    """def input(self, h, k, l):
        self.slabs = []
        for i in range(len(self.sublattices)):
            slabgens = SlabGenerator(self.sublattices[i],
                                    miller_index = (h,k,l),
                                    min_slab_size = 10,
                                    min_vacuum_size = 10)
            self.slabs.append(slabgens.get_slab())"""
        
        #print(self.slabs)
    
    #returns reciprocal lattice constants and geometry of lattice
    def output(self, file_name, h, k, l):
        slab_list = []
        for i in range(len(self.elements)):
            slab_key = f'{file_name} {self.elements[i]} {h}{k}{l}'
            slab_temp = Lattice.all_sublattice_slabs[slab_key]
            a_real = slab_temp.lattice.a
            b_real = slab_temp.lattice.b
            gamma = slab_temp.lattice.gamma

            a_recip = 2*math.pi / math.sin(math.radians(gamma)) / a_real
            b_recip = 2*math.pi / math.sin(math.radians(gamma)) / b_real
            #geom = self.slab_geometry(a_real, b_real, gamma)

            slab_list.append([a_recip, b_recip, gamma])
        return slab_list


    #based on 2D Bravais lattices
    #No way to differentiate primitive and centered variants of orthorhomic
    def slab_geometry(self, a, b, g):
        angle_tolerance = 0.01 #in degrees
        length_tolerance = 0.01 #in angstroms
        if abs(a - b) < length_tolerance:
            if abs(g - 60) < angle_tolerance or abs(g - 120) < angle_tolerance:
                return "h" #hexagonal
            elif abs(g - 90) < angle_tolerance:
                return "t" #tetragonal
            else:
                return "no 2D symmetry"
        else:
            if abs(g - 90) < angle_tolerance:
                return "o" #orthorhombic
            else:
                return "m" #monoclinic












"""Si111 = Structure.from_file("D:/Research/RHEED/RHEED Simulator/Si.cif")

slabgen = SlabGenerator(Si111,
                        miller_index = (1,1,1),
                        min_slab_size = 10,
                        min_vacuum_size = 10)

slabs = slabgen.get_slabs()

print(slabs)
print(slabs[0].lattice.gamma)
print(slabs[0].is_symmetric())
print(Lattice.is_hexagonal(slabs[0].lattice))
print(SpacegroupAnalyzer(slabs[0]).get_crystal_system())

for i in range(len(slabs)):
    areal = slabs[i].lattice.a
    breal = slabs[i].lattice.b
    print(SpacegroupAnalyzer(slabs[i]).get_crystal_system())
    print(SpacegroupAnalyzer(slabs[i]).get_lattice_type())"""
