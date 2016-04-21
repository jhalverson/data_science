def load_data(train=True, engineering=True, standardizer=None):
    """Read in the train or test data."""
 
    import numpy as np
    import pandas as pd
 
    # load the data set into a DataFrame
    file_name = 'train_blood.csv' if train else 'test_blood.csv'
    column_names = ['id_number', 'months_since_last', 'number_of_donations', 'total_volume', 'months_since_first', 'donation_in_march']
    if train:
        df = pd.read_csv(file_name, header=0, names=column_names)
    else:
        df = pd.read_csv(file_name, header=0, names=column_names[:-1])

    # extract targets and ids (use dummy array for test case)
    y = np.array(np.zeros(len(df)), dtype=np.int)
    if train:
        y = df['donation_in_march'].values
        df = df.drop(['donation_in_march'], axis=1)
    ids = df['id_number'].values
    df = df.drop(['id_number'], axis=1)

    # remove total_volume which is perfectly correlated with number_of_donations
    df = df.drop(['total_volume'], axis=1)
 
    # feature engineering
    if (engineering):
        df['last_to_first'] = df['months_since_last'] / df['months_since_first']
        df['months_btwn_donation'] = df['months_since_first'] / df['number_of_donations']
        df['inverse_first'] = 1.0 / df['months_since_first']

    # generate combinations of features
    features_set = []
    if train:
        from itertools import combinations as cmbs
	columns = df.columns.tolist()
        features_set = []
	for k in range(3, len(columns) + 1):
	    features_set.extend(list(cmbs(columns, k)))
	features_set = map(list, features_set)
   
    # preprocessing
    if standardizer:
        if train:
            df = pd.DataFrame(standardizer.fit_transform(df.values), columns=df.columns)
        else:
            df = pd.DataFrame(standardizer.transform(df.values), columns=df.columns)

    return df, y, ids, features_set
