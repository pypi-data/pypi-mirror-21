#!/usr/bin/env python
'''
build American Mineralogist Crystal Structure Databse (amcsd)
'''

import os
import re
import requests

try:
    from cStringIO import StringIO #python 2
except:
    from io import StringIO #python 3

import numpy as np

from itertools import groupby

import larch
from larch_plugins.xrd import generate_hkl,peaklocater

from sqlalchemy import (create_engine,MetaData,
                        Table,Column,Integer,String,Unicode,
                        PrimaryKeyConstraint,ForeignKeyConstraint,ForeignKey,
                        Numeric,func,
                        and_,or_,not_,tuple_)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,mapper,clear_mappers,relationship
from sqlalchemy.pool import SingletonThreadPool


# needed for py2exe?
#import sqlalchemy.dialects.sqlite

HAS_CifFile = False
try:
    import CifFile
    HAS_CifFile = True
except ImportError:
    pass

HAS_XRAYUTIL = False
try:
    import xrayutilities as xu
    HAS_XRAYUTIL = True
except ImportError:
    pass


SYMMETRIES = ['triclinic',
              'monoclinic',
              'orthorhombic',
              'tetragonal',
              'trigonal',
              'hexagonal',
              'cubic']
ELEMENTS = [['1',  'Hydrogen',  'H'], ['2',  'Helium',  'He'], ['3',  'Lithium',  'Li'],
            ['4',  'Beryllium',  'Be'], ['5',  'Boron',  'B'], ['6',  'Carbon',  'C'],
            ['7',  'Nitrogen',  'N'], ['8',  'Oxygen',  'O'], ['9',  'Fluorine',  'F'],
            ['10',  'Neon',  'Ne'], ['11',  'Sodium',  'Na'], ['12',  'Magnesium',  'Mg'],
            ['13',  'Aluminum',  'Al'], ['14',  'Silicon',  'Si'], ['15',  'Phosphorus',  'P'],
            ['16',  'Sulfur',  'S'], ['17',  'Chlorine',  'Cl'], ['18',  'Argon',  'Ar'],
            ['19',  'Potassium',  'K'], ['20',  'Calcium',  'Ca'], ['21',  'Scandium',  'Sc'],
            ['22',  'Titanium',  'Ti'], ['23',  'Vanadium',  'V'], ['24',  'Chromium',  'Cr'],
            ['25',  'Manganese',  'Mn'], ['26',  'Iron',  'Fe'], ['27',  'Cobalt',  'Co'],
            ['28',  'Nickel',  'Ni'], ['29',  'Copper',  'Cu'], ['30',  'Zinc',  'Zn'],
            ['31',  'Gallium',  'Ga'], ['32',  'Germanium',  'Ge'], ['33',  'Arsenic',  'As'],
            ['34',  'Selenium',  'Se'], ['35',  'Bromine',  'Br'], ['36',  'Krypton',  'Kr'],
            ['37',  'Rubidium',  'Rb'], ['38',  'Strontium',  'Sr'], ['39',  'Yttrium',  'Y'],
            ['40',  'Zirconium',  'Zr'], ['41',  'Niobium',  'Nb'], ['42',  'Molybdenum',  'Mo'],
            ['43',  'Technetium',  'Tc'], ['44',  'Ruthenium',  'Ru'], ['45',  'Rhodium',  'Rh'],
            ['46',  'Palladium',  'Pd'], ['47',  'Silver',  'Ag'], ['48',  'Cadmium',  'Cd'],
            ['49',  'Indium',  'In'], ['50',  'Tin',  'Sn'], ['51',  'Antimony',  'Sb'],
            ['52',  'Tellurium',  'Te'], ['53',  'Iodine',  'I'], ['54',  'Xenon',  'Xe'],
            ['55',  'Cesium',  'Cs'], ['56',  'Barium',  'Ba'], ['57',  'Lanthanum',  'La'],
            ['58',  'Cerium',  'Ce'], ['59',  'Praseodymium',  'Pr'], ['60',  'Neodymium',  'Nd'],
            ['61',  'Promethium',  'Pm'], ['62',  'Samarium',  'Sm'], ['63',  'Europium',  'Eu'],
            ['64',  'Gadolinium',  'Gd'], ['65',  'Terbium',  'Tb'], ['66',  'Dysprosium',  'Dy'],
            ['67',  'Holmium',  'Ho'], ['68',  'Erbium',  'Er'], ['69',  'Thulium',  'Tm'],
            ['70',  'Ytterbium',  'Yb'], ['71',  'Lutetium',  'Lu'], ['72',  'Hafnium',  'Hf'],
            ['73',  'Tantalum',  'Ta'], ['74',  'Tungsten',  'W'], ['75',  'Rhenium',  'Re'],
            ['76',  'Osmium',  'Os'], ['77',  'Iridium',  'Ir'], ['78',  'Platinum',  'Pt'],
            ['79',  'Gold',  'Au'], ['80',  'Mercury',  'Hg'], ['81',  'Thallium',  'Tl'],
            ['82',  'Lead',  'Pb'], ['83',  'Bismuth',  'Bi'], ['84',  'Polonium',  'Po'],
            ['85',  'Astatine',  'At'], ['86',  'Radon',  'Rn'], ['87',  'Francium',  'Fr'],
            ['88',  'Radium',  'Ra'], ['89',  'Actinium',  'Ac'], ['90',  'Thorium',  'Th'],
            ['91',  'Protactinium',  'Pa'], ['92',  'Uranium',  'U'], ['93',  'Neptunium',  'Np'],
            ['94',  'Plutonium',  'Pu'], ['95',  'Americium',  'Am'], ['96',  'Curium',  'Cm'],
            ['97',  'Berkelium',  'Bk'], ['98',  'Californium',  'Cf'], ['99',  'Einsteinium',  'Es'],
            ['100',  'Fermium',  'Fm'], ['101',  'Mendelevium',  'Md'], ['102',  'Nobelium',  'No'],
            ['103',  'Lawrencium',  'Lr'], ['104',  'Rutherfordium',  'Rf'], ['105',  'Dubnium',  'Db'],
            ['106',  'Seaborgium',  'Sg'], ['107',  'Bohrium',  'Bh'], ['108',  'Hassium',  'Hs'],
            ['109',  'Meitnerium',  'Mt'], ['110',  'Darmstadtium',  'Ds'], ['111',  'Roentgenium',  'Rg'],
            ['112',  'Ununbium',  'Uub'], ['113',  'Ununtrium',  'Uut'], ['114',  'Ununquadium',  'Uuq'],
            ['115',  'Ununpentium',  'Uup'], ['116',  'Ununhexium',  'Uuh'], ['117',  'Ununseptium',  'Uus'],
            ['118',  'Ununoctium',  'Uuo']]
