import mysql.connector

# import sys
# print(sys.version)exit

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    password='password'
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)
)''')


def main_menu(conn, cursor):
    choice = ''
    while (choice != 'quit'):
        print('\nMain Menu' + '\n======================' + '\nMake a selection:')
        print('1. Create a Recipe')
        print('2. Search a Recipe')
        print('3. Update a Recipe')
        print('4. Delete a Recipe')
        print('5. View All Recipes')
        print('Type "quit" to exit the program.')
        choice = input('\nYour selection: ')

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            view_all_recipes(conn, cursor)


def create_recipe(conn, cursor):
    name = str(input('\nEnter the recipe name: '))
    cooking_time = int(input('Enter the cooking time (mins): '))
    ingredients = input(
        'Enter the ingredients (separate with comma and space): ').split(', ')
    ingredients = [ingredient.title() for ingredient in ingredients]
    difficulty = calc_difficulty(cooking_time, ingredients)
    ingredients_str = ', '.join(ingredients)
    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print('Recipe saved to database.')


def calc_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10:
        if num_ingredients < 4:
            difficulty = "Easy"
        else:
            difficulty = "Medium"
    else:
        if num_ingredients < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
    # print('Difficulty: ', difficulty)
    return difficulty


def search_recipe(conn, cursor):
    all_ingredients = []
    cursor.execute('SELECT ingredients FROM Recipes')
    results = cursor.fetchall()
    for recipe_ingredients in results:
        for ingredients in recipe_ingredients:
            ingredient = ingredients.split(', ')
            all_ingredients.extend(ingredient)

    all_ingredients = list(dict.fromkeys(all_ingredients))

    all_ingredients_list = list(enumerate(all_ingredients))

    print('\nAll Ingredients List')
    print('--------------------')

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0]+1) + '. ' + tup[1])

    try:
        index = int(input('Select a number: ')) - 1
        ingredient_searched = all_ingredients_list[index][1]
    except IndexError:
        print('')
        print('That number is not in the list.')
    else:
        cursor.execute('SELECT* FROM Recipes WHERE ingredients LIKE %s',
                       ('%' + ingredient_searched + '%',))
        recipes_with_ingredient_searched = cursor.fetchall()

        print('\nThese recipes include your searched ingredient')
        print('----------------------------------------------')
        for row in recipes_with_ingredient_searched:
            print('\nID: ', row[0])
            print('Name: ', row[1])
            print('Ingredients: ', row[2])
            print('Cooking Time (mins): ', row[3])
            print('Difficulty: ', row[4])


def update_recipe(conn, cursor):
    view_all_recipes(conn, cursor)

    recipe_id_to_update = int(
        (input('\nEnter the ID of the recipe you would like to update: ')))
    attribute_column_to_update = str(input(
        '\nWhich attribute would you like to update, "name", "cooking_time", or "ingredients"? '))

    updated_attribute = input('\nEnter the new value: ')

    if attribute_column_to_update == 'name':
        cursor.execute('UPDATE Recipes SET name = %s WHERE id = %s',
                       (updated_attribute, recipe_id_to_update))
        print('Name updated to:', updated_attribute)
    elif attribute_column_to_update == 'cooking_time':
        cursor.execute('UPDATE Recipes SET cooking_time = %s WHERE id = %s',
                       (updated_attribute, recipe_id_to_update))
        print('Cooking Time updated to:', updated_attribute)
        cursor.execute('SELECT * FROM Recipes WHERE id = %s',
                       (recipe_id_to_update, ))
        recipe_to_update = cursor.fetchall()

        ingredients = tuple(recipe_to_update[0][2].split(','))
        cooking_time = recipe_to_update[0][3]

        updated_difficulty = calc_difficulty(cooking_time, ingredients)
        cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s',
                       (updated_difficulty, recipe_id_to_update))
    elif attribute_column_to_update == 'ingredients':
        cursor.execute('UPDATE Recipes SET ingredients = %s WHERE id = %s',
                       (updated_attribute, recipe_id_to_update))
        print('Ingredients updated to:', updated_attribute)
        cursor.execute('SELECT * FROM Recipes WHERE id = %s',
                       (recipe_id_to_update, ))
        recipe_to_update = cursor.fetchall()

        ingredients = tuple(recipe_to_update[0][2].split(','))
        cooking_time = recipe_to_update[0][3]

        updated_difficulty = calc_difficulty(cooking_time, ingredients)
        cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s',
                       (updated_difficulty, recipe_id_to_update))

    conn.commit()


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)

    recipe_to_delete = int(
        (input('\nEnter the ID of the recipe you would like to delete: ')))

    cursor.execute('DELETE FROM Recipes WHERE id = %s', (recipe_to_delete, ))

    conn.commit()
    print('\nThe recipe has been deleted.')


def view_all_recipes(conn, cursor):
    cursor.execute('SELECT * FROM Recipes')
    all_recipes = cursor.fetchall()

    print('\nRecipe List')
    print('------------')
    for row in all_recipes:
        print('\nID: ', row[0])
        print('Name: ', row[1])
        print('Ingredients: ', row[2])
        print('Cooking Time (mins): ', row[3])
        print('Difficulty: ', row[4])


main_menu(conn, cursor)
