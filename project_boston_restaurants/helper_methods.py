def biz2yelp():
    import pandas as pd
    df = pd.read_csv('restaurant_ids_to_yelp_ids.csv')
    d0 = df[['restaurant_id', 'yelp_id_0']]
    d1 = df[['restaurant_id', 'yelp_id_1']][df.yelp_id_1.notnull()]
    d1.rename(columns={'yelp_id_1': 'yelp_id_0'}, inplace=True)
    d2 = df[['restaurant_id', 'yelp_id_2']][df.yelp_id_2.notnull()]
    d2.rename(columns={'yelp_id_2': 'yelp_id_0'}, inplace=True)
    d3 = df[['restaurant_id', 'yelp_id_3']][df.yelp_id_3.notnull()]
    d3.rename(columns={'yelp_id_3': 'yelp_id_0'}, inplace=True)
    return pd.concat([d0, d1, d2, d3], ignore_index=True)

def read_json(filename):
    import pandas as pd
    with open(filename, 'rb') as f:
        data = f.readlines()
    data = map(lambda x: x.rstrip(), data)
    data_json_str = "[" + ','.join(data) + "]"
    return pd.read_json(data_json_str)
