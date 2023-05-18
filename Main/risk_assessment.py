"""
==========================================
Fuzzy Logic Control System: RISK RATING
==========================================

Description: Fuzzy Logic Control System that evaluates risk level given two risk antecedent values
Language: Python 3.9.4
-------------------------------------------------------------
"""

# imports
import numpy as np
from csv import reader
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

def risk_matrix(country, age):
    """
    Takes country and age and looks up corresponding risk level from the data sets

    Parameters
    ----------
    country : str, nationality of passenger

    age : int, age of passenger


    Returns
    -------
    tuple, tuple representing country risk score and age risk score respectively
        
    """

    country_risk = 0
    age_risk = 0
    
    with open('countryRisk.csv', 'r') as csv_file: # reading country risk dataset
        data = reader(csv_file)
        risk_data = {rows[0]: rows[1] for rows in data} # loading dataset into dictionary
        

        for country_, risk in risk_data.items():
            #print(country_, risk)
            if country_.lower().strip() == country.lower().strip(): # sanitizing data
                country_risk =  int(risk) # if country matches, assign the associated risk score

    with open('ageRisk.csv', 'r') as csv_file: # reading age risk dataset
        data = reader(csv_file)
        risk_data = {rows[0]: rows[1] for rows in data} # loading dataset into dictionary
        

        for age_range, risk in risk_data.items():
            
            min_,max_ = int(age_range.split('-')[0]), int(age_range.split('-')[1]) # split range values

            if age >= min_ and age <= max_: # if in between the range
                
                age_risk = int(risk)        # assign the associated risk score
          
    return country_risk, age_risk





def risk_calculator(country, age):
    """
    Uses fuzzy logic control system to provide a risk calculation for a passenger
    based on nationality and age. Uses three membership functions with values
    ranging from 0 to 4 to create triangular relationships and calculate a score.
    Relies on risk_matrix() to obtain risk ratings from the dataset.

    Paramters
    ---------

    country: str, nationality of passenger

    age: int, age of passenger
    

    Returns
    -------

    risk_score: float, total immigrational risk score for passenger
    """
    
    country_risk_score, age_risk_score = risk_matrix(country, age)
    
    # Create the antecedent variables
    country_risk = ctrl.Antecedent(np.arange(1, 5, 1), 'country_risk')  # universe of [1, 4]
    age_risk = ctrl.Antecedent(np.arange(1, 5, 1), 'age_risk')  # universe of [1, 4]

    # Create the consequent variable
    RISK = ctrl.Consequent(np.arange(1, 5, 1), 'RISK')  # universe of [1, 4]

    # Define the membership functions for the antecedent variables
    country_risk['low'] = fuzz.trimf(country_risk.universe, [1, 1, 2.5])
    country_risk['medium'] = fuzz.trimf(country_risk.universe, [1, 2.5, 4])
    country_risk['high'] = fuzz.trimf(country_risk.universe, [2.5, 4, 4])

    age_risk['low'] = fuzz.trimf(age_risk.universe, [1, 1, 2.5])
    age_risk['medium'] = fuzz.trimf(age_risk.universe, [1, 2.5, 4])
    age_risk['high'] = fuzz.trimf(age_risk.universe, [2.5, 4, 4])

    # Define the membership functions for the consequent variable
    RISK['low'] = fuzz.trimf(RISK.universe, [1, 1, 2.5])
    RISK['medium'] = fuzz.trimf(RISK.universe, [1, 2.5, 4])
    RISK['high'] = fuzz.trimf(RISK.universe, [2.5, 4, 4])
    


    # Define the rules for the fuzzy system
    rule1 = ctrl.Rule(country_risk['low'] & age_risk['low'], RISK['low'])
    rule2 = ctrl.Rule(country_risk['low'] & age_risk['medium'], RISK['low'])
    rule3 = ctrl.Rule(country_risk['low'] & age_risk['high'], RISK['medium'])
    rule4 = ctrl.Rule(country_risk['medium'] & age_risk['low'], RISK['low'])
    rule5 = ctrl.Rule(country_risk['medium'] & age_risk['medium'], RISK['medium'])
    rule6 = ctrl.Rule(country_risk['medium'] & age_risk['high'], RISK['high'])
    rule7 = ctrl.Rule(country_risk['high'] & age_risk['low'], RISK['medium'])
    rule8 = ctrl.Rule(country_risk['high'] & age_risk['medium'], RISK['high'])
    rule9 = ctrl.Rule(country_risk['high'] & age_risk['high'], RISK['high'])
    
    # Create the control system
    risk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

    # Create the simulation
    risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)

    # Set the input values for the antecedent variables
    risk_sim.input['country_risk'] = country_risk_score
    risk_sim.input['age_risk'] = age_risk_score
 
    
    # Compute the output value for the consequent variable
    risk_sim.compute()

    # Print the output value for the consequent variable
    final_score = risk_sim.output['RISK'] + risk_sim.output['RISK'] * 0.15 # upscale result by 15%
    print("Country Risk: ",country_risk_score, "\nAge Risk: ", age_risk_score, "\nRISK RATING FOR PASSENGER: ",round(final_score,2))
    """
    plt.ion()
    country_risk['medium'].view()
    plt.title('country_risk')
    plt.ioff()

    #image:: PLOT2RST.current_figure
    
    plt.ion()
    age_risk.view()
    plt.title('age_risk')
    plt.ioff()
    
    #.. image:: PLOT2RST.current_figure

    plt.ion()
    RISK.view()
    plt.title('RISK')
    plt.ioff()
    """
    return final_score
