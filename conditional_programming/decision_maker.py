import json


with open('user_profile.json', 'r') as file:
    # Load JSON data from the file
    user_profile = json.load(file)

with open('user_stomach.json', 'r') as file:
    # Load JSON data from the file
    user_stomach = json.load(file)

with open('next_meal.json', 'r') as file:
    # Load JSON data from the file
    next_meal = json.load(file)


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



# with open('drug_effects.json', 'r') as file:
#     # Load JSON data from the file
#     drug_effects = json.load(file)


# ##Checking if any component of the meal might react with a drug
# def get_drug_reaction(food):
#     reactions = foods_db['drug_interactions'] ##A dictionary
#     return reactions

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





# def evaluate_all_nutrients(food, quantity, age, sex):
#     nutrient_values = foods_db[food]['nutrition-per-100g']
#     for nutrient in nutrient_values:
#         rda = get_recommended_daily_intake(age, sex, nutrient)
#         next_meal_nutrient
#         if ((foods_db[food]['nutrition-per-100g'][nutrient] * quantity /100) > rda) :
#             difference = (foods_db[food]['nutrition-per-100g'][nutrient] * quantity /100) - rda
#             print("You have exceeded your daily total {} by {}".format(nutrient, difference))        
#         elif ((foods_db[food]['nutrition-per-100g'][nutrient] * quantity /100) < rda) :
#               difference = abs((foods_db[food]['nutrition-per-100g'][nutrient] * quantity /100) - rda)
#               print("You are still within your daily total {} and need to meet up by {}".format(nutrient, difference))   
#         else:
#             print("You have met your nutrient allowance for {}. Consider waiting 24 hours before taking in more".format(nutrient))


def evaluate():
    total_calories = 0
    total_carbohydrates = 0
    total_protein = 0
    for food, quantity in user_stomach.items():
        total_calories += get_meal_calories(food, quantity)
        total_carbohydrates += get_meal_carbohydrate(food, quantity)
        total_protein += get_meal_protein(food, quantity)
        #compound_summary = get_meal_compounds(food)
        #drug_interaction_summary = get_drug_reaction(food)
    return total_calories, total_carbohydrates, total_protein
        

def get_recommended_daily_intake(age, sex, nutrient):
    recommended_daily_allowance = rda[nutrient][sex][age]
    return recommended_daily_allowance

def calculate_nutrient_over_intake(recommeded_daily_allowance , consumed_quantity, desired_quantity):
    intake = ((desired_quantity + consumed_quantity) - recommeded_daily_allowance)
    return intake


def get_user_bio_data(user_profile):
    age = user_profile['age']
    sex = user_profile['sex']
    return age, sex

def generate_report():
    eaten_total_calories, eaten_total_carbohydrates, eaten_total_protein = evaluate(user_stomach)
    next_meal_total_calories, next_meal_total_carbohydrates, next_meal_total_protein = evaluate(next_meal)
    age, sex = get_user_bio_data(user_profile)

    rda = get_recommended_daily_intake(age+'+y', sex, 'Carbohydrate')
    carb_intake = calculate_nutrient_over_intake(rda, eaten_total_carbohydrates, next_meal_total_carbohydrates)
  
    rda = get_recommended_daily_intake(age+'+y', sex, 'Protein')
    protein_intake = calculate_nutrient_over_intake(rda, eaten_total_protein, next_meal_total_protein)
    
    feedback = f"Based on what you age, gender, what you have eaten and what you want to eat, your intake for Carbohydate is {carb_intake}, your intake for protein is {protein_intake}"
    
    with open('report.txt', 'w') as file:  
        file.write(feedback)  

    return feedback


generate_report()


