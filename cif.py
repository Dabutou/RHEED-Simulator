from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.core.lattice import Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

import math

class Cif():
    def __init__(self, file_name):
        self.struct = Structure.from_file(file_name)


    def input(self, h,k,l):
        self.slabgen = SlabGenerator(self.struct,
                                    miller_index = (h,k,l),
                                    min_slab_size = 10,
                                    min_vacuum_size = 10)
        self.slabs = self.slabgen.get_slabs()
    
    #returns reciprocal lattice constants and geometry of lattice
    def output(self):
        slab_list = []
        for i in range(len(self.slabs)):
            a_real = self.slabs[i].lattice.a
            b_real = self.slabs[i].lattice.b
            gamma = self.slabs[i].lattice.gamma

            a_recip = 2*math.pi / math.sin(math.radians(gamma)) / a_real
            b_recip = 2*math.pi / math.sin(math.radians(gamma)) / b_real
            geom = self.slab_geometry(a_real, b_real, gamma)

            slab_list.append([a_recip, b_recip, geom])
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
