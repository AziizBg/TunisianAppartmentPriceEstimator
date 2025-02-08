import json

with open('../../data/RAW/Binded.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

with open('../../data/GeoData/Locations.json', 'r', encoding="utf-8") as file:
    locationdata = json.load(file)

delegation_states = {}
munips_delegations = {}
for item in locationdata:
    for delegation in item['delegations']:
        delegation_states[delegation['delegation'].upper()] = item['governorate'].upper()
        for munip in delegation['localities']:
            munips_delegations[munip] = delegation['delegation'].upper()


treated = 0
todel = []
for item in data:
    if float(item["newMunipReport"]) < 0.8:
        #harmonic match
        if item['NewDelegation'] == munips_delegations[item['newMunip']] and item['NewState'] == delegation_states[item["NewDelegation"]]:
            pass
        else:
            if item['NewDelegation'] == munips_delegations[item['newMunip']] and item['NewDelegationReport']>0.8:
                item['NewState'] = delegation_states[item["NewDelegation"]]
            else:
                print(json.dumps(item, ensure_ascii=False, indent=4))
                todel.append(item)
                treated += 1
    else:
        item['NewDelegation'] = munips_delegations[item['newMunip']]
        item['NewState'] = delegation_states[item["NewDelegation"]]
    item['municipality'] = item['newMunip']
    item['delegation'] = item['NewDelegation']
    item['state'] = item['NewState']
    del item['NewDelegation']
    del item['newMunip']
    del item['NewState']
    del item['NewDelegationReport']
    del item['newMunipReport']
    del item['NewStateReport']


for item in todel:
    data.remove(item)

with open(f'../../data/Processed/processed.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(treated/len(data)*100,'%')
print(len(data))
