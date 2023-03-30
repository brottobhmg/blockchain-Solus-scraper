import time
import requests
from bs4 import BeautifulSoup


f = open('block_log.csv', 'w', newline='')
startTime=time.time()
print("Start at "+str(startTime))
f.write("block number, timestamp, hash, size, weight, version, merkleroot, tx, number transaction, difficulty, chainwork, headerhash, mixhash, pow winner, block reward, output amount, fee amount\n") #write header
f.write("0,1651442858,0000000a50fdaaf22f1c98b8c61559e15ab2269249aa1fb20683180703cdbf07,294,1176,4,7c1d71731b98c560a80cee3b88993c8c863342b9661894304fd843bf7e75a41f,['7c1d71731b98c560a80cee3b88993c8c863342b9661894304fd843bf7e75a41f'],1,0.00390625,0000000000000000000000000000000000000000000000000000000001000100,93aa1e9e397de2a5a60d309fa0b82267ab6520ae6302181847bf14bd41143f2a,0000000000000000000000000000000000000000000000000000000000000000,Genesis,0.00000000,None,0.00000000\n")

i=1
while i<451973:

    data=""

    response=response=requests.get("https://neoxa.cryptoscope.io/api/getblock/?index="+str(i))
    if "429 Too Many Requests" in response.text:
        time.sleep(1)
        print("Wait:"+str(i))
        continue
    
    response=response.json()
    data=str(i)+','+str(response["time"])+','+str(response["hash"])+','+str(response["size"])+','+str(response["weight"])+','+str(response["version"])+','+str(response["merkleroot"])+','+str(response["tx"])+','+str(len(response["tx"]))+','+str(response["difficulty"])+','+str(response["chainwork"])+','+str(response["headerhash"])+','+str(response["mixhash"])
    

    response=requests.get("https://neoxa.cryptoscope.io/block/block.php?blockheight="+str(i)).text
    soup = BeautifulSoup(response, 'html.parser')

    powWinner=soup.find_all('a')[-1].string #powWinner

    block_reward=soup.find_all('td')[17].text.strip() #block reward

    output_amount=soup.find_all('td')[21].text.strip() #output amount

    fee_amount=soup.find_all('td')[-1].text.strip() #fee amount

    data+=','+str(powWinner)+','+str(block_reward)+','+str(output_amount)+','+str(fee_amount)

    f.write(data+"\n")

    i+=1

    time.sleep(0.6)

    
finishTime=time.time()
print("Finish at "+str(finishTime))
print("The time spent on: "+str(finishTime-startTime))
# close the file
f.close()