SPACEGROUPS = [['1', 'A 1'], ['1', 'B 1'], ['1', 'C 1'], ['1', 'A1'], ['1', 'B1'], ['1', 'C1'], ['1', 'F 1'], ['1', 'F1'], ['1', 'I 1'],
               ['2', 'A -1'], ['2', 'A-1'], ['2', 'B -1'], ['2', 'B-1'], ['2', 'C -1'], ['2', 'C-1'], ['2', 'F -1'], ['2', 'F-1'], ['2', 'I -1'], ['2', 'I-1'], ['2', 'P -1'], ['2', 'P 1'], ['2', 'P-1'], ['2', 'P1'],
               ['3', 'A 2 1 1'], ['3', 'B 1 2 1'], ['3', 'C 1 1 2'], ['3', 'P 1 1 2'], ['3', 'P 1 2 1'], ['3', 'P 2 1 1'], ['3', 'P2'],
               ['4', 'A 21 1 1'], ['4', 'B 1 21 1'], ['4', 'C 1 1 21'], ['4', 'P 1 1 21'], ['4', 'P 1 21 1'], ['4', 'P 21 1 1'], ['4', 'P21'],
               ['5', 'A 1 1 2'], ['5', 'A 1 2 1'], ['5', 'B 1 1 2'], ['5', 'B 2 1 1'], ['5', 'C 1 2 1'], ['5', 'C 2 1 1'], ['5', 'C2'], ['5', 'F 1 1 2'], ['5', 'F 1 2 1'], ['5', 'F 2 1 1'], ['5', 'I 1 1 2'], ['5', 'I 1 2 1'], ['5', 'I 2 1 1'],
               ['6', 'A m 1 1'], ['6', 'B 1 m 1'], ['6', 'C 1 1 m'], ['6', 'P 1 1 m'], ['6', 'P 1 m 1'], ['6', 'P m 1 1'], ['6', 'Pm'],
               ['7', 'A b 1 1'], ['7', 'A d 1 1'], ['7', 'B 1 a 1'], ['7', 'B 1 d 1'], ['7', 'C 1 1 a'], ['7', 'C 1 1 d'], ['7', 'P 1 1 a'], ['7', 'P 1 1 b'], ['7', 'P 1 1 n'], ['7', 'P 1 a 1'], ['7', 'P 1 c 1'], ['7', 'P 1 n 1'], ['7', 'P b 1 1'], ['7', 'P c 1 1'], ['7', 'P n 1 1'], ['7', 'Pc'],
               ['8', 'A 1 1 m'], ['8', 'A 1 m 1'], ['8', 'B 1 1 m'], ['8', 'B m 1 1'], ['8', 'C 1 m 1'], ['8', 'C m 1 1'], ['8', 'Cm'], ['8', 'F 1 1 m'], ['8', 'F 1 m 1'], ['8', 'F m 1 1'], ['8', 'I 1 1 m'], ['8', 'I 1 m 1'], ['8', 'I m 1 1'],
               ['9', 'A 1 1 a'], ['9', 'A 1 a 1'], ['9', 'B 1 1 b'], ['9', 'B b 1 1'], ['9', 'C 1 c 1'], ['9', 'C c 1 1'], ['9', 'Cc'], ['9', 'F 1 1 d'], ['9', 'F 1 d 1'], ['9', 'F d 1 1'], ['9', 'I 1 1 a'], ['9', 'I 1 a 1'], ['9', 'I b 1 1'], ['9', 'I 1 1 b'],
               ['10', 'A 2 / m 1 1'], ['10', 'B 1 2 / m 1'], ['10', 'C 1 1 2 / m'], ['10', 'P 1 1 2 / m'], ['10', 'P 1 2 / m 1'], ['10', 'P 2 / m 1 1'], ['10', 'P2/m'], ['10', 'P 1 2/m 1'], ['10', 'P 1 1 2/m'],
               ['11', 'A 21 / m 1 1'], ['11', 'B 1 21 / m 1'], ['11', 'C 1 1 21 / m'], ['11', 'P 1 1 21 / m'], ['11', 'P 1 21/m 1'], ['11', 'P 1 21 / m 1'], ['11', 'P 21 / m 1 1'], ['11', 'P21/m'], ['11', 'P 1 1 21/m'],
               ['12', 'A 1 1 2 / m'], ['12', 'A 1 2 / m 1'], ['12', 'B 1 1 2 / m'], ['12', 'B 1 1 2/m'], ['12', 'B 2 / m 1 1'], ['12', 'C 1 2 / m 1'], ['12', 'C 1 2/m 1'], ['12', 'C 2 / m 1 1'], ['12', 'C2/m'], ['12', 'F 1 1 2 / m'], ['12', 'F 1 2 / m 1'], ['12', 'F 2 / m 1 1'], ['12', 'I 1 1 2 / m'], ['12', 'I 1 2 / m 1'], ['12', 'I 2 / m 1 1'], ['12', 'I 1 2/m 1'], ['12', 'A 1 2/m 1'], ['12', 'C 2/m '], ['12', 'A 1 1 2/m'], ['12', 'F 1 2/m 1'],
               ['13', 'A 2 / b 1 1'], ['13', 'A 2 / d 1 1'], ['13', 'B 1 2 / a 1'],  ['13', 'B 1 2 / d 1'], ['13', 'C 1 1 2 / a'], ['13', 'C 1 1 2 / d'], ['13', 'P 1 1 2 / a'], ['13', 'P 1 1 2 / b'], ['13', 'P 1 1 2 / n'], ['13', 'P 1 1 2/b'], ['13', 'P 1 2 / a 1'], ['13', 'P 1 2 / c 1'], ['13', 'P 1 2 / n 1'], ['13', 'P 1 2/c 1'], ['13', 'P 2 / b 1 1'], ['13', 'P 2 / c 1 1'], ['13', 'P 2 / n 1 1'], ['13', 'P2/c'], ['13', 'P 1 2/n 1'], ['13', 'P 1 2/a 1'],
               ['14', 'A 21 / b 1 1'], ['14', 'A 21 / d 1 1'], ['14', 'B 1 21 / a 1'], ['14', 'B 1 21 / d 1'], ['14', 'C 1 1 21 / a'], ['14', 'C 1 1 21 / d'], ['14', 'P 1 1 21 / a'], ['14', 'P 1 1 21 / b'], ['14', 'P 1 1 21 / n'], ['14', 'P 1 1 21/b'], ['14', 'P 1 21 / a 1'], ['14', 'P 1 21 / c 1'], ['14', 'P 1 21 / n 1'], ['14', 'P 1 21/c 1'], ['14', 'P 21 / b 1 1'], ['14', 'P 21 / c 1 1'], ['14', 'P 21 / n 1 1'], ['14', 'P21/c'], ['14', 'P 1 21/a 1'], ['14', 'P 1 21/n 1'], ['14', 'P 21/b 1 1'], ['14', 'P 1 1 21/n'], ['14', 'B 1 21/d 1'], ['14', 'B 1 21/m 1'], ['14', 'P 21/n 1 1'], ['14', 'P 1 1 21/a'], ['14', 'P 21/c'], ['14', 'P 21/n'],
               ['15', 'A 1 1 2 / a'], ['15', 'A 1 2 / a 1'], ['15', 'B 1 1 2 / b'], ['15', 'B 1 1 2/b'], ['15', 'B 2 / b 1 1'], ['15', 'C 1 2 / c 1'], ['15', 'C 1 2/c 1'], ['15', 'C 2 / c 1 1'], ['15', 'C2/c'], ['15', 'F 1 1 2 / d'], ['15', 'F 1 2 / d 1'], ['15', 'F 2 / d 1 1'], ['15', 'I 1 2/a 1'], ['15', 'A 1 2/a 1'], ['15', 'I 1 1 2 / a'], ['15', 'I 1 2 / a 1'], ['15', 'I 2 / b 1 1'], ['15', 'C 1 1 2/a'], ['15', 'F 1 2/d 1'], ['15', 'I 1 2/c 1'], ['15', 'C 2/c'], ['15', 'I 1 1 2/b'], ['15', 'I 1 1 2/a'], ['15', 'B 1 1 2/n'], ['15', 'A 1 2/n 1'],
               ['16', 'P 2 2 2'], ['16', 'P222'],
               ['17', 'P 2 2 21'], ['17', 'P 2 21 2'], ['17', 'P 21 2 2'], ['17', 'P222_1'], ['17', 'P2221'],
               ['18', 'P 2 21 21'], ['18', 'P 21 2 21'], ['18', 'P 21 21 2'], ['118', 'P2_12_12'], ['18', 'P2_122_1'], ['18', 'P21212'], ['18', 'P22_12_1'],
               ['19', 'P 21 21 2 1'], ['19', 'P 21 21 21'], ['19', 'P2_12_12_1'], ['19', 'P212121'],
               ['20', 'A 21 2 2'], ['20', 'A2_122'], ['20', 'B 2 21 2'], ['20', 'C 2 2 21'], ['20', 'C222_1'], ['20', 'C2221'],
               ['21', 'A 2 2 2'], ['21', 'B 2 2 2'], ['21', 'C 2 2 2'], ['21', 'C222'],
               ['22', 'F 2 2 2'], ['22', 'F222'],
               ['23', 'I 2 2 2'], ['23', 'I222'],
               ['24', 'I 21 21 2 1'], ['24', 'I 21 21 21'], ['24', 'I2_12_12_1'], ['24', 'I212121'],
               ['25', 'P 2 m m'], ['25', 'P m 2 m'], ['25', 'P m m 2'], ['25', 'P2mm'], ['25', 'Pm2m'], ['25', 'Pmm2'],
               ['26', 'P 21 a m'], ['26', 'P 21 m a'], ['26', 'P b 21 m'], ['26', 'P c m 21'], ['26', 'P m 21 b'], ['26', 'P m c 21'], ['26', 'P2_1am'], ['26', 'P2_1ma'], ['26', 'Pb2_1m'], ['26', 'Pcm2_1'], ['26', 'Pmc2_1'], ['26', 'Pmc21'],
               ['27', 'P 2 a a'], ['27', 'P b 2 b'], ['27', 'P c c 2'], ['27', 'Pcc2'],
               ['28', 'P 2 c m'], ['28', 'P 2 m b'], ['28', 'P b m 2'], ['28', 'P c 2 m'], ['28', 'P m 2 a'], ['28', 'P m a 2'], ['28', 'P2cm'], ['28', 'Pbm2'], ['28', 'Pma2'],
               ['29', 'P 21 a b'], ['29', 'P 21 c a'], ['29', 'P b 21 a'], ['29', 'P b c 21'], ['29', 'P c 21 b'], ['29', 'P c a 21'], ['29', 'P2_1ab'], ['29', 'P2_1ca'], ['29', 'Pbc2_1'], ['29', 'Pc2_1b'], ['29', 'Pca2_1'], ['29', 'Pca21'],
               ['30', 'P 2 a n'], ['30', 'P 2 n a'], ['30', 'P b 2 n'], ['30', 'P c n 2'], ['30', 'P n 2 b'], ['30', 'P n c 2'], ['30', 'P2an'], ['30', 'Pnc2'],
               ['31', 'P 21 m n'], ['31', 'P 21 n m'], ['31', 'P m 21 n'], ['31', 'P m n 21'], ['31', 'P n 21 m'], ['31', 'P n m 21'], ['31', 'P2_1mn'], ['31', 'P2_1nm'], ['31', 'Pmn2_1'], ['31', 'Pmn21'], ['31', 'Pn2_1m'], ['31', 'Pnm2_1'],
               ['32', 'P 2 c b'], ['32', 'P b a 2'], ['32', 'P c 2 a'], ['32', 'Pba2'],
               ['33', 'P 21 c n'], ['33', 'P 21 n b'], ['33', 'P b n 21'], ['33', 'P c 21 n'], ['33', 'P n 21 a'], ['33', 'P n a 21'], ['33', 'P2_1cn'], ['33', 'P2_1nb'], ['33', 'Pbn2_1'], ['33', 'Pc2_1n'], ['33', 'Pn2_1a'], ['33', 'Pna21'],
               ['34', 'P 2 n n'], ['34', 'P n 2 n'], ['34', 'P n n 2'], ['34', 'P2nn'], ['34', 'Pn2n'], ['34', 'Pnn2'],
               ['35', 'A 2 m m'], ['35', 'A2mm'], ['35', 'B m 2 m'], ['35', 'Bm2m'], ['35', 'C m m 2'], ['35', 'Cmm2'],
               ['36', 'A 21 a m'], ['36', 'A 21 m a'], ['36', 'A2_1am'], ['36', 'A2_1ma'], ['36', 'B b 21 m'], ['36', 'B m 21 b'], ['36', 'Bb2_1m'], ['36', 'C c m 21'], ['36', 'C m c 21'], ['36', 'Ccm2_1'], ['36', 'Cmc2_1'], ['36', 'Cmc21'],
               ['37', 'A 2 a a'], ['37', 'B b 2 b'], ['37', 'C c c 2'], ['37', 'Ccc2'],
               ['38', 'A m 2 m'], ['38', 'A m m 2'], ['38', 'Amm2'], ['38', 'B 2 m m'], ['38', 'B m m 2'], ['38', 'C 2 m m'], ['38', 'C m 2 m'],
               ['39', 'A b 2 m'], ['39', 'A b m 2'], ['39', 'Abm2'], ['39', 'Aem2'], ['39', 'B 2 a m'], ['39', 'B m a 2'], ['39', 'C 2 m a'], ['39', 'C m 2 a'], ['39', 'Cm2a'],
               ['40', 'A m 2 a'], ['40', 'A m a 2'], ['40', 'Ama2'], ['40', 'B 2 m b'], ['40', 'B b m 2'], ['40', 'B2mb'], ['40', 'C 2 c m'], ['40', 'C c 2 m'],
               ['41', 'A b 2 a'], ['41', 'A b a 2'], ['41', 'Aba2'], ['41', 'Aea2'], ['41', 'B 2 a b'], ['41', 'B b a 2'], ['41', 'Bba2'], ['41', 'C 2 c a'], ['41', 'C c 2 a'], ['41', 'C 2 c b'],
               ['42', 'F m m 2'], ['42', 'Fmm2'], ['42', 'F m 2 m'],
               ['43', 'F 2 d d'], ['43', 'F d 2 d'], ['43', 'F d d 2'], ['43', 'F dd2'], ['43', 'F2dd'], ['43', 'Fd2d'], ['43', 'Fdd2'],
               ['44', 'I m m 2'], ['44', 'Imm2'], ['44', 'I 2 m m'], ['44', 'I m 2 m'],
               ['45', 'I 2 a a'], ['45', 'I b 2 a'], ['45', 'I b a 2'], ['45', 'Iba2'],
               ['46', 'I 2 a m'], ['46', 'I 2 m a'], ['46', 'I b 2 m'], ['46', 'I b m 2'], ['46', 'I m 2 a'], ['46', 'I m a 2'], ['46', 'Ibm2'], ['46', 'Ima2'], ['46', 'I 2 m b'], ['46', 'I 2 c m'],
               ['47', 'P 2/m 2/m 2/m'], ['47', 'P m m m'], ['47', 'Pmmm'],
               ['48', 'P 2/n 2/n 2/n'], ['48', 'P n n n'], ['48', 'Pnnn'],
               ['49', 'P 2/c 2/c 2/m'], ['49', 'P b m b'], ['49', 'P c c m'], ['49', 'P m a a'], ['49', 'Pccm'],
               ['50', 'P 2/b 2/a 2/n'], ['50', 'P b a n'], ['50', 'P c n a'], ['50', 'P n c b'], ['50', 'Pban'], ['50', 'Pncb'],
               ['51', 'P 21/m 2/m 2/a'], ['51', 'P b m m'], ['51', 'P c m m'], ['51', 'P m a m'], ['51', 'P m c m'], ['51', 'P m m a'], ['51', 'P m m b'], ['51', 'Pbmm'], ['51', 'Pmam'], ['51', 'Pmma'],
               ['52', 'P 2/n 21/n 2/a'], ['52', 'P b n n'], ['52', 'P c n n'], ['52', 'P n a n'], ['52', 'P n c n'], ['52', 'P n n a'], ['52', 'P n n b'], ['52', 'Pbnn'], ['52', 'Pcnn'], ['52', 'Pnan'], ['52', 'Pncn'], ['52', 'Pnna'],
               ['53', 'P 2/m 2/n 21/a'], ['53', 'P b m n'], ['53', 'P c n m'], ['53', 'P m a n'], ['53', 'P m n a'], ['53', 'P n c m'], ['53', 'P n m b'], ['53', 'Pbmn'], ['53', 'Pbnm'], ['53', 'Pman'], ['53', 'Pmna'], ['53', 'Pncm'], ['53', 'Pnmb'], ['54', 'P 21/c 2/c 2/a'],
               ['54', 'P b a a'], ['54', 'P b a b'], ['54', 'P b c b'], ['54', 'P c a a'], ['54', 'P c c a'], ['54', 'P c c b'], ['54', 'Pbaa'], ['54', 'Pbcb'], ['54', 'Pcca'],
               ['55', 'P 21/b 21/a 2/m'], ['55', 'P b a m'], ['55', 'P c m a'], ['55', 'P m c b'], ['55', 'Pbam'], ['55', 'Pmcb'],
               ['56', 'P 21/c 21/c 2/n'], ['56', 'P b n b'], ['56', 'P c c n'], ['56', 'P n a a'], ['56', 'Pbnb'], ['56', 'Pccn'], ['56', 'Pnaa'],
               ['57', 'P 2/b 21/c 21/m'], ['57', 'P b c m'], ['57', 'P b m a'], ['57', 'P c a m'], ['57', 'P c m b'], ['57', 'P m a b'], ['57', 'P m c a'], ['57', 'Pbcm'], ['57', 'Pbma'], ['57', 'Pcam'], ['57', 'Pcmb'], ['57', 'Pmab'],
               ['58', 'P 21/n 21/n 2/m'], ['58', 'P m n n'], ['58', 'P n m n'], ['58', 'P n n m'], ['58', 'Pmnn'], ['58', 'Pnmn'], ['58', 'Pnnm'],
               ['59', 'P 21/m 21/m 2/n'], ['59', 'P m m n'], ['59', 'P m n m'], ['59', 'P n m m'], ['59', 'Pmmn'], ['59', 'Pmnm'], ['59', 'Pnmm'],
               ['60', 'P 21/b 2/c 21/n'], ['60', 'P b c n'], ['60', 'P b n a'], ['60', 'P c a n'], ['60', 'P c n b'], ['60', 'P n a b'], ['60', 'P n c a'], ['60', 'Pbcn'], ['60', 'Pbna'], ['60', 'Pcan'], ['60', 'Pcnb'], ['60', 'Pnab'], ['60', 'Pnca'],
               ['61', 'P 21/b 21/c 21/a'], ['61', 'P b c a'], ['61', 'P c a b'], ['61', 'Pbca'],['61', 'Pcab'],
               ['62', 'P 21/n 21/m 21/a'], ['62', 'P b n m'], ['62', 'P c m n'], ['62', 'P m c n'], ['62', 'P m n b'], ['62', 'P n a m'], ['62', 'P n m a'], ['62', 'Pcmn'], ['62', 'Pmcn'], ['62', 'Pmnb'], ['62', 'Pnam'], ['62', 'Pnma'], ['62', 'P 1 n m a 1'], ['62', 'P 1 n a m 1'],
               ['63', 'A m a m'], ['63', 'A m m a'], ['63', 'Amam'], ['63', 'Amma'], ['63', 'B b m m'], ['63', 'B m m b'], ['63', 'Bbmm'], ['63', 'Bmmb'], ['63', 'C 2/m 2/c 21/m'], ['63', 'C c m m'], ['63', 'C m c m'], ['63', 'Ccmm'], ['63', 'Cmcm'],
               ['64', 'A b a m'], ['64', 'A b m a'], ['64', 'Abma'], ['64', 'B b a m'], ['64', 'B m a b'], ['64', 'Bbam'], ['64', 'Bmab'], ['64', 'C 2/m 2/c 21/a'], ['64', 'C c m a'], ['64', 'C m c a'], ['64', 'Cmca'], ['64', 'Cmce'], ['64', 'B b c m'], ['64', 'A c a m'], ['64', 'C c m b'],
               ['65', 'C 2/m 2/m 2/m'], ['65', 'C m m m'], ['65', 'Cmmm'], ['65', 'A m m m'],
               ['66', 'A m a a'], ['66', 'Amaa'], ['66', 'B b m b'], ['66', 'C 2/c 2/c 2/m'], ['66', 'C c c m'], ['66', 'Cccm'],
               ['67', 'A b m m'], ['67', 'Abmm'], ['67', 'B m a m'], ['67', 'Bmam'], ['67', 'C 2/m 2/m 2/e'], ['67', 'C m m a'], ['67', 'Cmma'], ['67', 'Cmme'], ['67', 'A c m m'],
               ['68', 'A b a a'], ['68', 'B b a b'], ['68', 'C 2/c 2/c 2/e'], ['68', 'C c c a'], ['68', 'Ccca'], ['68', 'Ccce'],
               ['69', 'F 2/m 2/m 2/m'], ['69', 'F m m m'], ['69', 'Fmmm'],
               ['70', 'F 2/d 2/d 2/d'], ['70', 'F d d d'], ['70', 'Fddd'],
               ['71', 'I 2/m 2/m 2/m'], ['71', 'I m m m'], ['71', 'Immm'],
               ['72', 'I 2/b 2/a 2/m'], ['72', 'I b a m'], ['72', 'I b m a'], ['72', 'I m a a'], ['72', 'Ibam'], ['72', 'I m c b'], ['72', 'I c m a'], ['72', 'I m a b'],
               ['73', 'I 2/b 2/c 2/a'], ['73', 'I b c a'], ['73', 'Ibca'],
               ['74', 'I 2/m 2/m 2/a'], ['74', 'I b m m'], ['74', 'I m a m'], ['74', 'I m m a'], ['74', 'Ibmm'], ['74', 'Imam'], ['74', 'Imma'], ['74', 'I m c m'], ['74','I 1 m m a 1'],
               ['75', 'C 4'], ['75', 'P 4'], ['75', 'P4'],
               ['76', 'C 41'], ['76', 'P 41'], ['76', 'P4_1'], ['76', 'P41'],
               ['77', 'C 42'], ['77', 'P 42'], ['77', 'P4_2'], ['77', 'P42'],
               ['78', 'C 43'], ['78', 'P 43'], ['78', 'P4_3'], ['78', 'P43'],
               ['79', 'F 4'], ['79', 'I 4'], ['79', 'I4'],
               ['80', 'F 41'], ['80', 'I 41'], ['80', 'I41'],
               ['81', 'C -4'], ['81', 'P -4'], ['81', 'P-4'],
               ['82', 'F -4'], ['82', 'I -4'], ['82', 'I-4'],
               ['83', 'C 4 / m'], ['83', 'P 4 / m'], ['83', 'P 4/m'], ['83', 'P4/m'],
               ['84', 'C 42 / m'], ['84', 'P 42 / m'], ['84', 'P 42/m'], ['84', 'P4_2/m'], ['84', 'P42/m'],
               ['85', 'C 4 / a'], ['85', 'P 4 / n'], ['85', 'P 4/n'], ['85', 'P4/n'],
               ['86', 'C 42 / a'], ['86', 'P 42 / n'], ['86', 'P 42/n'], ['86', 'P4_2/n'], ['86', 'P42/n'],
               ['87', 'F 4 / m'], ['87', 'I 4 / m'], ['87', 'I 4/m'], ['87', 'I4/m'],
               ['88', 'F 41 / d'], ['88', 'I 41 / a'], ['88', 'I 41/a'], ['88', 'I4_1/a'], ['88', 'I41/a'],
               ['89', 'C 4 2 2'], ['89', 'P 4 2 2'], ['89', 'P422'],
               ['90', 'C 4 2 21'], ['90', 'P 4 21 2'], ['90', 'P4212'],
               ['91', 'C 41 2 2'], ['91', 'P 41 2 2'], ['91', 'P4_122'], ['91', 'P4122'],
               ['92', 'C 41 2 21'], ['92', 'P 41 21 2'], ['92', 'P4_12_12'], ['92', 'P41212'],
               ['93', 'C 42 2 2'], ['93', 'P 42 2 2'], ['93', 'P4222'],
               ['94', 'C 42 2 21'], ['94', 'P 42 21 2'], ['94', 'P42212'],
               ['95', 'C 43 2 2'], ['95', 'P 43 2 2'], ['95', 'P4_322'], ['95', 'P4322'],
               ['96', 'C 43 2 21'], ['96', 'P 43 21 2'], ['96', 'P4_32_12'], ['96', 'P43212'],
               ['97', 'F 4 2 2'], ['97', 'I 4 2 2'], ['97', 'I422'],
               ['98', 'F 41 2 2'], ['98', 'I 41 2 2'], ['98', 'I4_122'], ['98', 'I4122'],
               ['99', 'C 4 m m'], ['99', 'P 4 m m'], ['99', 'P4mm'],
               ['100', 'C 4 m b'], ['100', 'P 4 b m'], ['100', 'P4bm'],
               ['101', 'C 42 m c'], ['101', 'P 42 c m'], ['101', 'P42cm'],
               ['102', 'C 42 m n'], ['102', 'P 42 n m'], ['102', 'P4_2nm'], ['102', 'P42nm'],
               ['103', 'C 4 c c'], ['103', 'P 4 c c'], ['103', 'P4cc'],
               ['104', 'C 4 c n'], ['104', 'P 4 n c'], ['104', 'P4nc'],
               ['105', 'C 42 c m'], ['105', 'P 42 m c'], ['105', 'P4_2mc'], ['105', 'P42mc'],
               ['106', 'C 42 c b'], ['106', 'P 42 b c'], ['106', 'P42bc'],
               ['107', 'F 4 m m'], ['107', 'I 4 m m'], ['107', 'I4mm'],
               ['108', 'F 4 m c'], ['108', 'I 4 c m'], ['108', 'I4cm'],
               ['109', 'F 41 d m'], ['109', 'I 41 m d'], ['109', 'I41md'],
               ['110', 'F 41 d c'], ['110', 'I 41 c d'], ['110', 'I4_1cd'], ['110', 'I41cd'],
               ['111', 'C -4 m 2'], ['111', 'P -4 2 m'], ['111', 'P-42m'], ['111', 'P42m'],
               ['112', 'C -4 c 2'], ['112', 'P -4 2 c'], ['112', 'P-42c'], ['112', 'P42c'],
               ['113', 'C -4 m 21'], ['113', 'P -4 21 m'], ['113', 'P421m'],
               ['114', 'C -4 c 21'], ['114', 'P -4 21 c'], ['114', 'P421c'],
               ['115', 'C -4 2 m'], ['115', 'P -4 m 2'], ['115', 'P-4m2'], ['115', 'P4m2'],
               ['116', 'C -4 2 c'], ['116', 'P -4 c 2'], ['116', 'P4c2'],
               ['117', 'C -4 2 b'], ['117', 'C-42b'], ['117', 'P -4 b 2'], ['117', 'P-4b2'], ['117', 'P4b2'],
               ['118', 'C -4 2 n'], ['118', 'P -4 n 2'], ['118', 'P-4n2'], ['118', 'P4n2'],
               ['119', 'F -4 2 m'], ['119', 'I -4 m 2'], ['119', 'I-4m2'], ['119', 'I4m2'],
               ['120', 'F -4 2 c'], ['120', 'I -4 c 2'], ['120', 'I-4c2'], ['120', 'I4c2'],
               ['121', 'F -4 m 2'], ['121', 'I -4 2 m'], ['121', 'I-42m'], ['121', 'I42m'],
               ['122', 'F -4 d 2'], ['122', 'F-4d2'], ['122', 'I -4 2 d'], ['122', 'I-42d'], ['122', 'I42d'],
               ['123', 'C 4 / m m m'], ['123', 'P 4 / m m m'], ['123', 'P 4/m 2/m 2/m'], ['123', 'P4/mmm'], ['123', 'P 4/m m m'],
               ['124', 'C 4 / m c c'], ['124', 'P 4 / m c c'], ['124', 'P 4/m 2/c 2/c'], ['124', 'P4/mcc'], ['124', 'P 4/m c c'],
               ['125', 'C 4 / a m b'], ['125', 'P 4 / n b m'], ['125', 'P 4/n 2/b 2/m'], ['125', 'P4/nbm'], ['125', 'P 4/n b m'],
               ['126', 'C 4 / a c n'], ['126', 'P 4 / n n c'], ['126', 'P 4/n 2/n 2/c'], ['126', 'P4/nnc'], ['126', 'P 4/n n c'],
               ['127', 'C 4 / m m b'], ['127', 'P 4 / m b m'], ['127', 'P 4/m 21/b 2/m'], ['127', 'P4/mbm'], ['127', 'P 4/m b m'],
               ['128', 'C 4 / m c n'], ['128', 'P 4 / m n c'], ['128', 'P 4/m 21/n 2/c'], ['128', 'P4/mnc'], ['128', 'P 4/m n c'],
               ['129', 'C 4 / a m m'], ['129', 'P 4 / n m m'], ['129', 'P 4/n 21/m 2/m'], ['129', 'P4/nmm'], ['129', 'P 4/n m m'],
               ['130', 'C 4 / a c c'], ['130', 'P 4 / n c c'], ['130', 'P 4/n c c'], ['130', 'P 4/n 21/c 2/c'], ['130', 'P4/ncc'],
               ['131', 'C 42 / m c m'], ['131', 'P 42 / m m c'], ['131', 'P 42/m 2/m 2/c'], ['131', 'P4_2/mmc'], ['131', 'P42/mmc'], ['131', 'P 42/m m c'],
               ['132', 'C 42 / m m c'], ['132', 'P 42 / m c m'], ['132', 'P 42/m 2/c 2/m'], ['132', 'P4_2/mcm'], ['132', 'P42/mcm'],
               ['133', 'C 42 / a c b'], ['133', 'P 42 / n b c'], ['133', 'P 42/n 2/b 2/c'], ['133', 'P4_2/nbc'], ['133', 'P42/nbc'], ['133', 'P 42/n b c'],
               ['134', 'C 42 / a n m'], ['134', 'P 42 / n n m'], ['134', 'P 42/n 2/n 2/m'], ['134', 'P4_2/nnm'], ['134', 'P42/nnm'], ['134', 'P 42/n n m'],
               ['135', 'C 42 / m c b'], ['135', 'P 42 / m b c'], ['135', 'P 42/m 21/b 2/c'], ['135', 'P4_2/mbc'], ['135', 'P42/mbc'], ['135', 'P 42/m b c'],
               ['136', 'C 42 / m m n'], ['136', 'P 42 / m n m'], ['136', 'P 42/m n m'], ['136', 'P 42/m 21/n 2/m'], ['136', 'P4_2/mnm'], ['136', 'P42/mnm'],
               ['137', 'C 42 / a c m'], ['137', 'P 42 / n m c'], ['137', 'P 42/n 21/m 2/c'], ['137', 'P4_2/nmc'], ['137', 'P42/nmc'], ['137', 'P 42/n m c'],
               ['138', 'C 42 / a m c'], ['138', 'P 42 / n c m'], ['138', 'P 42/n 21/c 2/m'], ['138', 'P4_2/ncm'], ['138', 'P42/ncm'], ['138', 'P 42/n c m'],
               ['139', 'F 4 / m m m'], ['139', 'F4/mmm'], ['139', 'I 4 / m m m'], ['139', 'I 4/m 2/m 2/m'], ['139', 'I4/mmm'], ['139', 'I 4/m m m'], ['139', 'F 4/m m m'],
               ['140', 'F 4 / m m c'], ['140', 'I 4 / m c m'], ['140', 'I 4/m 2/c 2/m'], ['140', 'I4/mcm'], ['140', 'I 4/m c m'], 
               ['141', 'F 41 / d d m'], ['141', 'I 41 / a m d'], ['141', 'I 41/a 2/m 2/d'],['141', 'I4_1/amd'], ['141', 'I41/amd'], ['141', 'I 41/a m d'],
               ['142', 'F 41 / d d c'], ['142', 'I 41 / a c d'], ['142', 'I 41/a c d'], ['142', 'I 41/a 2/c 2/d'], ['142', 'I4_1/acd'], ['142', 'I41/acd'],
               ['143', 'H 3'], ['143', 'P 3'], ['143', 'P3'],
               ['144', 'H 31'], ['144', 'P 31'], ['144', 'P3_1'], ['144', 'P31'],
               ['145', 'H 32'], ['145', 'P 32'], ['145', 'P3_2'], ['145', 'P32'],
               ['146', 'R 3'], ['146', 'R3'],
               ['147', 'H -3'], ['147', 'P -3'], ['147', 'P-3'],
               ['148', 'R -3'], ['148', 'R-3'],
               ['149', 'H 3 2 1'], ['149', 'P 3 1 2'], ['149', 'P312'],
               ['150', 'H 3 1 2'], ['150', 'P 3 2 1'],
               ['151', 'H 31 2 1'], ['151', 'P 31 1 2'], ['151', 'P3_112'], ['151', 'P3112'],
               ['152', 'H 31 1 2'], ['152', 'P 31 2 1'], ['152', 'P3_121'], ['152', 'P3121'],
               ['153', 'H 32 2 1'], ['153', 'P 32 1 2'], ['153', 'P3_212'], ['153', 'P3212'],
               ['154', 'H 32 1 2'], ['154', 'P 32 2 1'], ['154', 'P3_221'], ['154', 'P3221'],
               ['155', 'R 3 2'], ['155', 'R32'],
               ['156', 'H 3 1 m'], ['156', 'P 3 m 1'], ['156', 'P3m1'],
               ['157', 'H 3 m 1'], ['157', 'P 3 1 m'], ['157', 'P31m'],
               ['158', 'H 3 1 c'], ['158', 'P 3 c 1'], ['158', 'P3c1'],
               ['159', 'H 3 c 1'], ['159', 'P 3 1 c'], ['159', 'P31c'],
               ['160', 'R 3 m'], ['160', 'R3m'],
               ['161', 'R 3 c'], ['161', 'R3c'],
               ['162', 'H -3 m 1'], ['162', 'P -3 1 m'], ['162', 'P-31m'],
               ['163', 'H -3 c 1'], ['163', 'P -3 1 c'], ['163', 'P-31c'],
               ['164', 'H -3 1 m'], ['164', 'P -3 m 1'], ['164', 'P-3m1'],
               ['165', 'H -3 1 c'], ['165', 'P -3 c 1'], ['165', 'P-3c1'],
               ['166', 'R -3 m'], ['166', 'R-3m'],
               ['167', 'R -3 c'], ['167', 'R-3c'], ['167', 'R -3 2/c'],
               ['168', 'P 6'], ['168', 'P6'],
               ['169', 'P 61'], ['169', 'P6_1'], ['169', 'P61'],
               ['170', 'P 65'], ['170', 'P6_5'], ['170', 'P65'],
               ['171', 'P 62'], ['171', 'P62'],
               ['172', 'P 64'], ['172', 'P64'],
               ['173', 'P 63'], ['173', 'P6_3'], ['173', 'P63'],
               ['174', 'P -6'], ['174', 'P-6'],
               ['175', 'P 6 / m'], ['175', 'P 6/m'], ['175', 'P6/m'],
               ['176', 'P 63 / m'], ['176', 'P 63/m'], ['176', 'P6_3/m'], ['176', 'P63/m'],
               ['177', 'P 6 2 2'], ['177', 'P622'],
               ['178', 'P 61 2 2'], ['178', 'P6122'],
               ['179', 'P 65 2 2'], ['179', 'P6_522'], ['179', 'P6522'],
               ['180', 'P 62 2 2'], ['180', 'P6_222'], ['180', 'P6222'],
               ['181', 'P 64 2 2'], ['181', 'P6_422'], ['181', 'P6422'],
               ['182', 'P 63 2 2'], ['182', 'P6_322'], ['182', 'P6322'],
               ['183', 'P 6 m m'], ['183', 'P6mm'],
               ['184', 'P 6 c c'], ['184', 'P6cc'],
               ['185', 'P 63 c m'], ['185', 'P6_3cm'], ['185', 'P63cm'],
               ['186', 'P 63 m c'], ['186', 'P6_3mc'], ['186', 'P63mc'],
               ['187', 'P -6 m 2'], ['187', 'P-6m2'], ['187', 'P6m2'],
               ['188', 'P -6 c 2'], ['188', 'P-6c2'], ['188', 'P6c2'],
               ['189', 'P -6 2 m'], ['189', 'P-62m'], ['189', 'P62m'],
               ['190', 'P -6 2 c'], ['190', 'P-62c'], ['190', 'P62c'],
               ['191', 'P 6 / m m m'], ['191', 'P 6/m 2/m 2/m'], ['191', 'P6/mmm'], ['191', 'P 6/m m m '],
               ['192', 'P 6 / m c c'], ['192', 'P 6/m c c'], ['192', 'P 6/m 2/c 2/c'], ['192', 'P6/mcc'],
               ['193', 'P 63 / m c m'], ['193', 'P 63/m 2/c 2/m'], ['193', 'P6_3/mcm'], ['193', 'P63/mcm'], ['63', 'P 63/m c m'],
               ['194', 'P 63/m m c'], ['194', 'P 63 / m m c'], ['194', 'P 63/m 2/m 2/c'], ['194', 'P6_3/mmc'], ['194', 'P63/mmc'],
               ['195', 'P 2 3'], ['195', 'P23'],
               ['196', 'F 2 3'], ['196', 'F23'],
               ['197', 'I 2 3'], ['197', 'I23'],
               ['198', 'P2_13'], ['198', 'P213'], ['198', 'P 21 3'],
               ['199', 'I2_13'], ['199', 'I 21 3'],
               ['200', 'P m -3'], ['203', 'P m 3'],
               ['201', 'P n -3'], ['201', 'Pn3'], ['201', 'P n 3'],
               ['202', 'F m -3'], ['202', 'Fm3'], ['202', 'F m 3'],
               ['203', 'F d -3'], ['203', 'Fd3'], ['203', 'F d 3'],
               ['204', 'I m -3'], ['204', 'Im3'], ['204', 'I m 3'],
               ['205', 'P a -3'], ['205', 'P a 3'], ['205', 'Pa3'],
               ['206', 'I a -3'], ['206', 'Ia3'], ['206', 'I a 3'],
               ['207', 'P 4 3 2'], ['207', 'P432'],
               ['208', 'P 42 3 2'], ['208', 'P4_232'], ['208', 'P4232'],
               ['209', 'F 4 3 2'], ['209', 'F432'],
               ['210', 'F 41 3 2'], ['210', 'F4132'],
               ['211', 'I 4 3 2'], ['211', 'I432'], ['211', 'Pm-3m'],
               ['212', 'P 43 3 2'], ['212', 'P4_332'], ['212', 'P4332'],
               ['213', 'P 41 3 2'], ['213', 'P4_132'], ['213', 'P4132'],
               ['214', 'I 41 3 2'], ['214', 'I4_132'], ['214', 'I4132'],
               ['215', 'P -4 3 m'], ['215', 'P-43m'], ['215', 'P43m'],
               ['216', 'F -4 3 m'], ['216', 'F-43m'], ['216', 'F43m'],
               ['217', 'I -4 3 m'], ['217', 'I-43m'], ['217', 'I43m'],
               ['218', 'P -4 3 n'], ['218', 'P-43n'], ['218', 'P43n'],
               ['219', 'F -4 3 c'], ['219', 'F-43c'], ['219', 'F43c'],
               ['220', 'I -4 3 d'], ['220', 'I-43d'], ['220', 'I43d'],
               ['221', 'P m -3 m'], ['221', 'P m 3 m'], ['221', 'Pm3m'], ['221', 'P 4/m -3 2/m'],
               ['222', 'P n -3 n'], ['222', 'Pn3n'],
               ['223', 'P m -3 n'], ['223', 'Pm3n'], ['223', 'P m 3 n'],
               ['224', 'P n -3 m'], ['224', 'Pn3m'], ['224', 'P n 3 m'],
               ['225', 'F m -3 m'], ['225', 'F m 3 m'], ['225', 'Fm-3m'], ['225', 'Fm3m'],
               ['226', 'F m -3 c'], ['226', 'Fm3c'],
               ['227', 'F d -3 m'], ['227', 'Fd-3m'], ['227', 'F d 3 m'], ['227', 'Fd3m'],
               ['228', 'F d -3 c'], ['228', 'Fd3c'], ['228', 'F d 3 c'],
               ['229', 'I m -3 m'], ['229', 'Im-3m'], ['229', 'Im3m'], ['229', 'I m 3 m'],
               ['230', 'I a -3 d'], ['230', 'Ia-3d'], ['230', 'Ia3d'], ['230', 'I a 3 d']]
