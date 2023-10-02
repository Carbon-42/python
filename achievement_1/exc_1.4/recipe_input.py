import pickle

recipes_list = []
all_ingredients = []


def take_recipe():
    name = input('Enter the recipe name: ')
    cooking_time = int(input('Enter the cooking time (min): '))
    ingredients = input(
        'Enter the ingredients (separate with comma and space): ').split(', ')
    ingredients = [ingredient.title() for ingredient in ingredients]

    recipe = {
        'name': name.capitalize(),
        'cooking_time': cooking_time,
        'ingredients': ingredients,
    }
    difficulty = calc_difficulty(recipe)
    return recipe


def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'


try:
    recipe_file_name = input(
        'Enter the file name where your recipes are saved. (must have .bin extension): ')
    recipe_file = open(recipe_file_name, 'rb')
    data = pickle.load(recipe_file)

except FileNotFoundError:
    print('File not found. Creating new one.')
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    print('Error unknown. Creating new file.')
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    recipe_file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']


n = int(input('How many recipes would you like to enter? '))

for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe['ingredients']:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

print('Your data has been saved to: ', recipe_file_name)
new_file = open(recipe_file_name, 'wb')
pickle.dump(data, new_file)
new_file.close()
