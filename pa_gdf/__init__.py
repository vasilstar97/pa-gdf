"""
Python package for validating `gpd.GeoDataFrame`. Includes `BaseSchema` to inherit from. 
"""

import importlib

__version__ = importlib.metadata.version("pa_gdf")
__author__ = "Vasilii Starikov"
__email__ = "vasilstar97@gmail.com"
__credits__ = []
__license__ = "BSD-3"

from .base_schema import BaseSchema