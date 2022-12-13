from surprise import SVD
from surprise import Dataset
from surprise import Reader
import pandas as pd

class SVDClass:
    def train(self):
        reader = Reader(line_format='user item rating', sep=',')

        data = Dataset.load_from_file("old_results/train_80.csv", reader=reader)
        built_trainset = data.build_full_trainset()

        self.algo = SVD()
        self.algo.fit(built_trainset)

    def predict(self):
        test = pd.read_csv('old_results/test_set_Odette.csv')
        pred = []

        for index, row in test.iterrows():
            print(row)
            print(row[0])
            pred.append(self.algo.predict(str(row['user_id']), str(row['recipe_id'])).est)

        test['pred'] = pred
        test.to_csv("predictions_Papa.csv", index=False)


model = SVDClass()
model.train()
model.predict()