CATEGORIES = ['soil',
              'salt',
              'clay']

QMIN = 0.2
QMAX = 10.0
QSTEP = 0.01
QWIDTH = 0.05

def make_engine(dbname):
    return create_engine('sqlite:///%s' % (dbname),
                         poolclass=SingletonThreadPool)

def iscifDB(dbname):
    '''
    test if a file is a valid scan database:
    must be a sqlite db file, with tables named according to _tables
    '''
    _tables = ('ciftbl',
               'elemtbl',
               'nametbl',
               'spgptbl',
               'symtbl',
               'authtbl',
               'qtbl',
               'cattbl',
               'symref',
               'compref',
               'authref',
               'qref',
               'catref')
    result = False
    try:
        engine = make_engine(dbname)
        meta = MetaData(engine)
        meta.reflect()
        result = all([t in meta.tables for t in _tables])
    except:
        pass
    return result

class _BaseTable(object):
    "generic class to encapsulate SQLAlchemy table"
    def __repr__(self):
        el = getattr(self, 'element', '??')
        return "<%s(%s)>" % (self.__class__.__name__, el)

class ElementTable(_BaseTable):
    (z, name, symbol) = [None]*3

class MineralNameTable(_BaseTable):
    (id,name) = [None]*2

class SpaceGroupTable(_BaseTable):
    (iuc_id, hm_notation) = [None]*2

