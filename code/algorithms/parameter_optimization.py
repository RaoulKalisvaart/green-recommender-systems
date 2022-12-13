from surprise import SVD
from surprise import Dataset
from surprise.model_selection import GridSearchCV
from surprise import Reader

reader = Reader(line_format='user item rating', sep=',')

data = Dataset.load_from_file("train_80_new.csv", reader=reader)
built_trainset = data.build_full_trainset()

param_grid = {'n_epochs': [20, 50, 80], 'lr_all': [0.1, 0.01, 0.001, 0.0001],
              'reg_all': [0.1, 0.01, 0.001, 0.0001], 'n_factors': [20, 50, 80]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5, n_jobs=-1)

gs.fit(data)

# best RMSE score
print(gs.best_score['rmse'])

# combination of parameters that gave the best RMSE score
print(gs.best_params['rmse'])