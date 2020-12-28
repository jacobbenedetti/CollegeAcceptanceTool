from requests import get
from bs4 import BeautifulSoup 
import pandas as pd 
from time import sleep 
import time as time 
from random import randint 
     
#url changers 
states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming'] 
     
#lists to store info     
startTime = time.time() 
requests = 0 
     
for state in states: 
    currentState = [] 
    collegeName = [] 
    SATRange = [] 
    ACTRange = [] 
    GPA = [] 
    acceptanceRate = []
    response = get("https://www.collegesimply.com/colleges/search?sort=&place=&gpa=&sat=&act=&admit=allmatch&field=&major=&radius=&zip=&state=" + state + "&size=&tuition-fees=&net-price=")      
    time.sleep(randint(8, 15)) 
    requests += 1 
    timeSinceStart = time.time() - startTime 
    print('requests per second is', (requests / int(timeSinceStart)), 'and have made ', requests, 'requests') 
     
    if response.status_code != 200: 
        print('wrong status code') 
     
    if (requests > 50): 
        print('more than expected requests')
        break
     
    html_soup = BeautifulSoup(response.text, 'html.parser') 
    college_cards = html_soup.find_all('div', class_ = 'card mt-3 mb-3') 
       
    for college in college_cards: 
        
        currentState.append(state)
        name = college.h4.a.text 
        collegeName.append(name) 
     
        liList = college.find('ul').find_all('li') 
        counter = 0
        
        for li in liList:
            if counter == 0:
                SATRange.append(li.strong.text)
                counter += 1    
            elif counter == 1:
                ACTRange.append(li.strong.text)
                counter += 1
            elif counter == 2:
                GPA.append(li.strong.text)
                counter += 1
            else:
                break
        
        acceptance = college.find('ul', class_ = 'list-unstyled small') 
        acceptancePercent = acceptance.li.strong.text 
        acceptanceRate.append(float(acceptancePercent))
    
    SATmin = []
    SATmax = []
    ACTmin = []
    ACTmax = []
    newGPA = []
    updatedStates = []

    for SAT in SATRange:
        if SAT != 'N/A':
            splitList = SAT.split('/')
            SATmin.append(splitList[0])
            SATmax.append(splitList[1])
        else:
            SATmin.append('Not published')
            SATmax.append('Not published')
        
    for ACT in ACTRange:
        if ACT != 'N/A':
            splitList2 = ACT.split('/')
            ACTmin.append(splitList2[0])
            ACTmax.append(splitList2[1])
        else:
            ACTmin.append('Not published')
            ACTmax.append('Not published')
            
    for xGPA in GPA:
        if xGPA != 'NA':
            newGPA.append(xGPA)
        else:
            newGPA.append('Not published')
        
    for state in currentState:
        newState = state.capitalize()
        updatedStates.append(newState)
    
    df = pd.DataFrame({'State' : updatedStates, 'College Name' : collegeName, 'SAT 25th Percentile' : SATmin, 'SAT 75th Percentile' : SATmax, 'ACT 25th Percentile' : ACTmin, 'ACT 75th Percentile' : ACTmax, 'Average GPA' : newGPA, 'Acceptance Rate' : acceptanceRate})
    df.to_csv(r'C:\\CS for Fun\\Data Science Retry\\College Data Files\\' + state + 'Data.csv', encoding = 'utf-8')