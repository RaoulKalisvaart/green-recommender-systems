from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
import time

def url_generator(recipe_name, recipe_id, pre_string):
    recipe_tokens = recipe_name.split()
    url = "https://www.food.com/" + pre_string + "/"
    for token in recipe_tokens:
        url += (token)
        url += ("-")
    url = url + str(recipe_id)
    print(url)
    return url

def evaluator(ingredient):
    total = 0
    items = ingredient.text.split()
    if("-" in items):
        dash = items.index("-")
        items = items[0:dash]
    for item in items:
        value =  eval(compile(item.replace("⁄", "/"), "<string>", "eval"))
        if(value > 0):
            total += value
    return total

def parts_mapper(part):
    return part.text.replace(',', '')

def scraper(url):
    html_doc = get(url, headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    ingredients = soup.find_all("div", {"class": "recipe-ingredients__ingredient-quantity"})
    parts = soup.find_all("div", {"class": "recipe-ingredients__ingredient-parts"})
    return (list(map(evaluator, ingredients)), list(map(parts_mapper, parts)))

pp_recipes = pd.read_csv("archive/PP_recipes.csv")
raw_recipes = pd.read_csv("archive/RAW_recipes.csv")
most_used = pd.read_csv("recipes_with_enough_ratings_final.csv")

most_used_recipes = pd.merge(pp_recipes, most_used, on=['id', 'id'])
print(most_used_recipes)
recipes = pd.merge(most_used_recipes, raw_recipes, on=['id','id'])

column_names = ["recipe_id", "ingredients", "quantities", "parts"]
quantity_data = pd.DataFrame(columns = column_names)

quantity_data['recipe_id'] = recipes['id']
print(quantity_data)

quantity_data['ingredients'] = quantity_data['ingredients'].astype(object)
quantity_data['quantities'] = quantity_data['quantities'].astype(object)
quantity_data['parts'] = quantity_data['parts'].astype(object)
print(quantity_data.dtypes)

count = 0

for index, row in recipes.iterrows():
    id = row['id']
    name = row['name']
    ingredient_ids = row['ingredient_ids']
    url = url_generator(name, id, "recipe")
    scraper_output = scraper(url)
    quantities = scraper_output[0]
    parts = scraper_output[1]
    if(len(quantities) == 0):
        url = url_generator(name, id, "about")
        quantities = scraper(url)
        if(len(quantities) == 0):
            print("error" + name)

    quantity_data.loc[quantity_data['recipe_id'] == id, 'ingredients'] = ingredient_ids
    quantity_data.loc[quantity_data['recipe_id'] == id, 'quantities'] = pd.Series([quantities] * quantity_data.shape[0])
    quantity_data.loc[quantity_data['recipe_id'] == id, 'parts'] = pd.Series([parts] * quantity_data.shape[0])

    count = count + 1
    if(count > 99):
        quantity_data.to_csv("quantity_data.csv")

quantity_data.to_csv("quantity_data.csv")

# ingredients = pd.read_csv("all_used_ingredients.csv")
# print(ingredients[ingredients["ingr_id"] == 7557]['ingr_name'])






