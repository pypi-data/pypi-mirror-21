# -*. coding: utf-8 -*-
# Copyright (c) 2008-2011, Noel O'Boyle; 2012, Adrià Cereto-Massagué; 2014-2016, Maciej Wójcikowski;
# All rights reserved.
#
#  This file is part of Cinfony.
#  The contents are covered by the terms of the BSD license
#  which is included in the file LICENSE_BSD.txt.

"""
rdkit - A Cinfony module for accessing the RDKit from CPython

Global variables:
  Chem and AllChem - the underlying RDKit Python bindings
  informats - a dictionary of supported input formats
  outformats - a dictionary of supported output formats
  descs - a list of supported descriptors
  fps - a list of supported fingerprint types
  forcefields - a list of supported forcefields
"""

from __future__ import print_function
import os
from copy import copy
import gzip
from base64 import b64encode
from itertools import combinations, chain
from collections import OrderedDict

from six import next, BytesIO, PY3
import numpy as np

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import Descriptors
from rdkit import RDConfig

import rdkit.DataStructs
import rdkit.Chem.MACCSkeys
import rdkit.Chem.AtomPairs.Pairs
import rdkit.Chem.AtomPairs.Torsions
# ODDT #
from rdkit.Chem.Lipinski import NumRotatableBonds
from rdkit.Chem.AllChem import ComputeGasteigerCharges
from rdkit.Chem.Pharm2D import Gobbi_Pharm2D, Generate

import oddt.pandas
from oddt.toolkits.common import detect_secondary_structure
from oddt.toolkits.extras.rdkit import _sybyl_atom_type, MolFromPDBBlock

_descDict = dict(Descriptors.descList)

backend = 'rdk'

elementtable = Chem.GetPeriodicTable()

BOND_ORDERS = {Chem.BondType.SINGLE: 1.0,
               Chem.BondType.DOUBLE: 2.0,
               Chem.BondType.TRIPLE: 3.0,
               Chem.BondType.AROMATIC: 1.5,
               Chem.BondType.UNSPECIFIED: 0.0}
SMARTS_DEF = {
    'rot_bond': Chem.MolFromSmarts('[!$(*#*)&!D1&!$(C(F)(F)F)&'
                                   '!$(C(Cl)(Cl)Cl)&'
                                   '!$(C(Br)(Br)Br)&'
                                   '!$(C([CH3])([CH3])[CH3])&'
                                   '!$([CD3](=[N,O,S])-!@[#7,O,S!D1])&'
                                   '!$([#7,O,S!D1]-!@[CD3]=[N,O,S])&'
                                   '!$([CD3](=[N+])-!@[#7!D1])&'
                                   '!$([#7!D1]-!@[CD3]=[N+])]-!@[!$(*#*)&'
                                   '!D1&!$(C(F)(F)F)&'
                                   '!$(C(Cl)(Cl)Cl)&'
                                   '!$(C(Br)(Br)Br)&'
                                   '!$(C([CH3])([CH3])[CH3])]').GetBonds()[0]
}
# trap errors since it's still new feature
try:
    from rdkit.Chem import CanonicalRankAtoms
except ImportError:
    pass

# PIL and Tkinter
try:
    import Tkinter as tk
    import Image as PIL
    import ImageTk as PILtk
except:
    PILtk = None

# Aggdraw
try:
    import aggdraw
    from rdkit.Chem.Draw import aggCanvas
except ImportError:
    aggdraw = None

fps = ['rdkit', 'layered', 'maccs', 'atompairs', 'torsions', 'morgan']
"""A list of supported fingerprint types"""
descs = list(_descDict.keys())
"""A list of supported descriptors"""

_formats = {'smi': "SMILES",
            'can': "Canonical SMILES",
            'mol': "MDL MOL file",
            'mol2': "Tripos MOL2 file",
            'sdf': "MDL SDF file",
            'inchi': "InChI",
            'inchikey': "InChIKey"}
_notinformats = ['can', 'inchikey']
_notoutformats = ['mol2']
if not Chem.INCHI_AVAILABLE:
    _notinformats += ['inchi']
    _notoutformats += ['inchi', 'inchikey']

informats = dict([(_x, _formats[_x]) for _x in _formats if _x not in _notinformats])
"""A dictionary of supported input formats"""
outformats = dict([(_x, _formats[_x]) for _x in _formats if _x not in _notoutformats])
"""A dictionary of supported output formats"""

