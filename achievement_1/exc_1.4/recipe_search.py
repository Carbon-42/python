import pickle


def display_recipe(recipe):
    print('')
    print('Recipe:', recipe['name'])
    print('Cooking Time:', recipe['cooking_time'], 'mins')
    print('Ingredients:')
    for ingredient in recipe['ingredients']:
        print('-', ingredient)
    print('Difficulty:', recipe['difficulty'])
    print('')


def search_ingredients(data):
    ingredients_list = data['all_ingredients']
    index_ingredients = list(enumerate(ingredients_list, 1))

    print('')
    for i in index_ingredients:
        print('No.', i[0], ' - ', i[1])

    print('')
    try:
        index = int(input('Select a number: ')) - 1
        ingredient_searched = ingredients_list[index]
    except IndexError:
        print('')
        print('That number is not in the list.')
    else:
        for recipe in data['recipes_list']:
            for ingredient in recipe['ingredients']:
                if ingredient == ingredient_searched:
                    print('')
                    print('These recipes include your searched ingredient')
                    print('----------------------------------------------')
                    display_recipe(recipe)


recipe_file_name = input(
    'Enter the file name where your recipes are saved. (must have .bin extension): ')

try:
    recipe_file = open(recipe_file_name, 'rb')
    data = pickle.load(recipe_file)
except FileNotFoundError:
    print('Error. Your file can not be found.')
else:
    search_ingredients(data)
