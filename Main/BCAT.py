"""
                                  ____   _____       _______ 
                                 |  _ \ / ____|   /\|__   __|
                                 | |_) | |       /  \  | |   
                                 |  _ <| |      / /\ \ | |   
                                 | |_) | |____ / ____ \| |   
                                 |____/ \_____/_/    \_\_|   

                        Blockchain Credential Authentication Technology
                                Capstone for Computing Security
                                          CSEC 499.600
                                        
Description: Blockchain CAT system for authentication of airline passengers based on passport authentication,
             face recognition, flight screening and immigrational risk assessment.

Language: Python3
"""

#-------------------------------
# Imports

import face_validation
import risk_assessment
import passport_scanner

import os
import json
import random
import pyttsx3
import requests
from web3 import Web3
from time import sleep
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


from selenium import webdriver
from time import sleep as nap
import time

#0.166
#0.22343015670776367
from selenium.webdriver.chrome.options import Options

#-------------------------------
# Environmental variables

ENV = load_dotenv('.env')

if (ENV):
    print("Environment Variables Successfumigrational Risk assessment score")

else:
    print("Environment Variables Could Not be Loaded...")
    exit(1)
    
load_dotenv('.env')

#-------------------------------
# Voice Module Configuration

voice_name = "Microsoft Zira Desktop - English (United States)"

engine = pyttsx3.init()
engine.setProperty('rate', 135)  # Speed of speech 
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

voices = engine.getProperty('voices')
selected_voice = None
for voice in voices:
    if voice.name == voice_name:
        selected_voice = voice
        break

    
if not selected_voice:
    print(f"Voice '{voice_name}' not found. Using the default voice.")
else:
    engine.setProperty('voice', selected_voice.id)

#-------------------------------
# Load Web Application Frontend

chrome_options = webdriver.ChromeOptions()

# Start Chrome in full screen mode
chrome_options.add_argument("--start-fullscreen")

# Initialize the driver with the chrome_options

driver = webdriver.Chrome(options=chrome_options)


#-------------------------------

def announce(message):
    """
    Announces messages or instructions to passenger through pyttsx3 module

    paramters:
    ---------
    message: string, text to be spoken
    """

    engine.say(message)
    engine.runAndWait()

def reset():
    """
    Resets the front end page for the next passenger and announces a message for the next passenger
    """
    announce("Next passenger please")
    driver.refresh()
    test()



def scan_passport():
    """
    Uses passport_scanner module to scan the passport presented on the live camera interface #01
    Uses tesseract engine to recognize characters and read machine readable zone code on the passport.
    Requires haardcascade frontal face xml configuration for face reecogniton on the passport.

    returns:
    -------
    scanned_passport: Dict, Json representation of scanned passport fields
    

    """
    
    announce("please present and scan your passport")

    scanned_passport = passport_scanner.scan()
    os.remove("passport.jpg")
    return scanned_passport

def risk_rating(country, age):
    """
    Uses risk_assessment module to calculate the immigrational risk assessment score associated with
    passenger based on nationality and age identified through scanned passport. Relies on ageRisk.csv
    and countryRisk.csv datasets to compute score.

    paramters:
    ---------
    country: string, country of passenger

    age: int, age of passenger

    returns:
    -------
    result: boolean, true if fuzzy logic algorithm produces less than 3, true if 3 to 4
    """

    countries = {'NLD': 'Netherlands'}
    
    country = countries[country]
    announce("Performing Background Check")

    result = risk_assessment.risk_calculator(country, age)

    if result >=3:
        announce("You have failed the background check, please see an airport officer")
        return False
    else:
        announce("Background check completed")
        return True
    
#risk_rating("sudan",18)
def face_recognition(number, name):
    """
    Uses face_validation to confirm the biometric identity of passenger with the one extracted from
    the blockchain. Image is stored as base64 in the blockchain and encoded as a .jpg to be used as
    a dataset.

    parameters:
    ----------
    base64: string, passport number of the passenger

    returns:
    -------

    result: boolean, true if biometric identity is a match, false otherwise
    """

    blob = "http://localhost:8040//"+number+".jpg"

    response = requests.get(blob)

    if response.status_code == 200:
        with open('passenger.jpg', 'wb') as f:
            f.write(response.content)
    else:
        print("AN ERROR HAS OCCURED WITH THE IMAGE")

    announce("Please Look at the Camera for facial authentication")

    result = face_validation.face_verification(name)

    

    if result == True:
        announce("Biometric Authentication completed")

    else:
        announce("Biometric Authentication failed, please see a airport officer")

    os.remove("passenger.jpg") # delete the image after being done


    return result

