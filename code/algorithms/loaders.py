import pandas as pd

"""Reader for loading in Food RecSys Dataset"""
class FoodDataLoader:
    def __init__(self, interactions_path, items_path):
        """Constructor: initializes FoodDataReader instance

        Requires path of item information and path of interaction
        information

        Interactions require users, items and ratings
        """

        self.items_path = items_path
        self.interactions_path = interactions_path

        self.read_data()

    def read_data(self):
        """Reads data from paths and creates
        dataframes to store items and interactions
        """

        self.items_df = pd.read(self.items_path)
        self.interactions_df = pd.read(self.interactions_path)

    def merge_data(self, id):
        """Merges item and interaction data

        Requires id to merge on
        """

        self.full_data = pd.merge(self.interactions_df, self.items_df, how='inner', on=['recipe_id'])

    def read_and_merge_data(self, id):
        """Full reading and merging pipeline

        Requires id to merge on
        """
        self.read_data()
        self.merge_data(id)



"""Reader for loading in general recsys dataset

Assumes 1 file, with users, items and interactions
"""
class GeneralDataLoader:
    def __init__(self, interactions_path):
        """Constructor: initializes GeneralDataReader instance

        Requires path of interaction
        information

        Interactions require users, items and ratings
        """

        self.interactions_path = interactions_path
        self.read_data()

    def read_data(self):
        """Reads data from paths and creates
        dataframes to store interactions
        """

        self.interactions_df = pd.read_csv(self.interactions_path)[["user_id", "recipe_id", "rating"]]

    def split_data(self, train_ratio):
        test_recipes = []
        test_users = []
        test_ratings = []

        train = self.interactions_df
        orig_length = len(train)

        while(len(train)/orig_length > train_ratio):
            row = train.sample()
            r_id = row['recipe_id'].values[0]
            u_id = row['user_id'].values[0]
            print(len(train))
            oc_recipe = len(train[train['recipe_id'] == r_id])
            oc_user = len(train[train['user_id'] == u_id])

            if(oc_recipe > 1 and oc_user > 1):
                test_recipes.append(row['recipe_id'].values[0])
                test_users.append(row['user_id'].values[0])
                test_ratings.append(row['rating'].values[0])
                train = train.drop(row.index)

        result = pd.DataFrame(columns = ['user_id', 'recipe_id', 'rating'])
        result['recipe_id'] = test_recipes
        result['user_id'] = test_users
        result['rating'] = test_ratings

        result.to_csv("train_80_new.csv", index=False)
        train.to_csv("test_20_new.csv", index=False)

dl = GeneralDataLoader("../data/input/food_dataset/interactions_filtered_and_removed_by_mean_outliers_removed.csv")
dl.split_data(0.8)


