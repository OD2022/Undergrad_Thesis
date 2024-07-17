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


def get_meal_compounds(food):
    if (foods_db[food]['compounds']) is not None:
        food_compounds = foods_db[food]['compounds']
        #for compound in food_compounds:
            #do some
    return


def get_meal_calories(food, quantity):
    energy = 0
    if (foods_db[food]['nutrition-per-100g']['energy']) is not None:
        energy = (foods_db[food]['nutrition-per-100g']['energy']) * quantity / 100
    return energy

def get_meal_protein(food, quantity):
    protein = 0
    if (foods_db[food]['nutrition-per-100g']['protein']) is not None:
        protein = (foods_db[food]['nutrition-per-100g']['protein']) * quantity / 100
    return protein

def get_meal_carbohydrate(food, quantity):
    carbohydrate = 0
    if (foods_db[food]['nutrition-per-100g']['carbohydrate']) is not None:
        carbohydrate = (foods_db[food]['nutrition-per-100g']['carbohydrate']) * quantity / 100
    return carbohydrate


def get_meal_moisture(food, quantity):
    moisture = 0
    if (foods_db[food]['nutrition-per-100g']['moisture']) is not None:
        moisture = (foods_db[food]['nutrition-per-100g']['moisture']) * quantity / 100
    return moisture

def get_meal_calcium(food, quantity):
    calcium = 0
    if (foods_db[food]['nutrition-per-100g']['calcium']) is not None:
        calcium = (foods_db[food]['nutrition-per-100g']['calcium']) * quantity / 100
    return calcium

def get_meal_sodium(food, quantity):
    sodium = 0
    if (foods_db[food]['nutrition-per-100g']['sodium']) is not None:
        sodium = (foods_db[food]['nutrition-per-100g']['sodium']) * quantity / 100
    return sodium

def get_meal_dietary_fibre(food, quantity):
    fibre = 0
    if (foods_db[food]['nutrition-per-100g']['dietary-fibre']) is not None:
        fibre = (foods_db[food]['nutrition-per-100g']['dietary-fibre']) * quantity / 100
    return fibre

def get_meal_polyunsaturated_fat(food, quantity):
    unsaturated_fat = 0
    if (foods_db[food]['nutrition-per-100g']['polyunsaturated-fat']) is not None:
        unsaturated_fat = (foods_db[food]['nutrition-per-100g']['polyunsaturated-fat']) * quantity / 100
    return unsaturated_fat


def get_meal_monounsaturated_fat(food, quantity):
    unsaturated_fat = 0
    if (foods_db[food]['nutrition-per-100g']['monounsaturated-fat']) is not None:
        unsaturated_fat = (foods_db[food]['nutrition-per-100g']['monounsaturated-fat']) * quantity / 100
    return unsaturated_fat


def get_meal_saturated_fat(food, quantity):
    saturated_fat = 0
    if (foods_db[food]['nutrition-per-100g']['saturated_fat']) is not None:
        saturated_fat = (foods_db[food]['nutrition-per-100g']['saturated_fat']) * quantity / 100
    return saturated_fat

def get_meal_fat(food, quantity):
    fat = 0
    if (foods_db[food]['nutrition-per-100g']['fat']) is not None:
       fat = (foods_db[food]['nutrition-per-100g']['fat']) * quantity / 100
    return fat

def get_meal_sugars(food, quantity):
    sugars = 0
    if (foods_db[food]['nutrition-per-100g']['sugars']) is not None:
        sugars = (foods_db[food]['nutrition-per-100g']['sugars']) * quantity / 100
    return sugars

def get_meal_copper(food, quantity):
    copper = 0
    if (foods_db[food]['nutrition-per-100g']['copper']) is not None:
        copper = (foods_db[food]['nutrition-per-100g']['copper']) * quantity / 100
    return copper

def get_meal_iron(food, quantity):
    iron = 0
    if (foods_db[food]['nutrition-per-100g']['iron']) is not None:
        iron = (foods_db[food]['nutrition-per-100g']['iron']) * quantity / 100
    return iron

