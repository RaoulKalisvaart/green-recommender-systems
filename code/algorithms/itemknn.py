from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd

class ItemKNN:
    def __init__(self, K):
        self.K = K
        self.model = NearestNeighbors()

    def train(self, trainset):
        # pivot and create movie-user matrix
        self.trainset = trainset
        self.movie_user_mat = trainset.pivot(
            index='recipe_id', columns='user_id', values='rating').fillna(0)

        #Create sparse matrix for speed
        self.movie_user_mat_sparse = csr_matrix(self.movie_user_mat.values)


        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model_knn.fit(self.movie_user_mat_sparse)


    def find_neighbours(self, id):
        query_index = self.movie_user_mat.index.tolist().index(id)
        original_id = self.movie_user_mat.iloc[query_index, :].values.reshape(1, -1)
        distances, indices = self.model_knn.kneighbors(original_id, n_neighbors=self.K+1)

        return distances, indices


    def predict(self, item_id, user_id):
        distances, indices = self.find_neighbours(item_id)
        item_ids = []

        for i in range(0, len(distances.flatten())):
            if i != 0:
                item_ids.append(self.movie_user_mat.index[indices.flatten()[i]])

        expected_user = self.trainset[self.trainset['user_id'] == user_id]
        boolean_series = expected_user.recipe_id.isin(item_ids)
        neighbours = expected_user[boolean_series]

        if(len(neighbours) == 0):
            return 1

        return neighbours['rating'].mean()







rs = ItemKNN(200)

train = pd.read_csv('old_results/train_80.csv')
test = pd.read_csv('old_results/test_20.csv')

rs.train(train)

predictions = []
for index, row in test.iterrows():
    pred = rs.predict(row['recipe_id'], row['user_id'])
    predictions.append(pred)

test['pred'] = predictions
test.to_csv("predictions_itemknn200.csv", index=False)