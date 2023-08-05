import matplotlib
matplotlib.use('Agg')
import unittest
from atomap import process_parameters


class test_process_parameters(unittest.TestCase):

    def setUp(self):
        self.generic_structure = process_parameters.GenericStructure()

    def test_generic_structure(self):
        generic_structure = self.generic_structure
        sublattice0 = generic_structure.sublattice_list[0]
        sublattice1 = process_parameters.GenericSublattice()
        generic_structure.add_sublattice_config(sublattice1)
        self.assertEqual(sublattice1.sublattice_order, 1)
        self.assertNotEqual(sublattice0.name, sublattice1.name)
        self.assertNotEqual(sublattice0.tag, sublattice1.tag)
        self.assertNotEqual(sublattice0.color, sublattice1.color)