base_feature_factory = AllChem.BuildFeatureFactory(os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef'))
""" Global feature factory based on BaseFeatures.fdef """

_forcefields = {'uff': AllChem.UFFOptimizeMolecule,
                'mmff94': AllChem.MMFFOptimizeMolecule}
forcefields = list(_forcefields.keys())
"""A list of supported forcefields"""


def _filereader_mol2(filename):
    block = ''
    data = ''
    n = 0
    with gzip.open(filename, 'rb') if filename.split('.')[-1] == 'gz' else open(filename, 'rb') as f:
        for line in f:
            line = line.decode('ascii')
            if line[:1] == '#':
                data += line
            elif line[:17] == '@<TRIPOS>MOLECULE':
                if n > 0:  # skip `zero` molecule (any preciding comments and spaces)
                    yield Molecule(source={'fmt': 'mol2', 'string': block})
                n += 1
                block = data
                data = ''
            block += line
        # open last molecule
        if block:
            yield Molecule(source={'fmt': 'mol2', 'string': block})


def _filereader_sdf(filename):
    block = ''
    n = 0
    with gzip.open(filename, 'rb') if filename.split('.')[-1] == 'gz' else open(filename, 'rb') as f:
        for line in f:
            line = line.decode('ascii')
            block += line
            if line[:4] == '$$$$':
                yield Molecule(source={'fmt': 'sdf', 'string': block})
                n += 1
                block = ''
        if block:  # open last molecule if any
            yield Molecule(source={'fmt': 'sdf', 'string': block})


def _filereader_pdb(filename, opt=None):
    block = ''
    n = 0
    with gzip.open(filename, 'rb') if filename.split('.')[-1] == 'gz' else open(filename, 'rb') as f:
        for line in f:
            line = line.decode('ascii')
            block += line
            if line[:4] == 'ENDMDL':
                yield Molecule(source={'fmt': 'pdb', 'string': block, 'opt': opt})
                n += 1
                block = ''
        if block:  # open last molecule if any
            yield Molecule(source={'fmt': 'pdb', 'string': block, 'opt': opt})


def readfile(format, filename, lazy=False, opt=None, *args, **kwargs):
    """Iterate over the molecules in a file.

    Required parameters:
       format - see the informats variable for a list of available
                input formats
       filename

    You can access the first molecule in a file using the next() method
    of the iterator:
        mol = next(readfile("smi", "myfile.smi"))

    You can make a list of the molecules in a file using:
        mols = list(readfile("smi", "myfile.smi"))

    You can iterate over the molecules in a file as shown in the
    following code snippet:
    >>> atomtotal = 0
    >>> for mol in readfile("sdf", "head.sdf"):
    ...     atomtotal += len(mol.atoms)
    ...
    >>> print(atomtotal)
    43
    """
    if not os.path.isfile(filename):
        raise IOError("No such file: '%s'" % filename)
    format = format.lower()
    # Eagerly evaluate the supplier functions in order to report
    # errors in the format and errors in opening the file.
    # Then switch to an iterator...
    if format in ["sdf", "mol"]:
        if lazy:
            return _filereader_sdf(filename)
        else:
            filename_handle = gzip.open(filename, 'rb') if filename.split('.')[-1] == 'gz' else open(filename, 'rb')
            return (Molecule(Mol) for Mol in Chem.ForwardSDMolSupplier(filename_handle, **kwargs))
    elif format == "pdb":
        def mol_reader():
            with open(filename) as f:
                yield Molecule(MolFromPDBBlock(f.read(), *args, **kwargs))
        return mol_reader()
    elif format == "mol2":
        return _filereader_mol2(filename)
    elif format == "smi":
        iterator = Chem.SmilesMolSupplier(filename, delimiter=" \t",
                                          titleLine=False, *args, **kwargs)

        def smi_reader():
            for mol in iterator:
                yield Molecule(mol)
        return smi_reader()
    elif format == 'inchi' and Chem.INCHI_AVAILABLE:
        def inchi_reader():
            for line in open(filename):
                mol = Chem.inchi.MolFromInchi(line.strip(), *args, **kwargs)
                yield Molecule(mol)
        return inchi_reader()
    else:
        raise ValueError("%s is not a recognised RDKit format" % format)


def readstring(format, string, **kwargs):
    """Read in a molecule from a string.

    Required parameters:
       format - see the informats variable for a list of available
                input formats
       string

    Example:
    >>> input = "C1=CC=CS1"
    >>> mymol = readstring("smi", input)
    >>> len(mymol.atoms)
    5
    """
    string = str(string)
    format = format.lower()
    if format in ["mol", "sdf"]:
        supplier = Chem.SDMolSupplier()
        supplier.SetData(string)
        mol = next(supplier)
        del supplier
    elif format == "mol2":
        mol = Chem.MolFromMol2Block(string, **kwargs)
    elif format == "pdb":
        mol = MolFromPDBBlock(string, **kwargs)
    elif format == "smi":
        s = string.strip().split('\n')[0].strip().split()
        mol = Chem.MolFromSmiles(s[0], **kwargs)
        if mol:
            mol.SetProp("_Name", ' '.join(s[1:]))
    elif format == 'inchi' and Chem.INCHI_AVAILABLE:
        mol = Chem.inchi.MolFromInchi(string, **kwargs)
    else:
        raise ValueError("%s is not a recognised RDKit format" % format)
    return Molecule(mol)


class Outputfile(object):
    """Represent a file to which *output* is to be sent.

    Required parameters:
       format - see the outformats variable for a list of available
                output formats
       filename

    Optional parameters:
       overwite -- if the output file already exists, should it
                   be overwritten? (default is False)

    Methods:
       write(molecule)
       close()
    """
    def __init__(self, format, filename, overwrite=False):
        self.format = format
        self.filename = filename
        if not overwrite and os.path.isfile(self.filename):
            raise IOError("%s already exists. Use 'overwrite=True' to overwrite it." % self.filename)
        if format == "sdf":
            self._writer = Chem.SDWriter(self.filename)
        elif format == "smi":
            self._writer = Chem.SmilesWriter(self.filename, isomericSmiles=True, includeHeader=False)
        elif format in ('inchi', 'inchikey') and Chem.INCHI_AVAILABLE:
            self._writer = open(filename, 'w')
        elif format in ('mol2'):
            self._writer = gzip.open(filename, 'w') if filename.split('.')[-1] == 'gz' else open(filename, 'w')
        elif format == "pdb":
            self._writer = Chem.PDBWriter(self.filename)
        else:
            raise ValueError("%s is not a recognised RDKit format" % format)
        self.total = 0  # The total number of molecules written to the file

    def write(self, molecule):
        """Write a molecule to the output file.

        Required parameters:
           molecule
        """
        if not self.filename:
            raise IOError("Outputfile instance is closed.")
        if self.format in ('inchi', 'inchikey', 'mol2'):
            self._writer.write(molecule.write(self.format) + '\n')
        else:
            self._writer.write(molecule.Mol)
        self.total += 1

    def close(self):
        """Close the Outputfile to further writing."""
        self.filename = None
        self._writer.flush()
        del self._writer


class Molecule(object):
    """Represent an rdkit Molecule.

    Required parameter:
       Mol -- an RDKit Mol or any type of cinfony Molecule

    Attributes:
       atoms, data, formula, molwt, title

    Methods:
       addh(), calcfp(), calcdesc(), draw(), localopt(), make3D(), removeh(),
       write()

    The underlying RDKit Mol can be accessed using the attribute:
       Mol
    """
    _cinfony = True

    def __new__(cls, Mol=-1, source=None, *args, **kwargs):
        """ Trap RDKit molecules which are 'None' """
        if Mol is None and source is None:
            return None
        else:
            return super(Molecule, cls).__new__(cls)

    def __init__(self, Mol=None, source=None, protein=False):
        if hasattr(Mol, "_cinfony"):
            a, b = Mol._exchange
            if a == 0:
                molecule = readstring("smi", b)
            else:
                molecule = readstring("mol", b)
            Mol = molecule.Mol

        self.Mol = Mol
        # ODDT #
        self.protein = protein
        # caches
        self._atom_dict = None
        self._res_dict = None
        self._ring_dict = None
        self._coords = None
        self._charges = None
        self._residues = None
        # lazy
        self._source = source  # dict with keys: n, fmt, string, filename
        if Mol is None and not source:
            self = None
            return None

    # lazy Molecule parsing requires masked Mol
    @property
    def Mol(self):
        if not self._Mol and self._source:
            tmp_mol = readstring(self._source['fmt'], self._source['string'])
            if tmp_mol is None:
                self = None
                return None
            else:
                self._Mol = tmp_mol.Mol
                self._source = None
        return self._Mol

    @Mol.setter
    def Mol(self, value):
        self._Mol = value

    @property
    def atoms(self):
        return AtomStack(self.Mol)

    @property
    def data(self):
        return MoleculeData(self.Mol)

    @property
    def molwt(self):
        return Descriptors.MolWt(self.Mol)

    @property
    def formula(self):
        return Descriptors.MolecularFormula(self.Mol)

    def _gettitle(self):
        # Note to self: maybe should implement the get() method for self.data
        if "_Name" in self.data:
            return self.data["_Name"]
        else:
            return ""

    def _settitle(self, val):
        self.Mol.SetProp("_Name", val)

    title = property(_gettitle, _settitle)

    @property
    def _exchange(self):
        if self.Mol.GetNumConformers() == 0:
            return (0, self.write("smi"))
        else:
            return (1, self.write("mol"))

    # cache frequently used properties and cache them in prefixed [_] variables
    @property
    def coords(self):
        if self._coords is None:
            self._coords = np.array([atom.coords for atom in self.atoms], dtype=np.float32)
            self._coords.setflags(write=False)
        return self._coords

    @coords.setter
    def coords(self, new):
        new = np.asarray(new, dtype=np.float64)
        if self.Mol.GetNumConformers() == 0:
            raise AttributeError("Atom has no coordinates (0D structure)")
        if self.Mol.GetNumAtoms() != new.shape[0]:
            raise AttributeError("Atom number is unequal. You have to supply new coordinates for all atoms")
        conformer = self.Mol.GetConformer()
        for idx in range(self.Mol.GetNumAtoms()):
            conformer.SetAtomPosition(idx, new[idx, :])
        # clear cache
        self._coords = None
        self._atom_dict = None

    @property
    def charges(self):
        if self._charges is None:
            self._charges = np.array([atom.partialcharge for atom in self.atoms])
        return self._charges

    @property
    def smiles(self):
        return Chem.MolToSmiles(self.Mol, isomericSmiles=True)

    # Custom ODDT properties #
    def _clear_cache(self):
        """Clear all ODDT caches and dicts"""
        self._atom_dict = None
        self._res_dict = None
        self._ring_dict = None
        self._coords = None
        self._charges = None
        self._residues = None

    @property
    def residues(self):
        if self._residues is None:
            res_idx = np.array([atom.GetPDBResidueInfo().GetResidueNumber()
                                if atom.GetPDBResidueInfo() is not None else 0
                                for atom in self.Mol.GetAtoms()])
            if len(np.unique(res_idx)) > 1:
                self._residues = np.split(np.argsort(res_idx, kind='mergesort'),
                                          (np.argwhere(np.diff(np.sort(res_idx)) != 0)
                                          .flatten() + 1))
            else:
                self._residues = [tuple(range(self.Mol.GetNumAtoms()))]
        return ResidueStack(self.Mol, self._residues)

    @property
    def sssr(self):
        return [list(path) for path in list(Chem.GetSymmSSSR(self.Mol))]

    @property
    def num_rotors(self):
        return NumRotatableBonds(self.Mol)

    @property
    def bonds(self):
        return BondStack(self.Mol)

    @property
    def canonic_order(self):
        """ Returns np.array with canonic order of heavy atoms in the molecule """
        tmp = self.clone
        tmp.removeh()
        return np.array(CanonicalRankAtoms(tmp.Mol), dtype=int)

    @property
    def atom_dict(self):
        # check cache and generate dicts
        if self._atom_dict is None:
            self._dicts()
        return self._atom_dict

    @property
    def res_dict(self):
        # check cache and generate dicts
        if self._res_dict is None:
            self._dicts()
        return self._res_dict

    @property
    def ring_dict(self):
        # check cache and generate dicts
        if self._ring_dict is None:
            self._dicts()
        return self._ring_dict

    @property
    def clone(self):
        return Molecule(Chem.Mol(self.Mol.ToBinary()))

    def _repr_svg_(self, size=(200, 200)):
        svg = self.write('svg', size=size)
        return svg.replace('svg:', '').replace('\n', '')

    def _repr_png_(self, size=(200, 200)):
        png = self.write('png', size=size)
        return '<img src="data:image/png;base64,%s" alt="%s">' % (
            b64encode(png).decode('ascii'),
            self.title)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if oddt.pandas.ipython_notebook:
            if oddt.pandas.image_backend == 'png':
                return self._repr_png_(size=oddt.pandas.image_size)
            else:
                return self._repr_svg_(size=oddt.pandas.image_size)
        else:
            return super(Molecule, self).__repr__()

    def clone_coords(self, source):
        self.Mol.RemoveAllConformers()
        for conf in source.Mol.GetConformers():
            self.Mol.AddConformer(conf)
        return self

    def _dicts(self):
        # Atoms
        atom_dtype = [('id', np.int16),
                      # atom info
                      ('coords', np.float32, 3),
                      ('radius', np.float32),
                      ('charge', np.float32),
                      ('atomicnum', np.int8),
                      ('atomtype', 'U5' if PY3 else 'a5'),
                      ('hybridization', np.int8),
                      ('neighbors', np.float32, (4, 3)),  # non-H neighbors coordinates for angles (max of 6 neighbors should be enough)
                      # residue info
                      ('resid', np.int16),
                      ('resname', 'U3' if PY3 else 'a3'),
                      ('isbackbone', bool),
                      # atom properties
                      ('isacceptor', bool),
                      ('isdonor', bool),
                      ('isdonorh', bool),
                      ('ismetal', bool),
                      ('ishydrophobe', bool),
                      ('isaromatic', bool),
                      ('isminus', bool),
                      ('isplus', bool),
                      ('ishalogen', bool),
                      # secondary structure
                      ('isalpha', bool),
                      ('isbeta', bool),
                      ]

        a = []
        atom_dict = np.empty(self.Mol.GetNumAtoms(), dtype=atom_dtype)
        metals = [3, 4, 11, 12, 13, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                  30, 31, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                  50, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                  69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
                  87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101,
                  102, 103]
        for i, atom in enumerate(self.atoms):

            atomicnum = atom.atomicnum
            partialcharge = atom.partialcharge
            coords = atom.coords
            atomtype = (atom.Atom.GetProp("_TriposAtomType")
                        if atom.Atom.HasProp("_TriposAtomType")
                        else _sybyl_atom_type(atom.Atom))
            if self.protein:
                residue = atom.Atom.GetMonomerInfo()
            else:
                residue = False

            # get neighbors, but only for those atoms which realy need them
            neighbors = np.zeros(4, dtype=[('coords', np.float32, 3),
                                           ('atomicnum', np.int8)])
            neighbors['coords'].fill(np.nan)
            for n, nbr_atom in enumerate(atom.neighbors):
                neighbors[n] = (nbr_atom.coords, nbr_atom.atomicnum)
            atom_dict[i] = (atom.idx,
                            coords,
                            elementtable.GetRvdw(atomicnum),
                            partialcharge if atomicnum > 1 else 0,
                            atomicnum,
                            atomtype,
                            np.clip(atom.Atom.GetHybridization() - 1, 0, 3),
                            neighbors['coords'],
                            # residue info
                            residue.GetResidueNumber() if residue else 0,
                            residue.GetResidueName().strip() if residue else '',
                            False,  # is backbone
                            # atom properties
                            False,  # IsHbondAcceptor
                            False,  # IsHbondDonor,
                            False,  # IsHbondDonorH,
                            atomicnum in metals,
                            atomicnum == 6 and np.in1d(neighbors['atomicnum'], [6, 1, 0]).all(),  # hydrophobe
                            atom.Atom.GetIsAromatic(),
                            atom.formalcharge < 0,  # is charged (minus)
                            atom.formalcharge > 0,  # is charged (plus)
                            atomicnum in [9, 17, 35, 53],  # is halogen?
                            False,  # alpha
                            False  # beta
                            )

        not_carbon = np.argwhere(~np.in1d(atom_dict['atomicnum'], [1, 6])).flatten()
        # Acceptors
        patt = Chem.MolFromSmarts('[$([O;H1;v2]),'
                                  '$([O;H0;v2;!$(O=N-*),'
                                  '$([O;-;!$(*-N=O)]),'
                                  '$([o;+0])]),'
                                  '$([n;+0;!X3;!$([n;H1](cc)cc),'
                                  '$([$([N;H0]#[C&v4])]),'
                                  '$([N&v3;H0;$(Nc)])]),'
                                  '$([F;$(F-[#6]);!$(FC[F,Cl,Br,I])])]')
        matches = np.array(self.Mol.GetSubstructMatches(patt, maxMatches=5000)).flatten()
        if len(matches) > 0:
            atom_dict['isacceptor'][np.intersect1d(matches, not_carbon)] = True

        # Donors
        patt = Chem.MolFromSmarts('[$([N&!H0&v3,N&!H0&+1&v4,n&H1&+0,$([$([Nv3](-C)(-C)-C)]),'
                                  '$([$(n[n;H1]),'
                                  '$(nc[n;H1])])]),'
                                  # Guanidine can be tautormeic - e.g. Arginine
                                  '$([NX3,NX2]([!O,!S])!@C(!@[NX3,NX2]([!O,!S]))!@[NX3,NX2]([!O,!S])),'
                                  '$([O,S;H1;+0])]')
        matches = np.array(self.Mol.GetSubstructMatches(patt, maxMatches=5000)).flatten()
        if len(matches) > 0:
            atom_dict['isdonor'][np.intersect1d(matches, not_carbon)] = True
            atom_dict['isdonorh'][[n.GetIdx()
                                   for idx in np.argwhere(atom_dict['isdonor']).flatten()
                                   for n in self.Mol.GetAtomWithIdx(int(idx)).GetNeighbors()
                                   if n.GetAtomicNum() == 1]] = True

        # Basic group
        patt = Chem.MolFromSmarts('[$([N;H2&+0][$([C,a]);!$([C,a](=O))]),'
                                  '$([N;H1&+0]([$([C,a]);!$([C,a](=O))])[$([C,a]);!$([C,a](=O))]),'
                                  '$([N;H0&+0]([C;!$(C(=O))])([C;!$(C(=O))])[C;!$(C(=O))]),'
                                  '$([N,n;X2;+0])]')
        matches = np.array(self.Mol.GetSubstructMatches(patt, maxMatches=5000)).flatten()
        if len(matches) > 0:
            atom_dict['isplus'][np.intersect1d(matches, not_carbon)] = True

        # Acidic group
        patt = Chem.MolFromSmarts('[$([C,S](=[O,S,P])-[O;H1])]')
        matches = np.array(self.Mol.GetSubstructMatches(patt, maxMatches=5000)).flatten()
        if len(matches) > 0:
            atom_dict['isminus'][np.intersect1d(matches, not_carbon)] = True

        # Match features and mark them in atom_dict
        translate_feats = {
                        #    'Donor': 'isdonor',
                        #    'Acceptor': 'isacceptor',
                        #    'NegIonizable': 'isminus',
                        #    'PosIonizable': 'isplus',
                           }

        # build residue dictionary
        if self.protein:
            # for protein finding features per residue is much faster
            for res in self.residues:
                for f, field in translate_feats.items():
                    feats = base_feature_factory.GetFeaturesForMol(res.Residue, includeOnly=f)
                    atom_dict[field][[res.atommap[idx]
                                      for feat in feats
                                      for idx in feat.GetAtomIds()
                                      if atom_dict['atomicnum'][res.atommap[idx]] > 1]] = True
                    # Mark donor Hs
                    if field == 'isdonor':
                        atom_dict['isdonorh'][[res.atommap[n.GetIdx()]
                                               for feat in feats
                                               for idx in feat.GetAtomIds()
                                               for n in res.Residue.GetAtomWithIdx(idx).GetNeighbors()
                                               if n.GetAtomicNum() == 1]] = True

            res_dict = None
            # Protein Residues (alpha helix and beta sheet)
            res_dtype = [('id', np.int16),
                         ('resname', 'U3' if PY3 else 'a3'),
                         ('N', np.float32, 3),
                         ('CA', np.float32, 3),
                         ('C', np.float32, 3),
                         ('O', np.float32, 3),
                         ('isalpha', bool),
                         ('isbeta', bool)
                         ]  # N, CA, C, O
            b = []
            aa = Chem.MolFromSmarts('NCC(-,=O)')  # amino backbone SMARTS
            conf = self.Mol.GetConformer()
            for residue in self.residues:
                path = residue.Residue.GetSubstructMatch(aa)
                if path:
                    atom_dict['isbackbone'][np.array([residue.atommap[i] for i in path])] = True
                    b.append((residue.MonomerInfo.GetResidueNumber(),
                              residue.MonomerInfo.GetResidueName(),
                              conf.GetAtomPosition(residue.atommap[path[0]]),
                              conf.GetAtomPosition(residue.atommap[path[1]]),
                              conf.GetAtomPosition(residue.atommap[path[2]]),
                              conf.GetAtomPosition(residue.atommap[path[3]]),
                              False,
                              False))
            res_dict = np.array(b, dtype=res_dtype)
            res_dict = detect_secondary_structure(res_dict)
            atom_dict['isalpha'][np.in1d(atom_dict['resid'], res_dict[res_dict['isalpha']]['id'])] = True
            atom_dict['isbeta'][np.in1d(atom_dict['resid'], res_dict[res_dict['isbeta']]['id'])] = True
        else:
            # find features for ligands
            for f, field in translate_feats.items():
                feats = base_feature_factory.GetFeaturesForMol(self.Mol, includeOnly=f)
                atom_dict[field][[idx
                                  for f in feats
                                  for idx in f.GetAtomIds()
                                  if atom_dict['atomicnum'][idx] > 1]] = True
                if field == 'isdonor':
                    atom_dict['isdonorh'][[n.GetIdx()
                                           for f in feats
                                           for idx in f.GetAtomIds()
                                           for n in self.Mol.GetAtomWithIdx(idx).GetNeighbors()
                                           if n.GetAtomicNum() == 1]] = True

        # FIX: remove acidic carbons from isminus group (they are part of smarts)
        atom_dict['isminus'][atom_dict['isminus'] & (atom_dict['atomicnum'] == 6)] = False

        # Aromatic Rings
        r = []
        for path in self.sssr:
            if self.Mol.GetAtomWithIdx(path[0]).GetIsAromatic():
                atoms = atom_dict[np.in1d(atom_dict['id'], path)]
                if len(atoms):
                    atom = atoms[0]
                    coords = atoms['coords']
                    centroid = coords.mean(axis=0)
                    # get vector perpendicular to ring
                    vector = np.cross(coords - np.vstack((coords[1:], coords[:1])), np.vstack((coords[1:], coords[:1])) - np.vstack((coords[2:], coords[:2]))).mean(axis=0) - centroid
                    r.append((centroid, vector, atom['isalpha'], atom['isbeta']))
        ring_dict = np.array(r, dtype=[('centroid', np.float32, 3),
                                       ('vector', np.float32, 3),
                                       ('isalpha', bool),
                                       ('isbeta', bool)])

        self._atom_dict = atom_dict
        self._atom_dict.setflags(write=False)
        self._ring_dict = ring_dict
        self._ring_dict.setflags(write=False)
        if self.protein:
            self._res_dict = res_dict
            # self._res_dict.setflags(write=False)

    def addh(self, only_polar=False, **kwargs):
        """Add hydrogens."""
        if only_polar:
            polar_atoms = [atom.GetIdx()
                           for atom in self.Mol.GetAtoms()
                           if atom.GetAtomicNum() != 6]
        else:
            polar_atoms = None

        self.Mol = Chem.AddHs(self.Mol, addCoords=True, onlyOnAtoms=polar_atoms, **kwargs)
        self._clear_cache()
        # merge Hs to residues
        if self.protein:
            for atom in self.Mol.GetAtoms():
                if atom.GetAtomicNum() == 1:
                    assert atom.GetDegree() == 1
                    neighbor_atom = atom.GetNeighbors()[0]
                    res = neighbor_atom.GetPDBResidueInfo()
                    if res is not None:
                        resid = res.GetResidueNumber()
                        resname = res.GetResidueName()
                        reschain = res.GetChainId()
                        atom.SetMonomerInfo(
                            Chem.AtomPDBResidueInfo(atomName=' H  ',
                                                    serialNumber=res.GetSerialNumber(),
                                                    residueName=res.GetResidueName(),
                                                    residueNumber=res.GetResidueNumber(),
                                                    chainId=res.GetChainId(),
                                                    insertionCode="",
                                                    isHeteroAtom=res.GetIsHeteroAtom()))

    def removeh(self, **kwargs):
        """Remove hydrogens."""
        self.Mol = Chem.RemoveHs(self.Mol, **kwargs)
        self._clear_cache()

    def write(self, format="smi", filename=None, overwrite=False, size=None, **kwargs):
        """Write the molecule to a file or return a string.

        Optional parameters:
           format -- see the informats variable for a list of available
                     output formats (default is "smi")
           filename -- default is None
           overwite -- if the output file already exists, should it
                       be overwritten? (default is False)

        If a filename is specified, the result is written to a file.
        Otherwise, a string is returned containing the result.

        To write multiple molecules to the same file you should use
        the Outputfile class.
        """
        format = format.lower()
        # Use lazy molecule if possible
        if self._source and 'fmt' in self._source and self._source['fmt'] == format and self._source['string']:
            return self._source['string']
        if filename:
            if not overwrite and os.path.isfile(filename):
                raise IOError("%s already exists. Use 'overwrite=True' to overwrite it." % filename)
        if format == "smi" or format == "can":
            result = '%s\t%s\n' % (Chem.MolToSmiles(self.Mol, **kwargs), self.title)
        elif format in ["mol", "sdf"]:
            result = Chem.MolToMolBlock(self.Mol, **kwargs)
        elif format == "mol2":
            result = Chem.MolToMol2Block(self.Mol, **kwargs)
        elif format == "pdb":
            result = Chem.MolToPDBBlock(self.Mol, **kwargs)
        elif format in ('inchi', 'inchikey') and Chem.INCHI_AVAILABLE:
            result = Chem.inchi.MolToInchi(self.Mol, **kwargs)
            if format == 'inchikey':
                result = Chem.inchi.InchiToInchiKey(result, **kwargs)
        elif format == "png":
            size = size or (200, 200)
            mc = Chem.Mol(self.Mol.ToBinary())
            AllChem.Compute2DCoords(mc)
            if hasattr(rdMolDraw2D, 'MolDraw2DCairo'):
                drawer = rdMolDraw2D.MolDraw2DCairo(*size)
                drawer.DrawMolecule(mc)
                drawer.FinishDrawing()
                if filename:
                    with open(filename, 'w+') as f:
                        f.write(drawer.GetDrawingText())
                else:
                    return drawer.GetDrawingText()
            else:
                bio = BytesIO()
                img = Draw.MolToImage(mc, size=size)
                img.save(bio, format='PNG')
                if filename:
                    with open(filename, 'w+') as f:
                        f.write(bio.getvalue())
                else:
                    return bio.getvalue()
        elif format == "svg":
            size = size or (200, 200)
            mc = Chem.Mol(self.Mol.ToBinary())
            AllChem.Compute2DCoords(mc)
            drawer = rdMolDraw2D.MolDraw2DSVG(*size)
            drawer.DrawMolecule(mc)
            drawer.FinishDrawing()
            svg = drawer.GetDrawingText()
            if filename:
                with open(filename, 'w+') as f:
                    f.write(svg)
            else:
                return svg
        else:
            raise ValueError("%s is not a recognised RDKit format" % format)
        if filename:
            with open(filename, "w") as f:
                f.write(result)
        else:
            return result

    def __iter__(self):
        """Iterate over the Atoms of the Molecule.

        This allows constructions such as the following:
           for atom in mymol:
               print(atom)
        """
        return iter(self.atoms)

    def calcdesc(self, descnames=None):
        """Calculate descriptor values.

        Optional parameter:
           descnames -- a list of names of descriptors

        If descnames is not specified, all available descriptors are
        calculated. See the descs variable for a list of available
        descriptors.
        """
        descnames = descnames or descs
        ans = {}
        for descname in descnames:
            try:
                desc = _descDict[descname]
            except KeyError:
                raise ValueError("%s is not a recognised RDKit descriptor type" % descname)
            ans[descname] = desc(self.Mol)
        return ans

    def calcfp(self, fptype="rdkit", opt=None):
        """Calculate a molecular fingerprint.

        Optional parameters:
           fptype -- the fingerprint type (default is "rdkit"). See the
                     fps variable for a list of of available fingerprint
                     types.
           opt -- a dictionary of options for fingerprints. Currently only used
                  for radius and bitInfo in Morgan fingerprints.
        """
        if opt is None:
            opt = {}
        fptype = fptype.lower()
        if fptype == "rdkit":
            fp = Fingerprint(Chem.RDKFingerprint(self.Mol))
        elif fptype == "layered":
            fp = Fingerprint(Chem.LayeredFingerprint(self.Mol))
        elif fptype == "maccs":
            fp = Fingerprint(Chem.MACCSkeys.GenMACCSKeys(self.Mol))
        elif fptype == "atompairs":
            # Going to leave as-is. See Atom Pairs documentation.
            fp = Chem.AtomPairs.Pairs.GetAtomPairFingerprintAsIntVect(self.Mol)
        elif fptype == "torsions":
            # Going to leave as-is.
            fp = Chem.AtomPairs.Torsions.GetTopologicalTorsionFingerprintAsIntVect(self.Mol)
        elif fptype == "morgan":
            info = opt.get('bitInfo', None)
            radius = opt.get('radius', 4)
            fp = Fingerprint(Chem.rdMolDescriptors.GetMorganFingerprintAsBitVect(self.Mol, radius, bitInfo=info))
        elif fptype == "pharm2d":
            fp = Fingerprint(Generate.Gen2DFingerprint(self.Mol, Gobbi_Pharm2D.factory))
        else:
            raise ValueError("%s is not a recognised RDKit Fingerprint type" % fptype)
        return fp

    def localopt(self, forcefield="uff", steps=500):
        """Locally optimize the coordinates.

        Optional parameters:
           forcefield -- default is "uff". See the forcefields variable
                         for a list of available forcefields.
           steps -- default is 500

        If the molecule does not have any coordinates, make3D() is
        called before the optimization.
        """
        forcefield = forcefield.lower()
        if self.Mol.GetNumConformers() == 0:
            self.make3D(forcefield)
        _forcefields[forcefield](self.Mol, maxIters=steps)

    def make3D(self, forcefield="mmff94", steps=50):
        """Generate 3D coordinates.

        Optional parameters:
           forcefield -- default is "uff". See the forcefields variable
                         for a list of available forcefields.
           steps -- default is 50

        Once coordinates are generated, a quick
        local optimization is carried out with 50 steps and the
        UFF forcefield. Call localopt() if you want
        to improve the coordinates further.
        """
        forcefield = forcefield.lower()
        success = AllChem.EmbedMolecule(self.Mol,
                                        useExpTorsionAnglePrefs=True,
                                        useBasicKnowledge=True,
                                        enforceChirality=True,
                                        )
        if success == -1:
            raise Exception("Embedding failed!")

        self.localopt(forcefield, steps)
        self._clear_cache()

    def make2D(self):
        """Generate 2D coordinates for molecule"""
        AllChem.Compute2DCoords(self.Mol)
        self._clear_cache()

    def __getstate__(self):
        if self._source is None:
            state = {'Mol': self.Mol,
                     'source': None,
                     'data': dict([(k, self.Mol.GetProp(k)) for k in self.Mol.GetPropNames(includePrivate=True)]),
                     'dicts': {'atom_dict': self._atom_dict,
                               'ring_dict': self._ring_dict,
                               'res_dict': self._res_dict,
                               }
                     }
        else:
            state = {'Mol': None,
                     'source': self._source,
                     'data': {},
                     'dicts': {'atom_dict': None,
                               'ring_dict': None,
                               'res_dict': None,
                               }
                     }
        return state

    def __setstate__(self, state):
        Molecule.__init__(self, Mol=state['Mol'], source=state['source'])
        if state['data']:
            self.data.update(state['data'])
        self._atom_dict = state['dicts']['atom_dict']
        self._ring_dict = state['dicts']['ring_dict']
        self._res_dict = state['dicts']['res_dict']


class AtomStack(object):
    def __init__(self, Mol):
        self.Mol = Mol

    def __iter__(self):
        for i in range(self.Mol.GetNumAtoms()):
            yield Atom(self.Mol.GetAtomWithIdx(i))

    def __len__(self):
        return self.Mol.GetNumAtoms()

    def __getitem__(self, i):
        if 0 <= i < self.Mol.GetNumAtoms():
            return Atom(self.Mol.GetAtomWithIdx(int(i)))
        else:
            raise AttributeError("There is no atom with ID %i" % i)


class Atom(object):
    """Represent an rdkit Atom.

    Required parameters:
       Atom -- an RDKit Atom

    Attributes:
        atomicnum, coords, formalcharge

    The original RDKit Atom can be accessed using the attribute:
       Atom
    """

    def __init__(self, Atom):
        self.Atom = Atom

    @property
    def atomicnum(self):
        return self.Atom.GetAtomicNum()

    @property
    def coords(self):
        owningmol = self.Atom.GetOwningMol()
        if owningmol.GetNumConformers() == 0:
            return (0, 0, 0)
        idx = self.Atom.GetIdx()
        atomcoords = owningmol.GetConformer().GetAtomPosition(idx)
        return (atomcoords[0], atomcoords[1], atomcoords[2])

    @property
    def formalcharge(self):
        return self.Atom.GetFormalCharge()

    # ODDT #
    @property
    def idx(self):
        """ Note that this index is 1-based and RDKit's internal index in 0-based.
        Changed to be compatible with OpenBabel"""
        return self.Atom.GetIdx() + 1

    @property
    def neighbors(self):
        return [Atom(a) for a in self.Atom.GetNeighbors()]

    @property
    def bonds(self):
        return [Bond(b) for b in self.Atom.GetBonds()]

    @property
    def partialcharge(self):
        if self.Atom.HasProp('_TriposPartialCharge'):
            return float(self.Atom.GetProp('_TriposPartialCharge'))
        if not self.Atom.HasProp('_GasteigerCharge'):
            ComputeGasteigerCharges(self.Atom.GetOwningMol(), nIter=50)
        return float(self.Atom.GetProp('_GasteigerCharge').replace(',', '.'))

    def __str__(self):
        if hasattr(self, "coords"):
            return "Atom: %d (%.2f %.2f %.2f)" % (self.atomicnum,
                                                  self.coords[0],
                                                  self.coords[1],
                                                  self.coords[2])
        else:
            return "Atom: %d (no coords)" % (self.atomicnum)


class BondStack(object):
    def __init__(self, Mol):
        self.Mol = Mol

    def __iter__(self):
        for i in range(self.Mol.GetNumBonds()):
            yield Bond(self.Mol.GetBondWithIdx(i))

    def __len__(self):
        return self.Mol.GetNumBonds()

    def __getitem__(self, i):
        if 0 <= i < self.Mol.GetNumBonds():
            return Bond(self.Mol.GetBondWithIdx(i))
        else:
            raise AttributeError("There is no bond with Idx %i" % i)


class Bond(object):
    def __init__(self, Bond):
        self.Bond = Bond

    @property
    def order(self):
        return BOND_ORDERS[self.Bond.GetBondType()]

    @property
    def atoms(self):
        return (Atom(self.Bond.GetBeginAtom()), Atom(self.Bond.GetEndAtom()))

    @property
    def isrotor(self):
        if (not self.Bond.IsInRing() and
            self.Bond.Match(Chem.MolFromSmarts('[!$(*#*)&!D1&!$(C(F)(F)F)&'
                                               '!$(C(Cl)(Cl)Cl)&'
                                               '!$(C(Br)(Br)Br)&'
                                               '!$(C([CH3])([CH3])[CH3])&'
                                               '!$([CD3](=[N,O,S])-!@[#7,O,S!D1])&'
                                               '!$([#7,O,S!D1]-!@[CD3]=[N,O,S])&'
                                               '!$([CD3](=[N+])-!@[#7!D1])&'
                                               '!$([#7!D1]-!@[CD3]=[N+])]-!@[!$(*#*)&'
                                               '!D1&!$(C(F)(F)F)&'
                                               '!$(C(Cl)(Cl)Cl)&'
                                               '!$(C(Br)(Br)Br)&'
                                               '!$(C([CH3])([CH3])[CH3])]').GetBondWithIdx(0))):
            a1, a2 = self.atoms
            if a1.atomicnum > 1 and a2.atomicnum > 1:
                a1_n = sum(n.atomicnum > 1 for n in a1.neighbors)
                a2_n = sum(n.atomicnum > 1 for n in a2.neighbors)
                if a1_n > 1 and a2_n > 1:
                    return True
        return False


class Residue(object):
    """Represent a RDKit residue.

    Required parameter:
       ParentMol -- Parent molecule (Mol) object
       path -- atoms path of a residue

    Attributes:
       atoms, idx, name.

    (refer to the Open Babel library documentation for more info).

    The Mol object constucted of residues' atoms can be accessed using the attribute:
       Residue
    """

    def __init__(self, ParentMol, atom_path):
        self.ParentMol = ParentMol
        self.atom_path = tuple(map(int, atom_path))
        assert len(self.atom_path) > 0
        self.atommap = {}
        self.bonds = []
        for i, j in combinations(self.atom_path, 2):
            b = self.ParentMol.GetBondBetweenAtoms(i, j)
            if b:
                self.bonds.append(b.GetIdx())
        self.Residue = Chem.PathToSubmol(self.ParentMol, self.bonds, atomMap=self.atommap)
        self.MonomerInfo = self.ParentMol.GetAtomWithIdx(self.atom_path[0]).GetMonomerInfo()
        self.atommap = dict((v, k) for k, v in self.atommap.items())

    @property
    def atoms(self):
        if len(self.atom_path) == 1:
            return [Atom(self.ParentMol.GetAtomWithIdx(self.atom_path[0]))]
        else:
            return AtomStack(self.Residue)

    @property
    def idx(self):
        return self.MonomerInfo.GetResidueNumber() if self.MonomerInfo else 0

    @property
    def name(self):
        return self.MonomerInfo.GetResidueName() if self.MonomerInfo else 'UNL'

    def __iter__(self):
        """Iterate over the Atoms of the Residue.

        This allows constructions such as the following:
           for atom in residue:
               print(atom)
        """
        return iter(self.atoms)


class ResidueStack(object):
    def __init__(self, Mol, paths):
        self.Mol = Mol
        self.paths = paths

    def __iter__(self):
        for i in range(len(self.paths)):
            yield Residue(self.Mol, self.paths[i])

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        if 0 <= i < len(self.paths):
            return Residue(self.Mol, self.paths[i])
        else:
            raise AttributeError("There is no residue with ID %i" % i)


class Smarts(object):
    """A Smarts Pattern Matcher

    Required parameters:
       smartspattern

    Methods:
       findall(molecule)

    Example:
    >>> mol = readstring("smi","CCN(CC)CC") # triethylamine
    >>> smarts = Smarts("[#6][#6]") # Matches an ethyl group
    >>> print(smarts.findall(mol))
    [(0, 1), (3, 4), (5, 6)]

    The numbers returned are the indices (starting from 0) of the atoms
    that match the SMARTS pattern. In this case, there are three matches
    for each of the three ethyl groups in the molecule.
    """
    def __init__(self, smartspattern):
        """Initialise with a SMARTS pattern."""
        self.rdksmarts = Chem.MolFromSmarts(smartspattern)
        if not self.rdksmarts:
            raise IOError("Invalid SMARTS pattern.")

    def match(self, molecule):
        """Find all matches of the SMARTS pattern to a particular molecule.

        Required parameters:
           molecule
        """
        return molecule.Mol.HasSubstructMatch(self.rdksmarts)

    def findall(self, molecule):
        """Find all matches of the SMARTS pattern to a particular molecule.

        Required parameters:
           molecule
        """
        return molecule.Mol.GetSubstructMatches(self.rdksmarts)


class MoleculeData(object):
    """Store molecule data in a dictionary-type object

    Required parameters:
      Mol -- an RDKit Mol

    Methods and accessor methods are like those of a dictionary except
    that the data is retrieved on-the-fly from the underlying Mol.

    Example:
    >>> mol = next(readfile("sdf", 'head.sdf'))
    >>> data = mol.data
    >>> print(data)
    {'Comment': 'CORINA 2.61 0041  25.10.2001', 'NSC': '1'}
    >>> print(len(data), data.keys(), data.has_key("NSC"))
    2 ['Comment', 'NSC'] True
    >>> print(data['Comment'])
    CORINA 2.61 0041  25.10.2001
    >>> data['Comment'] = 'This is a new comment'
    >>> for k,v in data.items():
    ...    print(k, "-->", v)
    Comment --> This is a new comment
    NSC --> 1
    >>> del data['NSC']
    >>> print(len(data), data.keys(), data.has_key("NSC"))
    1 ['Comment'] False
    """
    def __init__(self, Mol):
        self._mol = Mol

    def _testforkey(self, key):
        if key not in self:
            raise KeyError("'%s'" % key)

    def keys(self):
        return self._mol.GetPropNames()

    def values(self):
        return [self._mol.GetProp(x) for x in self.keys()]

    def items(self):
        return zip(self.keys(), self.values())

    def __iter__(self):
        return iter(self.keys())

    def iteritems(self):
        return iter(self.items())

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key):
        return self._mol.HasProp(key)

    def __delitem__(self, key):
        self._testforkey(key)
        self._mol.ClearProp(key)

    def clear(self):
        for key in self:
            del self[key]

    def has_key(self, key):
        return key in self

    def update(self, dictionary):
        for k, v in dictionary.items():
            self[k] = v

    def __getitem__(self, key):
        self._testforkey(key)
        return self._mol.GetProp(key)

    def __setitem__(self, key, value):
        self._mol.SetProp(key, str(value))

    def to_dict(self):
        return self._mol.GetPropsAsDict()

    def __repr__(self):
        return self.to_dict().__repr__()


