import geopandas as gpd
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from database.base import Base
from database.base import engine


class LineRoute(Base):
    __tablename__ = 'lines_routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    geom = Column(Geometry(geometry_type='LINESTRING', srid=4326))
    name = Column(String)
    ground = Column(String)
    direction = Column(String)

    def __init__(self, db):
        self.db = db

    def compare_linestrings(self, linestring: str):
        gdf = gpd.GeoDataFrame.from_postgis(
            f"""
                SELECT *
                FROM lines_routes
                WHERE name IN
                      (SELECT subquery.name
                       FROM (SELECT *,
                                    ST_HausdorffDistance(
                                            geom,
                                            ST_GeomFromText(
                                                    '{linestring}',
                                                    4326
                                                )
                                        ) as distance
                             FROM lines_routes
                             ORDER BY distance
                             LIMIT 3) AS subquery)
                ORDER BY id;
            """,
            geom_col='geom',
            con=engine
        )

        # Convert to json for fastapi
        gdf['geom'] = gdf['geom'].apply(lambda x: x.__geo_interface__)

        return gdf.to_dict(orient='records')

    def get_by_name(self, name: str):
        gdf = gpd.GeoDataFrame.from_postgis(
            f"""
            SELECT *
            FROM lines_routes
            WHERE name = '{name}';
            """,
            geom_col='geom',
            con=engine
        )

        # Convert to json for fastapi
        gdf['geom'] = gdf['geom'].apply(lambda x: x.__geo_interface__)

        return gdf.to_dict(orient='records')