def display_result(check, result):
    """
    modifies web application to reflect assessment results of passenger.
    Displays cross for failed respective check and Tick for passed.

    Parameters:
    ----------
    check: int, the assessment performed for the commuter (1-4)

    result: boolean, True or False if check was success or not

    """

    if result == True:
        result = 1
    else:
        result = 2

    arg = "result"+str(check)+'('+str(result)+')'

    driver.execute_script(arg)
    nap(2)


def retrieve_address(passport_no):
    """
    retrieves the associated blockchain address with the commuter based on passport number.

    parameters:
    ----------
    passport_no: string, passport code scanned from the passport

    returns:
    -------
    eadrr: string, Ethereum blockchain address associated with passport
    """

    with open("addresses.eadrr", 'r') as file:
        for address in file:
            if passport_no == address.split('0x')[0]:
                return '0x'+address.split('0x')[1].replace('\n','')

    display_result(1,False)
    return False

def compare_passports(scanned_passport, blockchain_passport):
    """
    compares two provided passports based on each passport field.

    paramters:
    ---------
    scanned_passport: JSON, json representation of passport scanned by commuter

    blockchain_passport: JSON, json representation of passport retrieved from the blockchain

    returns:
    -------
    result: boolean, true of false if passports match or dont, respectively
    """

    print("SCANNED PASSPORT", scanned_passport)
    print("BLOCKCHAIN PASSPORT: ", blockchain_passport)
    print("\n\n")

    for field in blockchain_passport:
        if field.lower() == 'nationality':
            continue
        
        elif blockchain_passport[field] != scanned_passport[field]:
            announce("Passport Authentication Failed, please see an airport officer")
            return False

    announce("passport authentication complete")
    return True

