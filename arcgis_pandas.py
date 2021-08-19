import arcpy
import numpy as np
import pandas as pd
import os

def argis2df(table, index_col=None):
    """Arcgis table to pandas dataframe
    :param table: arcgis table, with or without geometry (shape)
    :param index_col: colum to pass as pandas index
    :return: pandas DataFrame
    """

    desc = arcpy.Describe(table)
    cursor = arcpy.SearchCursor(table)

    new_data = []

    for row in cursor:
        new_row = {}
        for field in desc.fields:
            new_row[field.aliasName or field.name] = row.getValue(field.name)
        new_data.append(new_row)

    try:
        if not index_col:
            index_col = desc.OIDFieldName

        df = pd.DataFrame(new_data).set_index(index_col)
        df["SHAPEArea"] = df[desc.shapeFieldName].apply(lambda g: g.area)
        df["SHAPELength"] = df[desc.shapeFieldName].apply(lambda g: g.length)
        df[desc.shapeFieldName] = df[desc.shapeFieldName].apply(lambda g: g.WKT)
    except AttributeError:
        pass
    
    return df


def df2argis(df,gdb,fc):
    """pandas dataframe to arcgis table (without geometry
    :param df: pandas DataFrame 
    :param gdb: geodatabe destination
    :return: arcgis table without geometry (shape)
    """
    def _suppr(fc) :
      if arcpy.Exists(fc):
          arcpy.Delete_management(fc)
    _suppr(fc)       
    x = np.array(np.rec.fromrecords(df.values))
    names = df.dtypes.index.tolist()
    x.dtype.names = tuple(names)
    arcpy.da.NumPyArrayToTable(x, gdb + os.sep +fc)

        
        