class CrystalSymmetryTable(_BaseTable):
    (id, name) = [None]*2

class AuthorTable(_BaseTable):
    (id,name) = [None]*2

class QTable(_BaseTable):
    (id, q) = [None]*2

class CategoryTable(_BaseTable):
    (id,name) = [None]*2

class CIFTable(_BaseTable):
    (amcsd_id, mineral_id, iuc_id, cif) = [None]*4


class cifDB(object):
    '''
    interface to the American Mineralogist Crystal Structure Database
    '''
    def __init__(self, dbname=None, read_only=True,verbose=False):

        ## This needs to be modified for creating new if does not exist.
        self.dbname=dbname
        if verbose:
            print('\n\n================ %s ================\n' % self.dbname)
        if not os.path.exists(self.dbname):
            parent, child = os.path.split(__file__)
            self.dbname = os.path.join(parent, self.dbname)
            if not os.path.exists(self.dbname):
                print("File '%s' not found; building a new database!" % self.dbname)
                self.create_database(name=self.dbname)
            else:
                if not iscifDB(self.dbname):
                    raise ValueError("'%s' is not a valid cif database file!" % self.dbname)
        
        self.dbname = self.dbname
        self.engine = make_engine(self.dbname)
        self.conn = self.engine.connect()
        kwargs = {}
        if read_only:
            kwargs = {'autoflush': True, 'autocommit':False}
            def readonly_flush(*args, **kwargs):
                return
            self.session = sessionmaker(bind=self.engine, **kwargs)()
            self.session.flush = readonly_flush
        else:
            self.session = sessionmaker(bind=self.engine, **kwargs)()

        self.metadata =  MetaData(self.engine)
        self.metadata.reflect()
        tables = self.tables = self.metadata.tables

        ## Load tables
        ciftbl  = tables['ciftbl']
        elemtbl = tables['elemtbl']
        nametbl = tables['nametbl']
        spgptbl = tables['spgptbl']
        symtbl  = tables['symtbl']
        authtbl = tables['authtbl']
        cattbl  = tables['cattbl']
        qtbl    = tables['qtbl']
        symref  = tables['symref']
        compref = tables['compref']
        authref = tables['authref']
        catref  = tables['catref']
        qref    = tables['qref']

        ## Define mappers
        clear_mappers()
        mapper(ElementTable, elemtbl, properties=dict(
                 a=relationship(ElementTable, secondary=compref,
                 primaryjoin=(compref.c.z == elemtbl.c.z),
                 secondaryjoin=(compref.c.amcsd_id == ciftbl.c.amcsd_id))))
        mapper(MineralNameTable, nametbl, properties=dict(
                 a=relationship(MineralNameTable, secondary=ciftbl,
                 primaryjoin=(ciftbl.c.mineral_id == nametbl.c.mineral_id))))
        mapper(SpaceGroupTable, spgptbl, properties=dict(
                 a=relationship(SpaceGroupTable, secondary=symref,
                 primaryjoin=(symref.c.iuc_id == spgptbl.c.iuc_id),
                 secondaryjoin=(symref.c.symmetry_id == symtbl.c.symmetry_id))))
        mapper(CrystalSymmetryTable, symtbl, properties=dict(
                 a=relationship(CrystalSymmetryTable, secondary=symref,
                 primaryjoin=(symref.c.symmetry_id == symtbl.c.symmetry_id),
                 secondaryjoin=(symref.c.iuc_id == spgptbl.c.iuc_id))))
        mapper(AuthorTable, authtbl, properties=dict(
                 a=relationship(AuthorTable, secondary=authref,
                 primaryjoin=(authref.c.author_id == authtbl.c.author_id))))
        mapper(QTable, qtbl, properties=dict(
                 a=relationship(QTable, secondary=qref,
                 primaryjoin=(qref.c.q_id == qtbl.c.q_id))))
        mapper(CategoryTable, cattbl, properties=dict(
                 a=relationship(CategoryTable, secondary=catref,
                 primaryjoin=(catref.c.category_id == cattbl.c.category_id))))
        mapper(CIFTable, ciftbl, properties=dict(
                 a=relationship(CIFTable, secondary=compref,
                 primaryjoin=(compref.c.amcsd_id == ciftbl.c.amcsd_id),
                 secondaryjoin=(compref.c.z == elemtbl.c.z))))

        self.load_database()


    def query(self, *args, **kws):
        "generic query"
        return self.session.query(*args, **kws)

    def open_database(self):

        print('\nAccessing database: %s' % self.dbname)
        self.metadata = MetaData('sqlite:///%s' % self.dbname)

    def close_database(self):
        "close session"
        self.session.flush()
        self.session.close()
        clear_mappers()
            
    def create_database(self,name=None,verbose=False):

        if name is None:
            self.dbname = 'amcsd%02d.db'
            counter = 0
            while os.path.exists(self.dbname % counter):
                counter += 1
            self.dbname = self.dbname % counter
        else:
            self.dbname = name
    
        self.open_database()

        ###################################################
        ## Look up tables
        elemtbl = Table('elemtbl', self.metadata,
                  Column('z', Integer, primary_key=True),
                  Column('element_name', String(40), unique=True, nullable=True),
                  Column('element_symbol', String(2), unique=True, nullable=False)
                  )
        nametbl = Table('nametbl', self.metadata,
                  Column('mineral_id', Integer, primary_key=True),
                  Column('mineral_name', String(30), unique=True, nullable=True)
                  )
        spgptbl = Table('spgptbl', self.metadata,
                  Column('iuc_id', Integer),
                  Column('hm_notation', String(16), unique=True, nullable=True),
                  PrimaryKeyConstraint('iuc_id', 'hm_notation')
                  )
        symtbl = Table('symtbl', self.metadata,
                 Column('symmetry_id', Integer, primary_key=True),
                 Column('symmetry_name', String(16), unique=True, nullable=True)
                 )
        authtbl = Table('authtbl', self.metadata,
                  Column('author_id', Integer, primary_key=True),
                  Column('author_name', String(40), unique=True, nullable=True)
                  )
        qtbl = Table('qtbl', self.metadata,
               Column('q_id', Integer, primary_key=True),
               #Column('q', Float()) ## how to make this work? mkak 2017.02.14
               Column('q', String())
               )
        cattbl = Table('cattbl', self.metadata,
                 Column('category_id', Integer, primary_key=True),
                 Column('category_name', String(16), unique=True, nullable=True)
                 )
        ###################################################
        ## Cross-reference tables
        symref = Table('symref', self.metadata,
                 Column('iuc_id', None, ForeignKey('spgptbl.iuc_id')),
                 Column('symmetry_id', None, ForeignKey('symtbl.symmetry_id')),
                 PrimaryKeyConstraint('iuc_id', 'symmetry_id')
                 )
        compref = Table('compref', self.metadata,
                  Column('z', None, ForeignKey('elemtbl.z')),
                  Column('amcsd_id', None, ForeignKey('ciftbl.amcsd_id')),
                  PrimaryKeyConstraint('z', 'amcsd_id')
                  )
        authref = Table('authref', self.metadata,
                  Column('author_id', None, ForeignKey('authtbl.author_id')),
                  Column('amcsd_id', None, ForeignKey('ciftbl.amcsd_id')),
                  PrimaryKeyConstraint('author_id', 'amcsd_id')
                  )
        qref = Table('qref', self.metadata,
               Column('q_id', None, ForeignKey('qtbl.q_id')),
               Column('amcsd_id', None, ForeignKey('ciftbl.amcsd_id')),
               PrimaryKeyConstraint('q_id', 'amcsd_id')
               )
        catref = Table('catref', self.metadata,
                 Column('category_id', None, ForeignKey('cattbl.category_id')),
                 Column('amcsd_id', None, ForeignKey('ciftbl.amcsd_id')),
                 PrimaryKeyConstraint('category_id', 'amcsd_id')
                 )
        ###################################################
        ## Main table
        ciftbl = Table('ciftbl', self.metadata,
                 Column('amcsd_id', Integer, primary_key=True),
                 Column('mineral_id', Integer),
                 Column('iuc_id', ForeignKey('spgptbl.iuc_id')),
                 Column('cif', String(25)) ## , nullable=True
                 )
        ###################################################
        ## Add all to file
        self.metadata.create_all() ## if not exists function (callable when exists)

        ###################################################
        ## Define 'add/insert' functions for each table
        def_elem = elemtbl.insert()
        def_name = nametbl.insert()
        def_spgp = spgptbl.insert()
        def_sym  = symtbl.insert()
        def_auth = authtbl.insert()
        def_q    = qtbl.insert()
        def_cat  = cattbl.insert()
        
        add_sym  = symref.insert()
        add_comp = compref.insert()
        add_auth = authref.insert()
        add_q    = qref.insert()
        add_cat  = catref.insert()

        new_cif  = ciftbl.insert()


        ###################################################
        ## Populate the fixed tables of the database

        ## Adds all elements into database
        for element in ELEMENTS:
            z, name, symbol = element
            def_elem.execute(z=int(z),element_name=name,element_symbol=symbol)

        ## Adds all crystal symmetries
        for symmetry_id,symmetry in enumerate(SYMMETRIES):
            def_sym.execute(symmetry_name=symmetry.strip())
            if symmetry.strip() == 'triclinic':      ## triclinic    :   1 -   2
                for iuc_id in range(1,2+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'monoclinic':   ## monoclinic   :   3 -  15
                for iuc_id in range(3,15+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'orthorhombic': ## orthorhombic :  16 -  74
                for iuc_id in range(16,74+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'tetragonal':   ## tetragonal   :  75 - 142
                for iuc_id in range(75,142+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'trigonal':     ## trigonal     : 143 - 167
                for iuc_id in range(143,167+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'hexagonal':    ## hexagonal    : 168 - 194
                for iuc_id in range(168,194+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))
            elif symmetry.strip() == 'cubic':        ## cubic        : 195 - 230
                for iuc_id in range(195,230+1):
                    add_sym.execute(iuc_id=iuc_id,symmetry_id=(symmetry_id+1))

        for cat in CATEGORIES:
            def_cat.execute(category_name=cat)

        ## Adds qrange
        qrange = np.arange(QMIN,QMAX+QSTEP,QSTEP)
        for q in qrange:
            def_q.execute(q=float('%0.2f' % q))

        ## Adds all space groups
        for spgrp in SPACEGROUPS:
            iuc_id,name = spgrp
            try:
                def_spgp.execute(iuc_id=str(iuc_id),hm_notation=name)
            except:
                if verbose:
                    print('Duplicate: %s %s' % (str(iuc_id),name))
                pass
  
    def load_database(self):

        ###################################################
        ## Look up tables
        self.elemtbl = Table('elemtbl', self.metadata)
        self.nametbl = Table('nametbl', self.metadata)
        self.spgptbl = Table('spgptbl', self.metadata)
        self.symtbl  = Table('symtbl',  self.metadata)
        self.authtbl = Table('authtbl', self.metadata)
        self.qtbl    = Table('qtbl',    self.metadata)
        self.cattbl  = Table('cattbl',  self.metadata)
        ###################################################
        ## Cross-reference tables
        self.symref  = Table('symref', self.metadata)
        self.compref = Table('compref', self.metadata)
        self.authref = Table('authref', self.metadata)
        self.qref    = Table('qref', self.metadata)
        self.catref  = Table('catref', self.metadata)
        ###################################################
        ## Main table
        self.ciftbl  = Table('ciftbl', self.metadata)
        
        
    def cif_to_database(self,cifile,verbose=True,url=False,ijklm=1):
        '''
            ## Adds cifile into database
            When reading in new CIF:
            i.   put entire cif into field
            ii.  read _database_code_amcsd; write 'amcsd_id' to 'cif data'
            iii. read _chemical_name_mineral; find/add in' minerallist'; write
                 'mineral_id' to 'cif data'
            iv.  read _symmetry_space_group_name_H-M - find in 'spacegroup'; write
                 iuc_id to 'cif data'
            v.   read author name(s) - find/add in 'authorlist'; write 'author_id',
                 'amcsd_id' to 'authref'
            vi.  read _chemical_formula_sum; write 'z' (atomic no.), 'amcsd_id'
                 to 'compref'
            vii. calculate q - find each corresponding 'q_id' for all peaks; in write
                 'q_id','amcsd_id' to 'qpeak'
        '''

        if not HAS_CifFile or not HAS_XRAYUTIL:
            print('Missing required package(s) for this function:')
            print('Have CifFile? %r' % HAS_CifFile)
            print('Have xrayutilities? %r' % HAS_XRAYUTIL)
            return
            
        cf = CifFile.ReadCif(cifile)

        key = cf.keys()[0]

        ## Read icsd_id
        amcsd_id = None
        try:
            amcsd_id = int(cf[key][u'_database_code_icsd'])
        except:
            amcsd_id = int(cf[key][u'_database_code_amcsd'])


        ## check for amcsd in file already
        ## Find amcsd_id in database
        self.ciftbl = Table('ciftbl', self.metadata)
        search_cif = self.ciftbl.select(self.ciftbl.c.amcsd_id == amcsd_id)
        for row in search_cif.execute():
            if url:
                print('AMCSD %i already exists in database %s: %s' % 
                     (amcsd_id,self.dbname,cifile))
            else:
                print('%s: AMCSD %i already exists in database %s.' % 
                     (os.path.split(cifile)[-1],amcsd_id,self.dbname))
            return

        ## Read elements
        ALLelements = cf[key][u'_chemical_formula_sum'].split()
        for e0,element in enumerate(ALLelements):
            element= re.sub('[(){}<>.]', '', element)
            element = re.sub(r'([0-9])', r'', element)
            ALLelements[e0] = element

        ## Read mineral name
        mineral_name = None
        try:
            mineral_name = cf[key][u'_chemical_name_mineral']
        except:
            try:
                mineral_name = cf[key][u'_amcsd_formula_title']
            except:
                pass
            pass

        ## Read Hermann-Mauguin/space group
        hm_notation = cf[key][u'_symmetry_space_group_name_h-m']

        ## Read author names    
        authors = cf[key][u'_publ_author_name']
        for i,author in enumerate(authors):
            author = re.sub(r"[.]", r"", author)
            authors[i] = re.sub(r"[,]", r"", author)

   
        ## generate hkl list
        hkllist = generate_hkl(maxval=50)

        energy = 8048 # units eV


        if url:
            cifstr = requests.get(cifile).text
            cif = xu.materials.Crystal.fromCIF('/fromweb/file.cif',fid=StringIO(cifstr))
        else:
            with open(cifile,'r') as file:
                cifstr = str(file.read())
            cif = xu.materials.Crystal.fromCIF(cifile)

        qlist = cif.Q(hkllist)
        Flist = cif.StructureFactorForQ(qlist,energy)

        qnorm = np.linalg.norm(qlist,axis=1)
        Fnorm = np.abs(Flist)

        peak_qid = []
        for i,qi in enumerate(qnorm):
            if Fnorm[i] > 0.01:
                #qid = int((qi-QMIN)/QSTEP)+1
                qid = self.search_for_q(qi)
                if qid not in peak_qid:
                    peak_qid.append(qid)

        ###################################################
        def_elem = self.elemtbl.insert()
        def_name = self.nametbl.insert()
        def_spgp = self.spgptbl.insert()
        def_sym  = self.symtbl.insert()
        def_auth = self.authtbl.insert()
        def_q    = self.qtbl.insert()
        def_cat  = self.cattbl.insert()
        add_sym  = self.symref.insert()
        add_comp = self.compref.insert()
        add_auth = self.authref.insert()
        add_q    = self.qref.insert()
        add_cat  = self.catref.insert()
        new_cif  = self.ciftbl.insert()

        ## Find mineral_name
        match = False
        search_mineral = self.nametbl.select(self.nametbl.c.mineral_name == mineral_name)
        for row in search_mineral.execute():
            mineral_id = row.mineral_id
            match = True
        if match is False:
            def_name.execute(mineral_name=mineral_name)
            search_mineral = self.nametbl.select(self.nametbl.c.mineral_name == mineral_name)
            for row in search_mineral.execute():
                mineral_id = row.mineral_id
                match = True

        ## Find symmetry_name
        match = False
        search_spgrp = self.spgptbl.select(self.spgptbl.c.hm_notation == hm_notation)
        for row in search_spgrp.execute():
            iuc_id = row.iuc_id
            match = True
        if match is False:
            ## need a real way to deal with this trouble
            ## mkak 2016.11.04
            iuc_id = 0
            print('\tSpace group? ----> %s (amcsd: %i)' % (hm_notation,int(amcsd_id)))

        ## Save CIF entry into database
        new_cif.execute(amcsd_id=int(amcsd_id),
                             mineral_id=int(mineral_id),
                             iuc_id=iuc_id,
                             cif=cifstr)    

        ## Find composition (loop over all elements)
        for element in ALLelements:
            search_elements = self.elemtbl.select(self.elemtbl.c.element_symbol == element)
            for row in search_elements.execute():
                z = row.z
            try:
                add_comp.execute(z=z,amcsd_id=int(amcsd_id))
            except:
                print('could not find element: %s (amcsd: %i)' % (element,int(amcsd_id)))
                pass


        ## Find author_name
        for author_name in authors:
            match = False
            search_author = self.authtbl.select(self.authtbl.c.author_name == author_name)
            for row in search_author.execute():
                author_id = row.author_id
                match = True
            if match is False:
                def_auth.execute(author_name=author_name)
                search_author = self.authtbl.select(self.authtbl.c.author_name == author_name)
                for row in search_author.execute():
                    author_id = row.author_id
                    match = True
            if match == True:
                add_auth.execute(author_id=author_id,
                                   amcsd_id=int(amcsd_id))


        for calc_q_id in peak_qid:
            add_q.execute(q_id=calc_q_id,amcsd_id=int(amcsd_id))
            

    #     ## not ready for defined categories
    #     cif_category.execute(category_id='none',
    #                          amcsd_id=int(amcsd_id))

        if url:
            if verbose:
                self.print_amcsd_info(amcsd_id,no_qpeaks=len(peak_qid))
        else:
            if verbose:
                self.print_amcsd_info(amcsd_id,no_qpeaks=len(peak_qid),cifile=cifile)
            else:
                print('File : %s' % os.path.split(cifile)[-1])

    def url_to_cif(self,verbose=False,savecif=False,trackerr=False,
                     addDB=True,url=None,all=False):
    
        if url is None:
            url = 'http://rruff.geo.arizona.edu/AMS/download.php?id=%05d.cif&down=cif'
            #url = 'http://rruff.geo.arizona.edu/AMS/CIF_text_files/%05d_cif.txt'
 
        if trackerr:
            dir = os.getcwd()
            ftrack = open('%s/trouble_cif.txt' % dir,'a+')
            ftrack.write('using URL : %s\n\n' % url)
        
        ## Defines url range for searching and adding to cif database
        if all == True:
            iindex = range(99999)
        else:
            iindex = np.arange(13600,13700)
        
        for i in iindex:
            url_to_scrape = url % i
            r = requests.get(url_to_scrape)
            if r.text.split()[0] == "Can't" or '':
                if verbose:
                    print('\t---> ERROR on amcsd%05d.cif' % i)
                    if trackerr:
                        ftrack.write('%s\n' % url_to_scrape)
            else:
                if verbose:
                    print('Reading %s' % url_to_scrape)
                if savecif:
                    file = 'amcsd%05d.cif' % i
                    f = open(file,'w')
                    f.write(r.text)
                    f.close()
                    if verbose:
                        print('Saved %s' % file)
                if addDB:
                    try:
                        self.cif_to_database(url_to_scrape,url=True,verbose=verbose,ijklm=i)
                    except:
                        if trackerr:
                            ftrack.write('%s\n' % url_to_scrape)
                        pass

        if trackerr:
            ftrack.close()


#     def database_array(self,maxrows=None):
#     
#         cif_array = {}
#         
#         search_cif = self.ciftbl.select()
#         count = 0
#         for cifrow in search_cif.execute():
#             amcsd_id = cifrow.amcsd_id
#             mineral_id = cifrow.mineral_id
#             iuc_id = cifrow.iuc_id
#             
#             mineral_name = ''
#             search_mineralname = self.nametbl.select(self.nametbl.c.mineral_id == mineral_id)
#             for mnrlrow in search_mineralname.execute():
#                 mineral_name = mnrlrow.mineral_name
#         
#             search_composition = self.compref.select(self.compref.c.amcsd_id == amcsd_id)
#             composition = ''
#             for cmprow in search_composition.execute():
#                 z = cmprow.z
#                 search_periodic = self.elemtbl.select(self.elemtbl.c.z == z)
#                 for elmtrow in search_periodic.execute():
#                     composition = '%s %s' % (composition,elmtrow.element_symbol)
#                     
#             search_authors = self.authref.select(self.authref.c.amcsd_id == amcsd_id)
#             authors = ''
#             for atrrow in search_authors.execute():
#                 author_id = atrrow.author_id
#                 search_alist = self.authtbl.select(self.authtbl.c.author_id == author_id)
#                 for block in search_alist.execute():
#                     if authors == '':
#                         authors = '%s' % (block.author_name)
#                     else:
#                         authors = '%s; %s' % (authors,block.author_name)
# 
#             count = count + 1
#             cif_array.update({count:(str(amcsd_id),str(mineral_name),str(iuc_id),str(composition),str(authors))})
#             if maxrows is not None:
#                  if count >= maxrows:
#                      return cif_array
#        
#         return cif_array



##################################################################################
##################################################################################

#         usr_qry = self.query(self.ciftbl,
#                              self.elemtbl,self.nametbl,self.spgptbl,self.symtbl,
#                              self.authtbl,self.qtbl,self.cattbl,
#                              self.authref,self.qref,self.compref,self.catref,self.symref)\
#                       .filter(self.authref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
#                       .filter(self.authtbl.c.author_id == self.authref.c.author_id)\
#                       .filter(self.qref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
#                       .filter(self.qref.c.q_id == self.qtbl.c.q_id)\
#                       .filter(self.compref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
#                       .filter(self.compref.c.z == self.elemtbl.c.z)\
#                       .filter(self.catref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
#                       .filter(self.catref.c.category_id == self.cattbl.c.category_id)\
#                       .filter(self.nametbl.c.mineral_id == self.ciftbl.c.mineral_id)\
#                       .filter(self.symref.c.symmetry_id == self.symtbl.c.symmetry_id)\
#                       .filter(self.symref.c.iuc_id == self.spgptbl.c.iuc_id)\
#                       .filter(self.spgptbl.c.iuc_id == self.ciftbl.c.iuc_id)

##################################################################################
##################################################################################


##################################################################################

    def print_amcsd_info(self,amcsd_id,no_qpeaks=None,cifile=None):

        ALLelements,mineral_name,iuc_id,authors = self.all_by_amcsd(amcsd_id)
        
        if cifile:
            print(' ==== File : %s ====' % os.path.split(cifile)[-1])
        else:
            print(' ===================== ')
        print(' AMCSD: %i' % amcsd_id)

        elementstr = ' Elements: '
        for element in ALLelements:
            elementstr = '%s %s' % (elementstr,element)
        print(elementstr)
        print(' Name: %s' % mineral_name)
        print(' Space Group No.: %s' % iuc_id)
        if no_qpeaks:
            print(' No. q-peaks in range : %s' % no_qpeaks)
        authorstr = ' Author: '
        for author in authors:
            try:
                authorstr = '%s %s' % (authorstr,author.split()[0])
            except:
                pass
        print(authorstr)
        print(' ===================== ')
        print('')

    def return_cif(self,amcsd_id):

        search_cif = self.ciftbl.select(self.ciftbl.c.amcsd_id == amcsd_id)
        for row in search_cif.execute():
            return row.cif

##################################################################################

    def all_by_amcsd(self,amcsd_id,verbose=False):

        mineral_id,iuc_id,cifstr = self.cif_by_amcsd(amcsd_id,all=True)
        
        #mineral_name = self.mineral_by_amcsd(amcsd_id)
        mineral_name = self.search_for_mineral(mineral_id,id_no=False)[0][0]
        ALLelements  = self.composition_by_amcsd(amcsd_id)
        authors      = self.author_by_amcsd(amcsd_id)
        
        return ALLelements,mineral_name,iuc_id,authors

    def q_by_amcsd(self,amcsd,qmin=None,qmax=None):

        usr_qry = self.query(self.ciftbl,self.qref,self.qtbl)\
                      .filter(self.qref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
                      .filter(self.qref.c.q_id == self.qtbl.c.q_id)\
                      .filter(self.qref.c.amcsd_id == amcsd)
        if qmin is not None and qmax is not None:
            usr_qry = usr_qry.filter(and_(self.qtbl.c.q > qmin,self.qtbl.c.q < qmax))
        elif qmin is not None:
            usr_qry = usr_qry.filter(self.qtbl.c.q > qmin)        
        elif qmax is not None:
            usr_qry = usr_qry.filter(self.qtbl.c.q < qmax)
            
        return [float(row.q) for row in usr_qry.all()]

    def author_by_amcsd(self,amcsd_id):

        search_authors = self.authref.select(self.authref.c.amcsd_id == amcsd_id)
        authors = []
        for row in search_authors.execute():
            authors.append(self.search_for_author(row.author_id,id_no=False)[0][0])
        return authors

    def composition_by_amcsd(self,amcsd_id):

        search_composition = self.compref.select(self.compref.c.amcsd_id == amcsd_id)
        ALLelements = []
        for row in search_composition.execute():
            z = row.z
            search_periodic = self.elemtbl.select(self.elemtbl.c.z == z)
            for block in search_periodic.execute():
                ALLelements.append(block.element_symbol)
                
        return ALLelements

    def cif_by_amcsd(self,amcsd_id,all=False):

        search_cif = self.ciftbl.select(self.ciftbl.c.amcsd_id == amcsd_id)
        for row in search_cif.execute():
            if all: return row.mineral_id,row.iuc_id,row.cif
            else: return row.cif

    def mineral_by_amcsd(self,amcsd_id):

        search_cif = self.ciftbl.select(self.ciftbl.c.amcsd_id == amcsd_id)
        for row in search_cif.execute():
            cifstr = row.cif
            mineral_id = row.mineral_id
            iuc_id = row.iuc_id
        
        search_mineralname = self.nametbl.select(self.nametbl.c.mineral_id == mineral_id)
        for row in search_mineralname.execute():
            mineral_name = row.mineral_name
        return mineral_name

##################################################################################
##################################################################################

    def amcsd_by_q(self,include=[],list=None,verbose=False,minpeaks=2):

        q_incld  = []
        id_incld = []

        all_matches = []
        matches = []
        count = []

        
        if len(include) > 0:
            for q in include:
                q  = round_value(q,base=QSTEP)
                id = self.search_for_q(q)
                if id is not None and id not in id_incld:
                    id_incld += [id]
                        
        usr_qry = self.query(self.ciftbl,self.qtbl,self.qref)\
                      .filter(self.qref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
                      .filter(self.qref.c.q_id == self.qtbl.c.q_id)
        if list is not None:
            usr_qry = usr_qry.filter(self.ciftbl.c.amcsd_id.in_(list))

        ##  Searches composition of database entries

        if len(id_incld) > 0:
            fnl_qry = usr_qry.filter(self.qref.c.q_id.in_(id_incld))
#             fnl_qry = usr_qry.filter(self.qref.c.q_id.in_(id_incld))\
#                              .group_by(self.qref.c.amcsd_id)\
#                              .having(func.count()>2)## having at least two in range is important
            for row in fnl_qry.all():

                if row.amcsd_id not in matches:
                    matches += [row.amcsd_id]
                    count += [1]
                else:
                    idx = matches.index(row.amcsd_id)
                    count[idx] = count[idx]+1

        amcsd_matches = [x for y, x in sorted(zip(count,matches)) if y > minpeaks]
        count_matches = [y for y, x in sorted(zip(count,matches)) if y > minpeaks]
       
        return amcsd_matches,count_matches


    def amcsd_by_chemistry(self,include=[],exclude=[],list=None,verbose=False):

        amcsd_incld = []
        amcsd_excld = []
        z_incld = []
        z_excld = []
        
        if len(include) > 0:
            for element in include:
                z = self.search_for_element(element)
                if z is not None and z not in z_incld:
                    z_incld += [z]
        if isinstance(exclude,bool):
            if exclude:
                for element in ELEMENTS:
                    z, name, symbol = element
                    z = int(z)
                    if z not in z_incld:
                        z_excld += [z]
        else:
            if len(exclude) > 0:
                for element in exclude:
                    z = self.search_for_element(element)
                    if z is not None and z not in z_excld:
                        z_excld += [z] 


                        
        usr_qry = self.query(self.ciftbl,self.elemtbl,self.compref)\
                      .filter(self.compref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
                      .filter(self.compref.c.z == self.elemtbl.c.z)
        if list is not None:
            usr_qry = usr_qry.filter(self.ciftbl.c.amcsd_id.in_(list))

        ##  Searches composition of database entries
        if len(z_excld) > 0:
            fnl_qry = usr_qry.filter(self.compref.c.z.in_(z_excld))
            for row in fnl_qry.all():
                if row.amcsd_id not in amcsd_excld:
                    amcsd_excld += [row.amcsd_id]

        if len(z_incld) > 0:
            ## more elegant method but overloads query when too many (e.g. all others)
            ## used for exclusion
            ## mkak 2017.02.20
            #if len(amcsd_excld) > 0:
            #    usr_qry = usr_qry.filter(not_(self.compref.c.amcsd_id.in_(amcsd_excld)))
            fnl_qry = usr_qry.filter(self.compref.c.z.in_(z_incld))\
                             .group_by(self.compref.c.amcsd_id)\
                             .having(func.count()==len(z_incld))
            for row in fnl_qry.all():
                if row.amcsd_id not in amcsd_incld and row.amcsd_id not in amcsd_excld:
                    amcsd_incld += [row.amcsd_id]
        
        return amcsd_incld


    def amcsd_by_mineral(self,include='',list=None,verbose=True):

        amcsd_incld = []
        mnrl_id = self.search_for_mineral(include)

        usr_qry = self.query(self.ciftbl)
        if list is not None:
            usr_qry = usr_qry.filter(self.ciftbl.c.amcsd_id.in_(list))

 
        ##  Searches mineral name for database entries
        if len(mnrl_id) > 0:
            fnl_qry = usr_qry.filter(self.ciftbl.c.mineral_id.in_(mnrl_id))
            for row in fnl_qry.all():
                if row.amcsd_id not in amcsd_incld:
                    amcsd_incld += [row.amcsd_id]

        return amcsd_incld


    def amcsd_by_author(self,include=[''],list=None,verbose=True):

        amcsd_incld = []
        auth_id = []
        
        for author in include:
            id = self.search_for_author(author)
            auth_id += id

        ##  Searches mineral name for database entries
        usr_qry = self.query(self.ciftbl,self.authtbl,self.authref)\
                      .filter(self.authref.c.amcsd_id == self.ciftbl.c.amcsd_id)\
                      .filter(self.authref.c.author_id == self.authtbl.c.author_id)
        if list is not None:
            usr_qry = usr_qry.filter(self.ciftbl.c.amcsd_id.in_(list))

        ##  Searches author name in database entries
        if len(auth_id) > 0:
            fnl_qry = usr_qry.filter(self.authref.c.author_id.in_(auth_id))
            ## This currently works in an 'or' fashion, as each name in list
            ## can be matched to multiple auth_id values, so it is simpler to
            ## consider them all separately. Making a 2D list and restructuring
            ## query could improve this
            ## mkak 2017.02.24
            for row in fnl_qry.all():
                if row.amcsd_id not in amcsd_incld:
                    amcsd_incld += [row.amcsd_id]
        
        return amcsd_incld


##################################################################################
##################################################################################

    def search_for_q(self,q,qstep=None):
        '''
        searches q-reference table for match q value.
        '''
        if qstep is None:
            q1 = self.query(self.qtbl).filter(self.qtbl.c.q_id == 1)
            q2 = self.query(self.qtbl).filter(self.qtbl.c.q_id == 2)
            for qi,qj in zip(q1.all(),q2.all()):
                qstep = float(qj.q)-float(qi.q)
            
        q = round_value(q,base=qstep) 
     
        qrow = self.query(self.qtbl).filter(self.qtbl.c.q == q)
        if len(qrow.all()) == 1:
            for q0 in qrow.all():
                q_id = q0.q_id
                return q_id
        return
     
    def search_for_element(self,element,id_no=True,verbose=False):
        '''
        searches elements for match in symbol, name, or atomic number; match must be 
        exact.
        '''
        element = capitalize_string(element)
        elemrow = self.query(self.elemtbl)\
                      .filter(or_(self.elemtbl.c.z == element,
                                  self.elemtbl.c.element_symbol == element,
                                  self.elemtbl.c.element_name == element))
        if len(elemrow.all()) == 0:
            if verbose: print('%s not found in element database.' % element)
            return
        else:
            for row in elemrow.all():
                if id_no: return row.z
                else: return row

    def search_for_author(self,name,exact=False,id_no=True,verbose=False):
        '''
        searches database for author matching criteria given in 'name'
           - if name is a string:
                  - will match author name containing text
                  - will match id number if integer given in string
                  - will only look for exact match if exact flag is given
           - if name is an integer, will only match id number from database
        id_no: if True, will only return the id number of match(es)
               if False, returns name and id number
        e.g.   as INTEGER
               >>> cif.search_for_author(6,id_no=False)
                    ([u'Chao G Y'], [6])
               as STRING
               >>> cif.search_for_author('6',id_no=False)
                    ([u'Chao G Y', u'Geology Team 654'], [6, 7770])
        '''
    
        authname = []
        authid   = []

        id,name = filter_int_and_str(name,exact=exact)
        authrow = self.query(self.authtbl)\
                      .filter(or_(self.authtbl.c.author_name.like(name),
                                  self.authtbl.c.author_id  == id))
        if len(authrow.all()) == 0:
            if verbose: print('%s not found in author database.' % name)
        else:
            for row in authrow.all():
                authname += [row.author_name]
                authid   += [row.author_id]
                
        if id_no: return authid
        else: return authname,authid

    def search_for_mineral(self,name,exact=False,id_no=True,verbose=False):
        '''
        searches database for mineral matching criteria given in 'name'
           - if name is a string:
                  - will match mineral name containing text
                  - will match id number if integer given in string
                  - will only look for exact match if exact flag is given
           - if name is an integer, will only match id number from database
        id_no: if True, will only return the id number of match(es)
               if False, returns name and id number
        e.g.   as INTEGER
               >>> newcif.search_for_mineral(884,id_no=False)
                    ([u'Mg8(Mg2Al2)Al8Si12(O,OH)56'], [884])
               as STRING
               >>> newcif.search_for_mineral('884',id_no=False)
                    ([u'Mg8(Mg2Al2)Al8Si12(O,OH)56', u'Co3 Ge2.884 Tb0.624'], [884, 5973])
        
        '''
        mrlname = []
        mrlid   = []

        id,name = filter_int_and_str(name,exact=exact)
        mnrlrow = self.query(self.nametbl)\
                      .filter(or_(self.nametbl.c.mineral_name.like(name),
                                  self.nametbl.c.mineral_id  == id))
        if len(mnrlrow.all()) == 0:
            if verbose: print('%s not found in mineral name database.' % name)
        else:
            for row in mnrlrow.all():
                mrlname += [row.mineral_name]
                mrlid   += [row.mineral_id]
                
        if id_no: return mrlid
        else: return mrlname,mrlid
     
    def return_no_of_cif(self):
        
        lines = len(self.query(self.ciftbl).all())
        return lines

    def return_q(self):
        
        qqry = self.query(self.qtbl)
        q = [float(row.q) for row in qqry.all()]

        return np.array(q)

    def return_mineral_names(self):
        
        mineralqry = self.query(self.nametbl)
        names = ['']
        for row in mineralqry.all():
            names += [row.mineral_name]
        
        return sorted(names)

    def return_author_names(self):
        
        authorqry = self.query(self.authtbl)
        names = []
        for row in authorqry.all():
            names += [row.author_name]
        
        return sorted(names)

def round_value(x, prec=2, base=0.05):
  return round(base * round(float(x)/base),prec)

def capitalize_string(s):

    try:
        return s[0].upper() + s[1:].lower()
    except:
        return s
    
def filter_int_and_str(s,exact=False):

        try: i = int(s)
        except: i = 0
        if not exact:
            try: s = '%'+s+'%'
            except: pass
        
        return i,s


## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##
## --- xrayutilities method for reading cif ---
##
##         search_cif = self.ciftbl.select(self.ciftbl.c.amcsd_id == amcsd_id)
##         for row in search_cif.execute():
##             cifstr = row.cif
##         cif = xu.materials.Crystal.fromCIF('/fromdatabase/file.cif',fid=StringIO(cifstr))
##
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def column(matrix, i):
    return [row[i] for row in matrix]

class RangeParameter(object):

    def __init__(self,min=None,max=None,unit=None):

        self.min   = min
        self.max   = max
        self.unit  = unit
        
    def set_values(self,min=None,max=None,unit=None):

        self.__init__(min=min,max=max,unit=unit)

class SearchCIFdb(object):
    '''
    interface to the search the cif database
    '''
    def __init__(self, verbose=False):
    
        self.verbose = verbose
        
        ## running list of included amcsd id numbers
        self.amcsd_id = []

        ## tags for searching
        self.authors    = []
        self.keywords   = []
        self.categories = []
        self.amcsd      = []
        self.qpks       = []

        self.mnrlname   = ''

        self.elem_incl = []
        self.elem_excl = []
        self.allelem   = column(ELEMENTS,2)

        self.lattice_keys = ['a','b','c','alpha','beta','gamma']

        self.sg    = None
        self.a     = RangeParameter()
        self.b     = RangeParameter()
        self.c     = RangeParameter()
        self.alpha = RangeParameter()
        self.beta  = RangeParameter()
        self.gamma = RangeParameter()


        


    def print_all(self):
    
        for key in ['authors','mnrlname','keywords','categories','amcsd','qpks']:
             print('%s : %s' % (key,self.print_parameter(key=key)))
        print('chemistry : %s' % self.print_chemistry())
        print('geometry : %s' % self.print_geometry())
    
    def print_parameter(self,key='authors'):

        s = ''
        if len(self.__dict__[key]) > 0:
            for i,item in enumerate(self.__dict__[key]):
                item = item.split()[0]
                if i == 0:
                    s = '%s' % (item)
                else:
                    s = '%s, %s' % (s,item)
        return s

        
    def read_parameter(self,s,clear=True,key='authors'):
        '''
        This function works for keys: 
        'authors'
        'mnrlname
        keywords','categories','amcsd','qpks'
        '''
       
        if clear:
            self.__dict__[key] = []
        if len(s) > 0:
            for a in s.split(','):
                try:
                    self.__dict__[key] += [a.split()[0]]
                except:
                    pass

    def print_chemistry(self):
    
        s = ''
        for i,elem in enumerate(self.elem_incl):
            if i==0:
                s = '(%s' % elem
            else:
                s = '%s,%s' % (s,elem)
        if len(self.elem_incl) > 0:
            s = '%s) ' % s 
        if len(self.elem_excl) > 0:
            s = '%s- ' % s
        # if all else excluded, don't list
        if (len(self.allelem)-20) > (len(self.elem_incl)+len(self.elem_excl)): 
            for i,elem in enumerate(self.elem_excl):
                if i==0:
                    s = '%s(%s' % (s,elem)
                else:
                    s = '%s,%s' % (s,elem)
            if len(self.elem_excl) > 0:
                s = '%s)' % s
        return s
                
    def read_chemistry(self,s,clear=True):
       
        if clear:
            self.elem_incl,self.elem_excl = [],[]
        chem_incl,chem_excl = [],[]

        chemstr = re.sub('[( )]','',s)
        ii = -1
        for i,s in enumerate(chemstr):
            if s == '-':
                ii = i
        if ii > 0:
            chem_incl = chemstr[0:ii].split(',')
            if len(chemstr)-ii == 1:
                for elem in self.allelem:
                    if elem not in chem_incl:
                        chem_excl += [elem]
            elif ii < len(chemstr)-1:
                chem_excl = chemstr[ii+1:].split(',')
        else:
            chem_incl = chemstr.split(',')

        for elem in chem_incl:
            elem = capitalize_string(elem)
            if elem in self.allelem and elem not in self.elem_incl:
                self.elem_incl += [elem]
                if elem in self.elem_excl:
                    j = self.elem_excl.index(elem)
                    self.elem_excl.pop(j)
        for elem in chem_excl:
            elem = capitalize_string(elem)
            if elem in self.allelem and elem not in self.elem_excl and elem not in self.elem_incl:
                self.elem_excl += [elem]

    def print_geometry(self,unit='A'):

        s = ''

        key = 'sg'
        if self.__dict__[key] is not None:
            s = '%s%s=%s,' % (s,key,self.__dict__[key])
        for i,key in enumerate(self.lattice_keys):
            if self.__dict__[key].min is not None:
                s = '%s%s=%0.2f' % (s,key,float(self.__dict__[key].min))
                if self.__dict__[key].max is not None:
                    s = '%sto%0.2f' % (s,float(self.__dict__[key].max))
                s = '%s%s,' % (s,self.__dict__[key].unit)

        if len(s) > 1:
            if s[-1] == ',':
                s = s[:-1]

        return s

    def read_geometry(self,s):
        
        geostr = s.split(',')
        used = []
        for par in geostr:
            key = par.split('=')[0]
            val = par.split('=')[1]
            if key in 'sg':
                self.__dict__[key] = val
                used += [key]            
            elif key in self.lattice_keys:
                values = [''.join(g) for _, g in groupby(val, str.isalpha)]
                self.__dict__[key].min = values[0]
                if len(values) > 1: 
                    self.__dict__[key].unit = values[-1]
                if len(values) > 2:
                    self.__dict__[key].max = values[2]
                else:
                    self.__dict__[key].max = None
                used += [key]

        ## Resets undefined to None
        for key in self.lattice_keys:
            if key not in used:
                self.__dict__[key] = RangeParameter()
        key = 'sg'
        if key not in used:
            self.__dict__[key] = None
            
def match_database(fracq=0.75, pk_wid=0.05, q=None, ipks=None,
                   cifdatabase=None, verbose=False):
    '''
    fracq  : min. ratio of matched q to possible in q range, i.e. 'goodness gauge'
    pk_wid : maximum range in q which qualifies as a match between fitted and ideal

    '''

    q_pks = peaklocater(ipks,q)
    minq = np.min(q)
    maxq = np.max(q)

    qstep = QSTEP ## these quantities come from cifdb.py

    peaks = []
    p_ids = []

    for pk_q in q_pks:
        pk_id = cifdatabase.search_for_q(pk_q)

        ## performs peak broadening here
        if pk_wid > 0:
            st = int(pk_wid/qstep/2)
            for p in np.arange(-1*st,st+1):
                peaks += [pk_q+p*qstep]
                p_ids += [pk_id+p]
        else:
            peaks += [pk_q]
            p_ids += [pk_id]

    matches,count = cifdatabase.amcsd_by_q(peaks)
    goodness = np.zeros(len(count))

    for i, (amcsd,cnt) in enumerate(zip(matches,count)):
        peak_id = sorted(cifdatabase.q_by_amcsd(amcsd,qmin=minq,qmax=maxq))
        if len(peak_id) > 0:
            goodness[i] = float(cnt)/len(peak_id)

    try:
        matches,count,goodness = zip(*[(x,y,t) for t,x,y in sorted(zip(goodness,matches,count)) if t > fracq])
    except:
        matches,count,goodness = [],[],[]

    for i,amcsd in enumerate(matches):
        if verbose:
            str = 'AMCSD %i, %s (%0.3f --> %i of %i peaks)' % (amcsd,
                     cifdatabase.mineral_by_amcsd(amcsd),goodness[i],
                     count[i],count[i]/goodness[i])
            print(str)

               
    return matches
                
                          
                