def register(address, passport):
    """
    registers the passport with the Ethereum address provided in an authenticated manner

    parameters:
    ----------

    address: string, ethereum address where the passport will be registered to

    passport: list, array of passport field values
    """

    false = False
    contract_address = "0x0cc12aEe95F5E208DDf485b1C4c6697838b01797"

    contract_abi = [{"inputs":[{"internalType":"address","name":"eadrr","type":"address"}],"name":"getPassport","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_authorizedAccounts","type":"address[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string[]","name":"passportArray","type":"string[]"}],"name":"PassportRetrieved","type":"event"},{"inputs":[{"internalType":"address","name":"eadrr","type":"address"},{"internalType":"string","name":"country","type":"string"},{"internalType":"string","name":"pnumber","type":"string"},{"internalType":"string","name":"birth","type":"string"},{"internalType":"string","name":"expiry","type":"string"},{"internalType":"string","name":"nationality","type":"string"},{"internalType":"string","name":"sex","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"surname","type":"string"},{"internalType":"string","name":"persNumber","type":"string"}],"name":"registerPassport","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"authorizedAccounts","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]

    private_key = "7762e6039ebca2979de7c75e1f2522e52735b55f06e61d46c7c3cc79794eb879"

    address = "0x2DfAE3ab54075Cae47CcbD6A2B3bC343BC2dFb6c"

    #address = '0xeB1086e5a9D7F9B7458ea7650742b78080446886'


    url = 'http://127.0.0.1:7545'

    
    #passport = ['NLD','DE4878783', '650310', '240309', 'NLD', 'M', 'JOHN', "SAMPLE-PETER","<<<<<<<<<<<<<<"]

    web3 = Web3(Web3.HTTPProvider(url)) # connects to the blockchain

    eadrr = web3.toChecksumAddress(address)

    function_name = 'registerPassport'

    # Get the account address from the private key
    account_address = web3.eth.account.privateKeyToAccount(private_key).address

    contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)

    gas_estimate = contract.functions[function_name](eadrr,passport[0], passport[1],passport[2],passport[3],passport[4],passport[5],passport[6],passport[7],passport[8]).estimateGas({'from': account_address})
    print(gas_estimate)
    # Build the transaction without value (no Ether transfer)
    transaction = contract.functions[function_name](eadrr,passport[0], passport[1],passport[2],passport[3],passport[4],passport[5],passport[6],passport[7],passport[8]).buildTransaction({
        'from': account_address,
        'gas': gas_estimate,
        'gasPrice': web3.eth.gasPrice,
        'nonce': web3.eth.getTransactionCount(account_address),
        'value': 0,
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.signTransaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    
    #retrieved_passport = contract.functions.registerPassport(eadrr,'NLD','DE4878783', '650310', '240309', 'netherlands', 'm', 'JOHN', 'SAMPLE PETER','<<<<<<<<<<<<<<').call() # call specific method

    #retrieved_passport = contract.functions.registerPassport(eadrr,passport[0], passport[1],passport[2],passport[3],passport[4],passport[5],passport[6],passport[7],passport[8]).call() # call specific method
    #print(retrieved_passport)

#register(1,1)
def retrieve_passport(address):
    """
    connects to the private ethereum network and interacts with the smart contract
    functions to retrieve passport. This method requires the private key of an
    authorised BCAT unit.


    parameters:
    ---------
    eadrr: string, ethereum address associated with the passport

    returns:
    -------
    blockchain_passport: List, passport retrieved from blockchain

    raises:
    ------
    execution reverted: raised when account used is not authorised to interact with the smart contract

    """
    
    #contract_address = '0x3bA41fbaEb3b43F822C526166dec597f7e8A778f'

    #contract_abi = [{"inputs":[{"internalType":"address[]","name":"_authorizedAccounts","type":"address[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string[]","name":"passportArray","type":"string[]"}],"name":"PassportRetrieved","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"authorizedAccounts","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"eadrr","type":"address"}],"name":"getPassport","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"eadrr","type":"address"},{"internalType":"string","name":"country","type":"string"},{"internalType":"string","name":"pnumber","type":"string"},{"internalType":"string","name":"birth","type":"string"},{"internalType":"string","name":"expiry","type":"string"},{"internalType":"string","name":"nationality","type":"string"},{"internalType":"string","name":"sex","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"surname","type":"string"},{"internalType":"string","name":"persNumber","type":"string"}],"name":"registerPassport","outputs":[],"stateMutability":"nonpayable","type":"function"}]

    #private_key = "9d9cb8ae351a01903b0aa40a694ebac97820704854c7edc5105ab5caba39d192"

    url = str(os.getenv("BLOCKCHAIN_ADDRESS"))

    web3 = Web3(Web3.HTTPProvider(url)) # connects to the blockchain
    
    passport_address = web3.toChecksumAddress(address)


    # Initialize the contract object
    contract = web3.eth.contract(address=Web3.toChecksumAddress(os.getenv("SMART_CONTRACT_EADRR")), abi=os.getenv("SMART_CONTRACT_ABI"))
    #contract = web3.eth.contract(address=os.getenv('SMART_CONTRACT_EADRR'), abi=os.getenv('SMART_CONTRACT_ABI'))

    # Function name
    function_name = 'getPassport'

    # Get the account address from the private key
    account_address = web3.eth.account.privateKeyToAccount(os.getenv("PRIVATE_KEY")).address

    # Estimate the gas required for the transaction
    gas_estimate = contract.functions[function_name](passport_address).estimateGas({'from': account_address})

    # Build the transaction without value (no Ether transfer)
    transaction = contract.functions[function_name](passport_address).buildTransaction({
        'from': account_address,
        'gas': gas_estimate,
        'gasPrice': web3.eth.gasPrice,
        'nonce': web3.eth.getTransactionCount(account_address),
        'value': 0,
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.signTransaction(transaction, os.getenv("PRIVATE_KEY"))


    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    transaction_receipt = web3.eth.waitForTransactionReceipt(transaction_hash)
    logs = web3.eth.contract(abi=os.getenv("SMART_CONTRACT_ABI")).events.PassportRetrieved().processReceipt(transaction_receipt)


    for log in logs:
        passport_array = log.args['passportArray']
        passport = [item.replace("'",'').replace(' ','') for item in passport_array]
        print("Passport: ", passport)

    return passport


def format_response(response):
    """
    formats blockchain response into JSON object to match scanned passport object

    parameters:
    ----------
    response: list, passport field values

    returns:
    -------

    json_passport: JSON, passport JSON object
    """
    
    attributes = ['country', 'number', 'date_of_birth', 'expiration_date', 'nationality', 'sex', 'names', 'surname', 'persNumber']
    passport = {'country': '', 'number': '', 'date_of_birth': '', 'expiration_date': '', 'nationality': '', 'sex': '', 'names': '', 'surname': '', 'personal_number': ''}

    counter = 0
    for field in passport.keys() :
        passport[field] = response[counter]
        counter += 1

    for key, value in passport.items():
        passport[key] = value.replace("'", "")


    newsurname = passport['surname'].replace('-',' ')
    passport['surname'] = newsurname
    return passport
        

def verify_flight(passport_code):
    """
    verifies existence of flight record through querying passport number

    parameters:
    ----------
    passport_code: string, passport code from scanned passport

    returns:
    -------
    True/False: boolean, if booking  found, true otherwise false
    """

    announce("Performing Pre-flight screening")

    url = str(os.getenv("FLIGHT_ADDRESS")) + passport_code

    
    # for HttpBasicAuth
    #password = "bcat"
    #username = "password"
    #response = requests.post(url, json=passport_code, auth=HTTPBasicAuth(username, password))

    response = requests.post(url, data=passport_code)
    booking_ID, response_code = response.text, response.status_code

    if response_code == 302:
        return True
        announce("Pre-flight scereening completed")

    elif response_code == 417:
        announce("Pre-flight screening failed, no booking was found, Please see an airport officer")
        return False

    else:
        return response_code


def check(result):
    """
    Stops the screening process if the passenger failed any checks and resets

    param:
    -----
    result: boolean, if true then screening continues, if false, stops
    """
    
    if result == True:
        return 0

    else:
        announce("screening has ended, please see a airport control officer for assistance")
        reset()
    
def test():

    driver.get("http://localhost:8000/BCAT/")
    nap(3) # give time for the page to load

    announce("Welcome passenger, please step up to begin")

    scanned_passport = scan_passport()                              # Scan the passport

    if scanned_passport['sex'].lower() == "f":
        title = "miss"
    else:
        title = "mister"
    
    announce("Welcome " + title + ' ' + scanned_passport["names"])
    nap(1)

    passport_no = scanned_passport["number"]                        # Save the passport number

    print(scanned_passport,'\n\n')
    print(passport_no,'\n\n')

    eadrr = retrieve_address(passport_no)

    if eadrr == False:
        announce("Passport is not registered, please see a airport officer")
        reset()
    # Retrieve ethereum address associated with passenger

    print(eadrr,'\n\n')

    blockchain_passport = retrieve_passport(eadrr)                  # Retrieve the passport from the blockchain
    
    blockchain_passport = format_response(blockchain_passport)      # Format the passport retrieved from the blockchain

    passport_check_result = compare_passports(scanned_passport, blockchain_passport) # Second check, verify passports match

    display_result(1, passport_check_result)                        # Reflect result of passport verification

    preflight_screening_result = verify_flight(passport_no)         # First check, verify booked flight
    
    display_result(2, preflight_screening_result)                   # Reflect result of booking verification on the web app

    name = blockchain_passport["names"] + ' ' + blockchain_passport["surname"]

    face_screening_result = face_recognition(passport_no, name)     # Verify facial biometric identity

    display_result(3, face_screening_result)                        # Reflect result of facial authentication

    country = scanned_passport["country"]                           # Store country


    if int(scanned_passport["date_of_birth"][:2]) <= 20:                 # store age
        
        age = 2023 - int('20' + scanned_passport["date_of_birth"][:2])
    else:
        age = 2023 - int('19' + scanned_passport["date_of_birth"][:2])

    print("\n\nAGE = ",age,'\n\n')
            

    risk_assessment_result = risk_rating(country, age)          # Compute immigrational Risk assessment score

    display_result(4, risk_assessment_result)                   # Reflect result of immigrational risk assessment


    print("passport check: ", passport_check_result, '\n\n')
    print("face validation: ", face_screening_result,'\n\n')
    print("risk assessment: ", risk_assessment_result, '\n\n')

    messages = ["Thank you, Have a safe and pleasant journey!", "Thank you, and enjoy your flight", "Thank you, Enjoy your flight to the fullest!"]
    announce(random.choice(messages)) # say goodbye to the passenger

    sleep(3) # wait 3 seconds
    reset()  # reset for next passenger


test()

def BCAT():
    """
    Main module for BCAT python program. operates other functions to calculate results, interact
    with the private Ethereum blockchain and format data as well as display results to the django
    web application.
    """

    while True:

        scanned_passport = scan_passport()                              # Scan the passport

        passport_no = scanned_passport["number"]                        # Save the passport number

        preflight_screening_result = verify_flight(passport_no)         # First check, verify booked flight
    
        display_result(1, preflight_screening_result)                   # Reflect result of booking verification on the web app

        eadrr = retrieve_address(passport_no)                           # Retrieve ethereum address associated with passenger

        blockchain_passport = retrieve_passport(eadrr)                  # Retrieve the passport from the blockchain

        blockchain_passport = format_response(blockchain_passport)      # Format the passport retrieved from the blockchain

        pasport_check_result = compare_passports(scanned_passport, blockchain_passport) # Second check, verify passports match

        display_result(2, passport_check_result)                        # Reflect result of passport verification

        image = blockhain_passport["image"]                             # Save base64 image of the passenger

        name = blockchain_passport["names"] + ' ' + blockchain_passport["surname"]

        face_screening_result = face_recognition(image, name)                 # Verify facial biometric identity

        display_result(3, face_screening_result)                        # Reflect result of immigrational risk assessment

        country = scanned_passport["country"]                           # Store country

        if scanned_passport["date_of_birth"][:2] <= 20:                 # store age
        
            age = 2023 - int('20' + scanned_passport["date_of_birth"][:2])
        else:
            age = 2023 - int('19' + scanned_passport["date_of_birth"][:2])
            
        #risk_assessment_result = risk_(country, age)          # Compute immigrational Risk assessment score

        display_result(4, risk_assessment_result)                       # Reflect result of immigrational risk assessment

        sleep(3) # wait 3 seconds
        reset()  # reset for next passenger
        
        

#############################################################################################################################################
