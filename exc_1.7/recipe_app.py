# imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker


# initialize create_engine and assign to variable
engine = create_engine('mysql://cf-python:password@localhost/task_database')

# create Base class, holds sqlalchemy class properties


class Base(DeclarativeBase):
    pass


# create Session class and bind to engine
Session = sessionmaker(bind=engine)

# initialize Session and assign to variable
session = Session()

# create Recipe class and inherit Base class


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return '<Recipe ID: ' + str(self.id) + '-' + self.name + '-' + self.difficulty + '>'

    # class string method
    def __str__(self):
        return f"\nRecipe ID: {self.id}\n{'-'*30}\nName: {self.name}\nDifficulty: {self.difficulty}\nCooking Time: {self.cooking_time} minutes\n{'-'*30}\nIngredients:\n{self.ingredients}\n{'-'*30}"

    def calc_difficulty(cooking_time, recipe_ingredients):
        num_ingredients = len(recipe_ingredients)
        if int(cooking_time) < 10:
            if num_ingredients < 4:
                difficulty = "Easy"
            else:
                difficulty = "Medium"
        else:
            if num_ingredients < 4:
                difficulty = "Intermediate"
            else:
                difficulty = "Hard"
        return difficulty

    def return_ingredients_as_list(self):
        all_ingredients = []
        if not self.ingredients:
            return all_ingredients
        else:
            all_ingredients = self.ingredients.split(', ')
            return all_ingredients


# create Recipe model on database
Base.metadata.create_all(engine)

# define create_recipe funtion


def create_recipe():
    recipe_ingredients = []

    # validate name input
    valid_input_name = False
    while valid_input_name == False:
        name = input('\nEnter the recipe name: ')
        if len(name) < 50 and name.isnumeric() == False:
            valid_input_name = True

            # vaildate cooking_time input
            valid_cooking_time = False
            while valid_cooking_time == False:
                cooking_time = input('Enter the cooking time (mins): ')
                if cooking_time.isnumeric() == True:
                    valid_cooking_time = True
                else:
                    print('\nPlease enter a number: ')
        else:
            print('\nPlease enter a name with less than 50 letters.')

    # validate ingredients number input
    valid_num_ingredients = False
    while valid_num_ingredients == False:
        num_ingredients = input(
            '\nHow many ingredients would you like to enter? ')
        if num_ingredients.isnumeric() == True:
            valid_num_ingredients = True
            for i in range(int(num_ingredients)):

                # validate ingredients length
                valid_ingredient = False
                while valid_ingredient == False:
                    entry = input('\nEnter an ingredient: ')
                    recipe_ingredients.append(entry)
                    recipe_ingredients_str = ', '.join(recipe_ingredients)
                    x = len(recipe_ingredients_str)
                    if x <= 255:
                        valid_ingredient = True
                    else:
                        remaining_character_num = x - (2+len(i))
                        recipe_ingredients.remove(i)
                        print(
                            f'Error: Ingredients list can not exceed 255 characters. You have {remaining_character_num} characters remaining.')
        else:
            print('\nError: Please enter a valid number.')

    # calculate difficulty
    difficulty = Recipe.calc_difficulty(cooking_time, recipe_ingredients)

    recipe_entry = Recipe(
        name=name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredients_str,
        difficulty=difficulty
    )

    session.add(recipe_entry)
    session.commit()
    print('\nYour recipe has been saved in the database.')

# define view_all recipes function


def view_all_recipes():
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print('\nThere are no recipes in the database.')
        return None

    else:
        print('\nList of all recipes: ')
        print('-'*30)
        for recipe in all_recipes:
            print(recipe)

# define search_by _ingredients function


def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print('\nThere are no recipes in the database.')
        return None

    else:
        results = session.query(Recipe.ingredients).all()

    all_ingredients = []

    for recipe_ingredients in results:
        for ingredients in recipe_ingredients:
            ingredient = ingredients.split(', ')
            all_ingredients.extend(ingredient)

    all_ingredients = list(dict.fromkeys(all_ingredients))

    all_ingredients_list = list(enumerate(all_ingredients))

    print('\n')
    print('\nAll Ingredients List')
    print('='*40)

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0]+1) + '. ' + tup[1])

    try:
        search_nums_input = input(
            '\nSelect ingredients by numbers (separate with spaces): ')
        numbers_to_search = search_nums_input.split(' ')

        search_ingredients = []
        for i in numbers_to_search:
            index = int(i) - 1
            search_ingr = all_ingredients_list[index][1]
            search_ingredients.append(search_ingr)

        conditions = []
        for i in search_ingredients:
            like_term = '%' + i + '%'
            condition = Recipe.ingredients.like(like_term)
            conditions.append(condition)

        searched_recipes = session.query(Recipe).filter(*conditions).all()

        print('\nRecipes that match your search criteria')
        print('='*40)
        for recipe in searched_recipes:
            print(recipe)

    except:
        print('\nError: Your numbers were not in the list.')

