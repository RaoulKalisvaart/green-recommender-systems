import pandas as pd
import math
import statistics

class NDCGCalculator:
    def __init__(self, data):
        self.data = data

    def calculateIDCG(self, length):
        ranking = self.data.copy()
        ranking = ranking.sort_values('rating', ascending=False).head(length).reset_index()
        IDCG = 0
        # print(ranking)
        for index, row in ranking.iterrows():
            exp = row["rating"]

            nom = pow(2, exp) - 1
            denom = math.log2(index + 2)


            IDCG = IDCG + (nom / denom)

        IDCG = IDCG / length
        return IDCG

    def calculateNDCG(self, length):
        ranking = self.data.copy()
        ranking = ranking.sort_values('weighted_utility', ascending=False).head(length).reset_index()

        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #     print(ranking)

        DCG = 0

        for index, row in ranking.iterrows():
            if(row.empty):
                continue

            current_item = row["rating"]


            exp = current_item

            nom = pow(2, exp) - 1
            denom = math.log2(index + 2)

            DCG = DCG + (nom/denom)

        DCG = DCG / length

        IDCG = self.calculateIDCG(length)
        NDCG = DCG/IDCG

        return NDCG


splits = pd.read_csv("../separating_data/splits2.csv", index_col=0).transpose()

ALPHAS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# ALPHAS = [1]

# techniques = ["GlobalAverage", "SVD", "SVDpp", "CoClustering"]
# NUMBERS = ["1", "2"]

techniques = ["userKNN", "itemKNN"]
NUMBERS = ["", "1", "2"]

for technique in techniques:
    for set_number in NUMBERS:
        NDCG_per_alpha = []
        for alpha in ALPHAS:
            df = pd.read_csv(technique+"/predictions_"+technique+set_number+"_weighted_alpha="+str(alpha)+".csv")
            NDCG_arrays = []

            for i in range(0, 495):
                current_split = splits[i]
                merged = pd.merge(df, current_split, left_on='id', right_on=i)
                calc = NDCGCalculator(merged)
                calculated_NDCG = calc.calculateNDCG(20)
                NDCG_arrays.append(calculated_NDCG)

            median = statistics.median(NDCG_arrays)
            NDCG_per_alpha.append(median)

        NDCG_df = pd.DataFrame()
        NDCG_df["alpha"] = ALPHAS
        NDCG_df["NDCG"] = NDCG_per_alpha

        NDCG_df.to_csv(technique+"/NDCG_"+technique+set_number+".csv", index=False)

        print(ALPHAS)
        print(NDCG_per_alpha)

