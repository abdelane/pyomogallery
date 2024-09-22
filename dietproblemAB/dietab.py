from pyomo.environ import *
#imports pyomo package

infinity = float('inf')
#sets infinity to a float value

model = AbstractModel()
#creates an abstract model named model

# Foods
model.F = Set()
#creates an empty set of foods that can be filled later

# Nutrients
model.N = Set()
#creates an empty set of nutrients that can be filled later

# Cost of each food
model.c    = Param(model.F, within=PositiveReals)
#creates a parameter for the cost of each food for every item in the set 
# of foods and all costs must be postive and real

# Amount of nutrient in each food
model.a    = Param(model.F, model.N, within=NonNegativeReals)
#creates a parameter for the amount of each nutrient in each food, so 
# it is a parameter for each combination of item from the set of foods and nutrients

# Lower and upper bound on each nutrient
model.Nmin = Param(model.N, within=NonNegativeReals, default=0.0)
#parameter for the minimum amount of each nutrient, default is 0
model.Nmax = Param(model.N, within=NonNegativeReals, default=infinity)
#parameter for the maximum amount of each nutrient, default is infinity


# Volume per serving of food
model.V    = Param(model.F, within=PositiveReals)
#parameter for the volume of each food within set F, must be positive and real

# Maximum volume of food consumed (must be positibe and real)
model.Vmax = Param(within=PositiveReals)

# Number of servings consumed of each food
model.x = Var(model.F, within=NonNegativeIntegers)
#integer variable for the number of servings of each food in set F,
#  must be nonnegative

# Minimize the cost of food that is consumed
def cost_rule(model):
    #defines a function to minimize the cost of food in model

    return sum(model.c[i]*model.x[i] for i in model.F)
    #returns the sum of the cost of each food times the number of servings 
    # of that food i within the set of food F

model.cost = Objective(rule=cost_rule)
#returns the objective function for the model where the cost of food times 
# number of servings in summed over all foods

# Limit nutrient consumption for each nutrient
def nutrient_rule(model, j):
    #defines constraint on the model using j to iterate over the set of 
    # nutrients and i to iterate over set of foods

    value = sum(model.a[i,j]*model.x[i] for i in model.F)
    #sums the amount of nutrient in each food times the number of servings for all foods in set F

    return inequality(model.Nmin[j], value, model.Nmax[j])
    #returns the inequality that the amount of nutrient in the food must be less than the max
    #  number of nutrients and more than the min number of nutrients

model.nutrient_limit = Constraint(model.N, rule=nutrient_rule)
#returns the constraint for the model that the nutrient limit must be satisfied for all nutrients

# Limit the volume of food consumed
def volume_rule(model):
    #defines another constraint on the volume of food consumed in the model
    return sum(model.V[i]*model.x[i] for i in model.F) <= model.Vmax
    #returns the constraint that the sum of the volume of food times the number of servings 
    # for each food in the set F and ensures it is less than the max volume

model.volume = Constraint(rule=volume_rule)
#returns the constraint for the model that the volume of food consumed must be less than the max volume