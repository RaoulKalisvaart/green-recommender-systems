import pandas as pd
import math
import statistics

class GNDCGCalculator:
    def __init__(self, data):
        self.data = data

    def calculateGIDCG(self, length):
        ranking = self.data.copy()
        ranking = ranking.sort_values('greenness', ascending=False).head(length).reset_index()
        GIDCG = 0
        for index, row in ranking.iterrows():
            greenness = row["greenness"]

            nom = pow(2, greenness) - 1
            denom = math.log2(index + 2)


            GIDCG = GIDCG + (nom / denom)

        GIDCG = GIDCG / length
        return GIDCG

    def calculateGNDCG(self, length):
        ranking = self.data.copy()
        ranking = ranking.sort_values('weighted_utility', ascending=False).head(length).reset_index()

        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #     print(ranking)

        GDCG = 0

        for index, row in ranking.iterrows():
            if(row.empty):
                continue

            current_item = row["greenness"]


            greenness = current_item

            nom = pow(2, greenness) - 1
            denom = math.log2(index + 2)

            GDCG = GDCG + (nom/denom)

        GDCG = GDCG / length

        GIDCG = self.calculateGIDCG(length)
        GNDCG = GDCG/GIDCG

        return GNDCG


splits = pd.read_csv("../separating_data/splits.csv", index_col=0).transpose()

ALPHAS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
techniques = ["GlobalAverage"]
NUMBERS = [""]

for technique in techniques:
    for set_number in NUMBERS:
        GNDCG_per_alpha = []

        for alpha in ALPHAS:
            df = pd.read_csv(technique+"/predictions_"+technique+set_number+"_weighted_alpha="+str(alpha)+".csv")
            GNDCG_arrays = []

            for i in range(0, 495):
                current_split = splits[i]
                merged = pd.merge(df, current_split, left_on='id', right_on=i)
                calc = GNDCGCalculator(merged)
                calculated_GNDCG = calc.calculateGNDCG(20)
                GNDCG_arrays.append(calculated_GNDCG)

            median = statistics.median(GNDCG_arrays)
            GNDCG_per_alpha.append(median)

        GNDCG_df = pd.DataFrame()
        GNDCG_df["alpha"] = ALPHAS
        GNDCG_df["GNDCG"] = GNDCG_per_alpha

        GNDCG_df.to_csv(technique+"/GNDCG_"+technique+set_number+".csv", index=False)

        print(ALPHAS)
        print(GNDCG_per_alpha)

