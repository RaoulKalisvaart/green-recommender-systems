from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
import pandas as pd

class UserKNN:
    def __init__(self, K):
        self.K = K
        self.model = NearestNeighbors()

    def train(self, trainset):
        # pivot and create movie-user matrix
        self.trainset = trainset
        self.movie_user_mat = trainset.pivot(
            index='user_id', columns='recipe_id', values='rating').fillna(0)

        #Create sparse matrix for speed
        self.movie_user_mat_sparse = csr_matrix(self.movie_user_mat.values)


        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model_knn.fit(self.movie_user_mat_sparse)


    def find_neighbours(self, id):
        query_index = self.movie_user_mat.index.tolist().index(id)
        # print(query_index)
        original_id = self.movie_user_mat.iloc[query_index, :].values.reshape(1, -1)
        # print(original_id)
        distances, indices = self.model_knn.kneighbors(original_id, n_neighbors=self.K+1)

        # for i in range(0, len(distances.flatten())):
        #     if i == 0:
        #         print('Recommendations for {0}:\n'.format(self.movie_user_mat.index[query_index]))
        #     else:
        #         print('{0}: {1}, with distance of {2}:'.format(i, self.movie_user_mat.index[indices.flatten()[i]],
        #                                                        distances.flatten()[i]))

        return distances, indices


    def predict(self, item_id, user_id):
        distances, indices = self.find_neighbours(user_id)
        user_ids = []

        for i in range(0, len(distances.flatten())):
            if i != 0:
                user_ids.append(self.movie_user_mat.index[indices.flatten()[i]])

        expected_recipe = self.trainset[self.trainset['recipe_id'] == item_id]
        boolean_series = expected_recipe.user_id.isin(user_ids)
        neighbours = expected_recipe[boolean_series]

        if(len(neighbours) == 0):
            return 1

        return neighbours['rating'].mean()







# dl = GeneralDataLoader("../data/input/food_dataset/just_interactions.csv")
rs = UserKNN(200)

# train, test = train_test_split(dl.interactions_df, test_size=0.05)
#

train = pd.read_csv('old_results/train_80.csv')
test = pd.read_csv('old_results/test_20.csv')

rs.train(train)

predictions = []
for index, row in test.iterrows():
    pred = rs.predict(row['recipe_id'], row['user_id'])
    predictions.append(pred)

test['pred'] = predictions
test.to_csv("predictions_userknn200.csv", index=False)