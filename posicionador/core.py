from .definitions import json, gpd, Polygon, pd
from .definitions import bound_series_to_geoseries, bounds_to_polygon, polygon_to_bound_str

def correct_polos_from_id(territories, polo_id):

    if type(territories) != type(pd.DataFrame()):
        raise Exception('WARN: wrong data format')

    if not all(n in territories.columns for n in ['Bounds__c', 'Name','Id','ParentTerritory2Id']):
        raise Exception('WARN: wrong dataframe format')
    
    # 'Inputs' Territory DataFrames:
    polo_df = territories[territories['Id']==polo_id]
    rotas_df = territories[territories['ParentTerritory2Id']==polo_id]
        
    # If rotas does not exist:
    if len(rotas_df) < 1:
        raise Exception('WARN: Rotas não encontadas para polo: {}'.format(polo_df['Name'].loc[0]))
        return None
        
    # 'Inputs' Territory GeoDataFrames Transformming:
    rotas_geo = gpd.GeoDataFrame({
                        'Id': rotas_df['Id'].values,
                        'ParentTerritory2Id': rotas_df['ParentTerritory2Id'].values,
                        'Name': rotas_df['Name'].values,
                        'geometry': bound_series_to_geoseries(rotas_df['Bounds__c'])
                        })

    polo_geo = gpd.GeoDataFrame({
                        'Id': polo_df['Id'].values, 
                        'ParentTerritory2Id': polo_df['ParentTerritory2Id'].values,
                        'Name': polo_df['Name'].values,
                        'geometry': bound_series_to_geoseries(polo_df['Bounds__c'])
                        })
    
    # Getting Intersection Between Polos and Rotas:
    new_rotas_geo = gpd.overlay(rotas_geo, polo_geo, how='intersection')
    
    # Thron Away Areas:
    thrown_away = pd.concat([gpd.overlay(rotas_geo, polo_geo, how='difference'),
                             gpd.overlay(polo_geo, rotas_geo, how='difference')])
    
    #return new_rotas_geo, rotas_geo, polo_geo, thrown_away
    
    # Getting Rotas SalesForce-Like type:
    new_rotas = pd.DataFrame()
    new_rotas[['Id', 'Name', 'ParentTerritory2Id']] = pd.DataFrame(new_rotas_geo[['Id_1', 'Name_1', 'ParentTerritory2Id_1']])
    new_rotas['Bounds__c'] = new_rotas_geo['geometry'].apply(polygon_to_bound_str)
    
    return new_rotas, thrown_away, rotas_geo, polo_geo, new_rotas_geo
    