class Fingerprint(object):
    """A Molecular Fingerprint.

    Required parameters:
       fingerprint -- a vector calculated by one of the fingerprint methods

    Attributes:
       fp -- the underlying fingerprint object
       bits -- a list of bits set in the Fingerprint

    Methods:
       The "|" operator can be used to calculate the Tanimoto coeff. For example,
       given two Fingerprints 'a', and 'b', the Tanimoto coefficient is given by:
          tanimoto = a | b
    """
    def __init__(self, fingerprint):
        self.fp = fingerprint

    def __or__(self, other):
        return rdkit.DataStructs.FingerprintSimilarity(self.fp, other.fp)

    def __getattr__(self, attr):
        if attr == "bits":
            # Create a bits attribute on-the-fly
            return list(self.fp.GetOnBits())
        else:
            raise AttributeError("Fingerprint has no attribute %s" % attr)

    def __str__(self):
        return ", ".join([str(x) for x in _compressbits(self.fp)])

    @property
    def raw(self):
        return np.array(self.fp)


def _compressbits(bitvector, wordsize=32):
    """Compress binary vector into vector of long ints.

    This function is used by the Fingerprint class.

    >>> _compressbits([0, 1, 0, 0, 0, 1], 2)
    [2, 0, 2]
    """
    ans = []
    for start in range(0, len(bitvector), wordsize):
        compressed = 0
        for i in range(wordsize):
            if i + start < len(bitvector) and bitvector[i + start]:
                compressed += 2**i
        ans.append(compressed)

    return ans


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
