class Recipe():
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficulty = None

    def calc_difficulty(self):
        num_ingredients = len(self.ingredients)
        if self.cooking_time < 10:
            if num_ingredients < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if num_ingredients < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def get_ingredients(self):
        return self.ingredients

    def add_ingredients(self, *ingredient):
        if not ingredient in self.ingredients:
            self.ingredients.extend(ingredient)
            self.update_all_ingredients(ingredient)

    def get_difficulty(self):
        if self.difficulty:
            return self.difficulty
        else:
            Recipe.calc_difficulty(self)

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self, ingredient):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        return f'\nRecipe name: {self.name}\nIngredients: {", ".join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}'

    def recipe_search(data, search_term):
        data = recipes_list
        for recipe in data:
            if recipe .search_ingredient(search_term):
                print(recipe)


tea = Recipe('Tea')
tea.add_ingredients('tea leaves', 'sugar', 'water')
tea.set_cooking_time(5)
tea.get_difficulty()

coffee = Recipe('Coffee')
coffee.add_ingredients('coffee powder', 'sugar', 'water')
coffee.set_cooking_time(5)
coffee.get_difficulty()

cake = Recipe('Cake')
cake.add_ingredients('sugar', 'butter', 'eggs',
                     'vanilla essence', 'flour', 'baking powder', 'milk')
cake.set_cooking_time(50)
cake.get_difficulty()

banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients(
    'bananas', 'milk', 'peanut butter', 'sugar', 'ice cubes')
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()

recipes_list = [tea, coffee, cake, banana_smoothie]

print('\nRecipes List')
print('------------')
for recipe in recipes_list:
    print(recipe)

search_ingredients = ['water', 'sugar', 'bananas']
for ingredient in search_ingredients:
    print(f'\nSearch results for recipes with "{ingredient}"')
    print('-----------------------------------------')
    Recipe.recipe_search(recipes_list, ingredient)