# define edit_recipe function


def edit_recipe():
    if session.query(Recipe).count() == 0:
        print('\nThere are no recipes in the database.')
        return None

    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()

        print('\nList of available recipes.')
        print('-'*30)
        for i in results:
            print('\nID: ', i[0])
            print('Name: ', i[1])

    try:
        recipe_selection = int(
            (input('\nEnter the ID of the recipe you would like to edit: ')))
        recipe_to_edit = session.get(Recipe, recipe_selection)
        print('\n')
        print('-'*30)
        print('1. Name:', recipe_to_edit.name)
        print('2. Cooking Time:', recipe_to_edit.cooking_time)
        print('3. Ingredients:', recipe_to_edit.ingredients)

        attribute_column_to_edit = str(input(
            '\nWhich attribute # would you like to edit, 1, 2, or 3? '))

        if attribute_column_to_edit == '1':
            valid_input_name = False
            while valid_input_name == False:
                name = input('\nEnter the new recipe name: ')
                if len(name) < 50 and name.isnumeric() == False:
                    valid_input_name = True
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update(
                        {Recipe.name: name})
                    print('\nRecipe name updated to: ', name)
                else:
                    print('\nPlease enter a name with less than 50 letters.')

        elif attribute_column_to_edit == '2':
            valid_cooking_time = False
            while valid_cooking_time == False:
                cooking_time = input('Enter the cooking time (mins): ')
                if cooking_time.isnumeric() == True:
                    valid_cooking_time = True
                    difficulty = Recipe.calc_difficulty(
                        cooking_time, recipe_to_edit.ingredients)
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update(
                        {Recipe.cooking_time: cooking_time, Recipe.difficulty: difficulty})
                    print('\nRecipe cooking time updated to: ', cooking_time)
                else:
                    print('\nPlease enter a number: ')

        elif attribute_column_to_edit == '3':
            recipe_ingredients = []
            valid_num_ingredients = False
            while valid_num_ingredients == False:
                num_ingredients = input(
                    '\nHow many ingredients would you like to enter? ')
                if num_ingredients.isnumeric() == True:
                    valid_num_ingredients = True
                    for i in range(int(num_ingredients)):
                        valid_ingredient = False
                        while valid_ingredient == False:
                            entry = input('\nEnter an ingredient: ')
                            recipe_ingredients.append(entry)
                            recipe_ingredients_str = ', '.join(
                                recipe_ingredients)
                            x = len(recipe_ingredients_str)
                            if x <= 255:
                                valid_ingredient = True
                            else:
                                print('recipe_ingredients_str', x)
                                print('entry', len(entry))
                                remaining_character_num = (
                                    len(entry) - (x - 255))
                                print('rem_chara', remaining_character_num)
                                recipe_ingredients.remove(entry)
                                print(
                                    f'Error: Ingredients list can not exceed 255 characters. You have {remaining_character_num} characters remaining.')
                    difficulty = Recipe.calc_difficulty(
                        recipe_to_edit.cooking_time, recipe_ingredients)
                    session.query(Recipe).filter(Recipe.id == recipe_to_edit.id).update(
                        {Recipe.ingredients: recipe_ingredients_str, Recipe.difficulty: difficulty})
                    print('\nRecipe ingredients updated to: ', recipe_ingredients)
                else:
                    print('\nError: Please enter a valid number.')
        else:
            print('\nError: Your number was not in the list. Please try again.')
        session.commit()
    except:
        print('\nError: Your number was not in the list. Please try again.')
        return None


# define delete_recipe function
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print('\nThere are no recipes in the database.')
        return None

    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()

        print('\nList of available recipes.')
        print('-'*30)
        for i in results:
            print('\nID: ', i[0])
            print('Name: ', i[1])

    try:
        recipe_selection = int(
            (input('\nEnter the ID of the recipe you would like to delete: ')))
        recipe_to_delete = session.get(Recipe, recipe_selection)
        print(recipe_to_delete)
        confirm_deletion = input(
            '\nYou are about to delete this recipe. Are you sure? (y/n): ')
        if confirm_deletion == 'y':
            session.delete(recipe_to_delete)
            session.commit()
            print('\n', recipe_to_delete.name, 'deleted.')
        else:
            return None

    except:
        return None

# define main_main function


def main_menu():
    choice = ''
    while (choice != 'quit'):
        print('\n')
        print('\nMain Menu\n' + '='*40 + '\nMake a selection:')
        print('1. Create a Recipe')
        print('2. View All Recipes')
        print('3. Search a Recipes by Ingredients ')
        print('4. Edit a Recipe ')
        print('5. Delete a Recipe')
        print('Type "quit" to exit the program.')
        print('='*40)
        choice = input('\nYour selection: ')

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        else:
            if choice == 'quit':
                print('\nBye')
            else:
                print('\nError: Please select a valid option.')


main_menu()

session.close()
