final_recommendation_report = 'I am the final recommendation report'
food_graph = {}
food_drug_interactions = {}
scd_rdi = {} ##Contains sickle cell disease RDI
user_profile = {} ##Age and Sex
user_stomach = {} ##Contains consumed foods
meal_components = {} ##Contains detected foods


def fill_stomach():
    return 0


def generate_food_graph(file_route):
    ##Opens CSV File
    ##Maps data into a graph
    return


def calculate_portion_hazard():
    return


def get_recommended_daily_intake():
    return


##Checking if any component of the meal might react with a drug
def add_drug_reaction_to_report(meal_components):
    for meal in meal_components:
        if len(food_graph.meal['drug_reactions'])!=0:
            if calculate_portion_hazard(food_graph.meal['drug_reactions']):
                print(f"{meal} is known to interact with {meal['drug_reactions']}")
        else:
            print("Meal has no reaction and is safe to eat")
    return


##Checking if any component of the meal contains a compound that may be an allergen
def add_compound_allergen_to_report(meal_components):
    for meal in meal_components:
        if len(food_graph.meal['compound_allergens']) !=0:
            if calculate_portion_hazard(food_graph.meal['compound_allergens'], meal['portion']):
                print(f"{meal} is known to interact with {meal['drug_reactions']}")
            else:
                print("Meal has no reaction and is safe to eat")


def get_user_input():
    return


#Takes in a list of names of the foods detected in the meal from the Computer Vision Module
def sum_meal_calories(meal_components):
    meal_sum = 0
    for food in meal_components:
        meal_sum += food.calories
    return meal_sum



#Takes in a list of names of the foods detected in the meal from the Computer Vision Module
def sum_meal_vitaminB12(meal_components):
    meal_vitaminB12 = 0
    for food in meal_components:
        meal_vitaminB12 += food.vitaminB12
    return


def get_food_alternatives(food):
    return