def get_meal_zinc(food, quantity):
    zinc = 0
    if (foods_db[food]['nutrition-per-100g']['zinc']) is not None:
        zinc = (foods_db[food]['nutrition-per-100g']['zinc']) * quantity / 100
    return zinc

def get_meal_potassium(food, quantity):
    potassium = 0
    if (foods_db[food]['nutrition-per-100g']['potassium']) is not None:
        potassium = (foods_db[food]['nutrition-per-100g']['potassium']) * quantity / 100
    return potassium

def get_meal_manganese(food, quantity):
    manganese = 0
    if (foods_db[food]['nutrition-per-100g']['manganese']) is not None:
        manganese = (foods_db[food]['nutrition-per-100g']['manganese']) * quantity / 100
    return manganese


def get_meal_magnesium(food, quantity):
    magnesium = 0
    if (foods_db[food]['nutrition-per-100g']['magnesium']) is not None:
        magnesium = (foods_db[food]['nutrition-per-100g']['magnesium']) * quantity / 100
    return magnesium



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
    total_zinc = 0
    total_sugars = 0
    total_fat = 0
    total_sodium = 0
    total_potassium = 0
    total_dietary_fibre = 0
    total_calcium = 0
    total_monounsaturated_fat = 0
    total_polyunsaturated_fat = 0
    total_manganese = 0
    total_magnesium = 0
    total_copper = 0
    total_moisture = 0
    total_saturated_fat = 0
    total_iron = 0

    for food, quantity in user_stomach.items():
        total_calories += get_meal_calories(food, quantity)
        total_carbohydrates += get_meal_carbohydrate(food, quantity)
        total_protein += get_meal_protein(food, quantity)
        total_zinc += get_meal_zinc(food, quantity)
        total_sugars += get_meal_sugars(food, quantity)
        total_fat += get_meal_fat(food, quantity)
        total_sodium += get_meal_sodium(food, quantity)
        total_potassium += get_meal_potassium(food, quantity)
        total_dietary_fibre += get_meal_dietary_fibre(food, quantity)
        total_calcium += get_meal_calcium(food, quantity)
        total_monounsaturated_fat += get_meal_monounsaturated_fat(food, quantity)
        total_polyunsaturated_fat += get_meal_polyunsaturated_fat(food, quantity)
        total_manganese += get_meal_manganese(food, quantity)
        total_magnesium += get_meal_magnesium(food, quantity)
        total_copper += get_meal_copper(food, quantity)
        total_iron += get_meal_iron(food, quantity)
        total_moisture += get_meal_moisture(food, quantity)
        total_saturated_fat += get_meal_saturated_fat(food, quantity)       
    return total_calories, total_carbohydrates, total_protein, total_zinc, total_sugars, total_fat, total_sodium, total_potassium, total_dietary_fibre, total_calcium, total_monounsaturated_fat, total_polyunsaturated_fat, total_manganese, total_magnesium, total_copper, total_moisture, total_saturated_fat, total_iron
        

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
    # Evaluate total nutrients consumed from user_stomach
    (eaten_total_calories, eaten_total_carbohydrates, eaten_total_protein, eaten_total_zinc,
     eaten_total_sugars, eaten_total_fat, eaten_total_sodium, eaten_total_potassium,
     eaten_total_dietary_fibre, eaten_total_calcium, eaten_total_monounsaturated_fat,
     eaten_total_polyunsaturated_fat, eaten_total_manganese, eaten_total_magnesium,
     eaten_total_copper, eaten_total_moisture, eaten_total_saturated_fat, eaten_total_iron) = evaluate()

    # Evaluate total nutrients expected from next_meal
    (next_meal_total_calories, next_meal_total_carbohydrates, next_meal_total_protein, 
     next_meal_total_zinc, next_meal_total_sugars, next_meal_total_fat, next_meal_total_sodium,
     next_meal_total_potassium, next_meal_total_dietary_fibre, next_meal_total_calcium,
     next_meal_total_monounsaturated_fat, next_meal_total_polyunsaturated_fat,
     next_meal_total_manganese, next_meal_total_magnesium, next_meal_total_copper,
     next_meal_total_moisture, next_meal_total_saturated_fat, next_meal_total_iron) = evaluate(next_meal)

    # Get age and sex from user_profile
    age, sex = get_user_bio_data(user_profile)

    # Prepare feedback for each nutrient category
    nutrients_feedback = []

    # Carbohydrates
    rda_carb = get_recommended_daily_intake(f"{age}y", sex, 'Carbohydrate')
    carb_intake = calculate_nutrient_over_intake(rda_carb, eaten_total_carbohydrates, next_meal_total_carbohydrates)
    if carb_intake > 0:
        nutrients_feedback.append(f"Carbohydrates: Exceeded daily intake by {carb_intake}")
    elif carb_intake < 0:
        nutrients_feedback.append(f"Carbohydrates: Need to meet daily intake by {-carb_intake}")
    else:
        nutrients_feedback.append(f"Carbohydrates: Met daily intake")

    # Protein
    rda_protein = get_recommended_daily_intake(f"{age}y", sex, 'Protein')
    protein_intake = calculate_nutrient_over_intake(rda_protein, eaten_total_protein, next_meal_total_protein)
    if protein_intake > 0:
        nutrients_feedback.append(f"Protein: Exceeded daily intake by {protein_intake}")
    elif protein_intake < 0:
        nutrients_feedback.append(f"Protein: Need to meet daily intake by {-protein_intake}")
    else:
        nutrients_feedback.append(f"Protein: Met daily intake")

    # Zinc
    rda_zinc = get_recommended_daily_intake(f"{age}y", sex, 'Zinc')
    zinc_intake = calculate_nutrient_over_intake(rda_zinc, eaten_total_zinc, next_meal_total_zinc)
    if zinc_intake > 0:
        nutrients_feedback.append(f"Zinc: Exceeded daily intake by {zinc_intake}")
    elif zinc_intake < 0:
        nutrients_feedback.append(f"Zinc: Need to meet daily intake by {-zinc_intake}")
    else:
        nutrients_feedback.append(f"Zinc: Met daily intake")

    # Sugars
    rda_sugars = get_recommended_daily_intake(f"{age}y", sex, 'Sugars')
    sugars_intake = calculate_nutrient_over_intake(rda_sugars, eaten_total_sugars, next_meal_total_sugars)
    if sugars_intake > 0:
        nutrients_feedback.append(f"Sugars: Exceeded daily intake by {sugars_intake}")
    elif sugars_intake < 0:
        nutrients_feedback.append(f"Sugars: Need to meet daily intake by {-sugars_intake}")
    else:
        nutrients_feedback.append(f"Sugars: Met daily intake")

    # Fat
    rda_fat = get_recommended_daily_intake(f"{age}y", sex, 'Fat')
    fat_intake = calculate_nutrient_over_intake(rda_fat, eaten_total_fat, next_meal_total_fat)
    if fat_intake > 0:
        nutrients_feedback.append(f"Fat: Exceeded daily intake by {fat_intake}")
    elif fat_intake < 0:
        nutrients_feedback.append(f"Fat: Need to meet daily intake by {-fat_intake}")
    else:
        nutrients_feedback.append(f"Fat: Met daily intake")

    # Sodium
    rda_sodium = get_recommended_daily_intake(f"{age}y", sex, 'Sodium')
    sodium_intake = calculate_nutrient_over_intake(rda_sodium, eaten_total_sodium, next_meal_total_sodium)
    if sodium_intake > 0:
        nutrients_feedback.append(f"Sodium: Exceeded daily intake by {sodium_intake}")
    elif sodium_intake < 0:
        nutrients_feedback.append(f"Sodium: Need to meet daily intake by {-sodium_intake}")
    else:
        nutrients_feedback.append(f"Sodium: Met daily intake")

    # Potassium
    rda_potassium = get_recommended_daily_intake(f"{age}y", sex, 'Potassium')
    potassium_intake = calculate_nutrient_over_intake(rda_potassium, eaten_total_potassium, next_meal_total_potassium)
    if potassium_intake > 0:
        nutrients_feedback.append(f"Potassium: Exceeded daily intake by {potassium_intake}")
    elif potassium_intake < 0:
        nutrients_feedback.append(f"Potassium: Need to meet daily intake by {-potassium_intake}")
    else:
        nutrients_feedback.append(f"Potassium: Met daily intake")

    # Dietary Fibre
    rda_fibre = get_recommended_daily_intake(f"{age}y", sex, 'Dietary Fiber')
    fibre_intake = calculate_nutrient_over_intake(rda_fibre, eaten_total_dietary_fibre, next_meal_total_dietary_fibre)
    if fibre_intake > 0:
        nutrients_feedback.append(f"Dietary Fibre: Exceeded daily intake by {fibre_intake}")
    elif fibre_intake < 0:
        nutrients_feedback.append(f"Dietary Fibre: Need to meet daily intake by {-fibre_intake}")
    else:
        nutrients_feedback.append(f"Dietary Fibre: Met daily intake")

    # Calcium
    rda_calcium = get_recommended_daily_intake(f"{age}y", sex, 'Calcium')
    calcium_intake = calculate_nutrient_over_intake(rda_calcium, eaten_total_calcium, next_meal_total_calcium)
    if calcium_intake > 0:
        nutrients_feedback.append(f"Calcium: Exceeded daily intake by {calcium_intake}")
    elif calcium_intake < 0:
        nutrients_feedback.append(f"Calcium: Need to meet daily intake by {-calcium_intake}")
    else:
        nutrients_feedback.append(f"Calcium: Met daily intake")

    # Monounsaturated Fat
    rda_monounsaturated_fat = get_recommended_daily_intake(f"{age}y", sex, 'Monounsaturated Fat')
    monounsaturated_fat_intake = calculate_nutrient_over_intake(rda_monounsaturated_fat, eaten_total_monounsaturated_fat, next_meal_total_monounsaturated_fat)
    if monounsaturated_fat_intake > 0:
        nutrients_feedback.append(f"Monounsaturated Fat: Exceeded daily intake by {monounsaturated_fat_intake}")
    elif monounsaturated_fat_intake < 0:
        nutrients_feedback.append(f"Monounsaturated Fat: Need to meet daily intake by {-monounsaturated_fat_intake}")
    else:
        nutrients_feedback.append(f"Monounsaturated Fat: Met daily intake")

    # Polyunsaturated Fat
    rda_polyunsaturated_fat = get_recommended_daily_intake(f"{age}y", sex, 'Polyunsaturated Fat')
    polyunsaturated_fat_intake = calculate_nutrient_over_intake(rda_polyunsaturated_fat, eaten_total_polyunsaturated_fat, next_meal_total_polyunsaturated_fat)
    if polyunsaturated_fat_intake > 0:
        nutrients_feedback.append(f"Polyunsaturated Fat: Exceeded daily intake by {polyunsaturated_fat_intake}")
    elif polyunsaturated_fat_intake < 0:
        nutrients_feedback.append(f"Polyunsaturated Fat: Need to meet daily intake by {-polyunsaturated_fat_intake}")
    else:
        nutrients_feedback.append(f"Polyunsaturated Fat: Met daily intake")

    # Manganese
    rda_manganese = get_recommended_daily_intake(f"{age}y", sex, 'Manganese')
    manganese_intake = calculate_nutrient_over_intake(rda_manganese, eaten_total_manganese, next_meal_total_manganese)
    if manganese_intake > 0:
        nutrients_feedback.append(f"Manganese: Exceeded daily intake by {manganese_intake}")
    elif manganese_intake < 0:
        nutrients_feedback.append(f"Manganese: Need to meet daily intake by {-manganese_intake}")
    else:
        nutrients_feedback.append(f"Manganese: Met daily intake")

    # Magnesium

    
    with open('report.txt', 'w') as file:  
        file.write(nutrients_feedback)  

    return nutrients_feedback


generate_report()


