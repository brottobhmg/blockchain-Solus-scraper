import time
import requests
from bs4 import BeautifulSoup

coin="neoxa"

f = open('block_log.csv', 'w', newline='')
startTime=time.time()
print("Start at "+str(startTime))
f.write("block number, timestamp, hash, size, weight, version, merkleroot, tx, number transaction, difficulty, chainwork, headerhash, mixhash, pow winner, block reward, output amount, fee amount\n") #write header

i=2145
while i<2155:

    data=""

    try:
        response=response=requests.get("https://"+coin+".cryptoscope.io/api/getblock/?index="+str(i))
    except:
        time.sleep(2)
        continue
    if "429 Too Many Requests" in response.text:
        time.sleep(1)
        print("Wait:"+str(i))
        continue
    
    response=response.json()
    data=str(i)+','+str(response["time"])+','+str(response["hash"])+','+str(response["size"])+','+str(response["weight"])+','+str(response["version"])+','+str(response["merkleroot"])+','+str(response["tx"]).replace(",",";")+','+str(len(response["tx"]))+','+str(response["difficulty"])+','+str(response["chainwork"])+','+str(response["headerhash"])+','+str(response["mixhash"])
    
    try:
        response=requests.get("https://"+coin+".cryptoscope.io/block/block.php?blockheight="+str(i)).text
    except:
        time.sleep(2)
        continue
    
    soup = BeautifulSoup(response, 'html.parser')
   
    if i!=0:
        powWinner=soup.find_all('a')[-1].string #powWinner
        block_reward=soup.find_all('td')[17].text.strip() #block reward
        output_amount=soup.find_all('td')[21].text.strip() #output amount
        fee_amount=soup.find_all('td')[-1].text.strip() #fee amount
    else:
        powWinner= soup.find_all('td')[9].text
        block_reward= soup.find_all('td')[13].text
        output_amount=soup.find_all('td')[15].text.strip()
        fee_amount=soup.find_all('td')[-1].text.strip()

    data+=','+str(powWinner)+','+str(block_reward)+','+str(output_amount)+','+str(fee_amount)
    f.write(data+"\n")

    i+=1

    time.sleep(0.6)


finishTime=time.time()
print("Finish at "+str(finishTime))
print("The time spent on: "+str(finishTime-startTime))
# close the file
f.close()




