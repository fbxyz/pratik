# pratik

## dep_reg.json
Les codes départementaux et les nouvelles régions associées
 
``` import requests, json
url = 'https://raw.githubusercontent.com/fbxyz/pratik/main/dep_reg.json'
resp = requests.get(url)
data = json.loads(resp.text)
```
