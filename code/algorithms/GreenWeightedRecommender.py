import pandas as pd

'''
Pseudocode:

for every interaction:
    utility = alpha*rating + (1-alpha)*greenness

'''

ALPHAS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# ALPHAS = [1, 0.8, 0.6]
# techniques = ["GlobalAverage", "SVD", "SVDpp", "CoClustering"]
# NUMBERS = ["1", "2"]

techniques = ["userKNN", "itemKNN"]
NUMBERS = ["", "1", "2"]

for technique in techniques:
    for set_number in NUMBERS:
        item_data = pd.read_csv("recipes_with_carbon_total_filtered_and_removed_by_mean_outliers_removed_greenness.csv")
        predictions = pd.read_csv("../separating_data/full_test_sets/predictions_"+technique+set_number+".csv")

        available_items = pd.merge(predictions, item_data, how='inner', on=['recipe_id'])


        for ALPHA in ALPHAS:
            wu = []
            for index, row in available_items.iterrows():
                pred = row['pred']
                greenness = row['greenness']
                wu.append(pred * ALPHA + greenness * (1-ALPHA))

            available_items['weighted_utility'] = wu

            print(available_items[['pred', 'greenness', 'weighted_utility']])
            available_items[['id', 'user_id', 'recipe_id', 'rating', 'pred', 'greenness', 'weighted_utility']].to_csv(technique + "/predictions_"+technique+set_number+"_weighted_alpha="+str(ALPHA)+".csv")

