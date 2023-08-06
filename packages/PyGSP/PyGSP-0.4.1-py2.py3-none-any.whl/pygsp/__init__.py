# -*- coding: utf-8 -*-

"""
This toolbox is splitted in different modules taking care of the different aspects of Graph Signal Processing.

Those modules are : :ref:`Graphs <graphs-api>`, :ref:`Filters <filters-api>`, :ref:`Operators <operators-api>`, :ref:`PointCloud <pointclouds-api>`, :ref:`Plotting <plotting-api>`, :ref:`Data Handling <data_handling-api>` and :ref:`Utils <utils-api>`.

You can find detailed documentation on the use of the functions in the subsequent pages.
"""

# When importing the toolbox, you surely want these modules.
from pygsp import graphs
from pygsp import operators
from pygsp import utils
from pygsp import features
from pygsp import filters
from pygsp import pointclouds
from pygsp import data_handling
from pygsp import optimization
from pygsp import plotting

# Silence the code checker warning about unused symbols.
assert data_handling
assert filters
assert graphs
assert operators
assert optimization
assert pointclouds
assert features
assert plotting
assert utils

__version__ = '0.4.2'
__email__ = 'LTS2Graph@groupes.epfl.ch'
__release_date__ = '2017-04-27'
