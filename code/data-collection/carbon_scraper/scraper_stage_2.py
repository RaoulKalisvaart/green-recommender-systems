import pandas as pd

# ing_1 = pd.read_csv("scraped_ingredients.csv")
# ing_2 = pd.read_csv("scraped_ingredients2.csv")
# ing_3 = pd.read_csv("scraped_ingredients3.csv")
# ing_4 = pd.read_csv("scraped_ingredients4.csv")
#
# frames = [ing_1, ing_2, ing_3, ing_4]
# result = pd.concat(frames)
#
# result.to_csv("scraped_ingredients_combined.csv")

ing = pd.read_csv("ingredients_in_used_recipes.csv")

filter = ing[ing['url'] == "Not found"]
# n = 10
# print(filter['ingr_name'].value_counts()[:n].index.tolist())
# print(filter['ingr_name'].value_counts()[:n])
print(filter['ingr_name'].str.split().str[-1].value_counts().head(40))

for index, row in ing.iterrows():
    name = row['ingr_name']
    last = name.split()[-1]
    first = name.split()[0]
    url = row['url']
    if(last == 'juice' and url == "Not found"):
        print(url + " " + last)
        ing.at[index, 'CO2'] = 0
        ing.at[index, 'url'] = "removed"

ing.to_csv("ingredients_in_used_recipes.csv")

#rice
#beans

#op eerste veranderd: chicken, turkey, tuna (even goed naar kijken, bijvoorbeeld seasoning).


#######################################################


