import random 
import os
import yaml




config = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), 'insults.yml')))

def generateInsult():
    pref = 'Thou'

    col1 = random.choice(config['column1'])
    col2 = random.choice(config['column2'])
    col3 = random.choice(config['column3'])

    return f"{pref} {col1} {col2} {col3}"

