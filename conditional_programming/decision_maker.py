import json

final_recommendation_report = ''
user_profile = {} ##Age and Sex
user_stomach = {} ##Contains consumed foods
next_meal = {} ###Contains the food a user is about to eat

with open('foods.json', 'r') as file:
    # Load JSON data from the file
    foods_db = json.load(file)


with open('recommended_daily_allowance.json', 'r') as file:
    # Load JSON data from the file
    rda = json.load(file)


with open('compounds.json', 'r') as file:
    # Load JSON data from the file
    compounds = json.load(file)

with open('compound_health_effects.json', 'r') as file:
    # Load JSON data from the file
    compound_health_effects = json.load(file)


with open('drug_effects.json', 'r') as file:
    # Load JSON data from the file
    drug_effects = json.load(file)



##Checking if any component of the meal might react with a drug
def get_drug_reaction(food):
    reactions = foods_db['drug_interactions'] ##A dictionary
    return reactions


def get_meal_compounds(food):
    return


def get_meal_calories(food, quantity):
    calories = 0
    calories = (foods_db[food]['nutrition-per-100g']['energy']) * quantity / 100
    return calories

def get_meal_protein(food, quantity):
    protein = 0
    protein = (foods_db[food]['nutrition-per-100g']['protein']) * quantity / 100
    return protein

def get_meal_carbohydrate(food, quantity):
    carbohydrate = 0
    carbohydrate = (foods_db[food]['nutrition-per-100g']['carbohydrate']) * quantity / 100
    return carbohydrate

def evaluate_stomach(user_stomach):
    total_calories = 0
    total_carbohydrates = 0
    total_protein = 0
    compound_summary =''
    drug_interaction_summary = ''
    for food, quantity in user_stomach:
        total_calories += get_meal_calories(food, quantity)
        total_carbohydrates += get_meal_carbohydrate(food, quantity)
        total_protein += get_meal_protein(food, quantity)
        compound_summary = get_meal_compounds(food)
        drug_interaction_summary = get_drug_reaction(food)
    return total_calories, total_carbohydrates, total_protein, compound_summary, drug_interaction_summary
        

def get_recommended_daily_intake(age, sex, nutrient):
    recommended_daily_allowance = rda[nutrient][sex][age]
    return recommended_daily_allowance

def calculate_nutrient_over_intake(recommeded_daily_allowance , consumed_quantity, desired_quantity):
    over_intake = abs((desired_quantity + consumed_quantity) - recommeded_daily_allowance)
    return over_intake

def calculate_nutrient_under_intake(recommeded_daily_allowance, consumed_quantuty, desired_quantity):
    under_intake = abs((desired_quantity + consumed_quantuty) - recommeded_daily_allowance)
    return under_intake


def get_user_bio_data(age, sex):
    user_profile['age'] = age
    user_profile['sex'] = sex
    return

def get_stomach_contents():
    return

def get_desired_meal():
    return

