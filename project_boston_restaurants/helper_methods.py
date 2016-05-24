def biz2yelp():
    import pandas as pd
    df = pd.read_csv('data/restaurant_ids_to_yelp_ids.csv')
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

def drop_duplicate_inspections(df, threshold=60):
    """Removes duplicate inspections."""
    import numpy as np
    indices_to_drop = []
    for i in range(0, df.shape[0]):
        if (i + 1 == df.shape[0]): break
        restaurant_match = df.iloc[i, 2] == df.iloc[i + 1, 2]
        violation_match = all([df.iloc[i, j] == df.iloc[i + 1, j] for j in [3, 4, 5]])
        date_match = (df.iloc[i + 1, 1] - df.iloc[i, 1]) / np.timedelta64(1, 'D') < threshold
        if (restaurant_match and violation_match and date_match): indices_to_drop.append(df.index[i + 1])
    return df.drop(indices_to_drop)
