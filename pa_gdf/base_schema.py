import pandera as pa
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
from pandera.typing import Index
from pandera.typing.geopandas import GeoSeries

DEFAULT_CRS = 4326

class BaseSchema(pa.DataFrameModel):
    """
    Base `gpd.GeoDataFrame` schema to inherit from.

    Defined basic `index` and `geometry` columns as well as methods for: 
    
    - validating geometry types;
    - generating empty `gpd.GeoDataFrame`.

    Notes:

    While inheriting make sure to override `_geometry_types() -> set[type[BaseGeometry]]` class method.

    """
    
    idx: Index[int] = pa.Field(unique=True)
    """Unique `gpd.GeoDataFrame` index."""
    
    geometry: GeoSeries
    """`gpd.GeoDataFrame` geometry column."""
    
    class Config:
        """
        Base schema config.
        
        Attributes:
        ---------
        strict : str
            Filters extra columns.
        add_missing_columns : bool
            Adds missing columns if not presented.
        """
        strict = "filter"
        add_missing_columns = True

    @classmethod
    def _geometry_types(cls) -> set[type[BaseGeometry]]:
        """
        Return available geometry types for the schema.
        
        Raises
        ------
        NotImplementedError
            If method is not implemented in the schema.
        """
        raise NotImplementedError

    @classmethod
    def generate_empty_gdf(cls) -> gpd.GeoDataFrame:
        """
        Creates an empty `gpd.GeoDataFrame` using schema columns.
        
        Returns
        -------
        gpd.GeoDataFrame
            Empty `gpd.GeoDataFrame` with set default CRS.
        """
        columns = cls.to_schema().columns.keys()
        return gpd.GeoDataFrame(columns=columns, crs=DEFAULT_CRS)

    @pa.check("geometry")
    @classmethod
    def _check_geometry(cls, series):
        """
        Checks geometry types using `_geometry_types()` method.
        
        Parameters
        ----------
        series
            `gpd.GeoDataFrame` geometry column series to validate.
        
        Returns
        -------
        pandera.typing.Series[bool]
            True, if geometry is one of the available types.
        """
        return series.map(lambda x: any(isinstance(x, geom_type) for geom_type in cls._geometry_types()))
