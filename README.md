# Green Recommender Systems
Code and data used in the paper: _Towards Carbon Footprint-Aware Recommender Systems for Greener
Item Recommendation_

## Dataset
The dataset in this repository contains greenness scores of recipes (i.e. scores describing their sustainability), originating from the Food.com dataset. The paper describes in depth how the dataset was constructed.

This repository does not contain the original Food.com dataset, that we used to build our dataset on. That dataset, which includes the user-item ratings, can be found here: https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions

The dataset created in our paper, the RecipeEmissions dataset, is structured in two csv files:
* ingredients_CO2_greenness.csv: this file contains recipe IDs (corresponding to the original Food.com dataset), along with their estimated CO2-eq value and calculated greenness.
* recipe_information.csv: this file contains the recipe information used to calculate the total CO2-eq (e.g. the used ingredients, their quantities and standardized parts).
