recipe_list = []
ingredients_list = []


def take_recipe():
    name = input('Enter the recipe name: ')
    cooking_time = int(input('Enter the cooking time (min): '))
    ingredients = input(
        'Enter the ingredients (separate with comma and space): ').split(', ')
    ingredients = [ingredient.title() for ingredient in ingredients]

    recipe = {
        'name': name.capitalize(),
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    return recipe


n = int(input('How many recipes would you like to enter? '))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipe_list.append(recipe)

for recipe in recipe_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) > 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'

    print('')
    print('Recipe:', recipe['name'])
    print('Cooking Time:', recipe['cooking_time'], 'mins')
    print('Ingredients:')
    for ingredient in recipe['ingredients']:
        print(' ', ingredient)
    print('Difficulty:', recipe['difficulty'])
    print('')


def print_ingredients():
    ingredients_list.sort()
    print('Ingredients Available from All Recipes')
    print('--------------------------------------')
    for ingredient in ingredients_list:
        print(ingredient)
    print('')


print_ingredients()
