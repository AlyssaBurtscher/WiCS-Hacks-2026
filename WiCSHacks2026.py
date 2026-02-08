from serpapi import GoogleSearch
import streamlit as st
import math

params = {
  "engine": "google_events",
  "q": "Music in Austin",
  "api_key": "0b49844007fbc97cd2cb3e59b038f686346dd98d6b77212fdba0f68cbe2cc277"
}

search = GoogleSearch(params)
results = search.get_dict()
events_results = results["events_results"]

st.set_page_config(page_title="Austin Music Events", page_icon="🎵", layout="wide")

st.title("🎵 Austin Music Events 🎵")
l = []
for x in events_results:
    d = {}
    d["title"] = x['title']
    d["image"] = x['image']
    d["when"] = x['date']['when']
    d["address"] = x['address'][0]
    l.append(d)



travel = []
for i in range(len(l)):
  params = {
    "engine": "google_maps_directions",
    "start_addr": "110 Inner Campus Drive",
    "end_addr": l[i]['address'],
    "api_key": "0b49844007fbc97cd2cb3e59b038f686346dd98d6b77212fdba0f68cbe2cc277",
    "travel_mode": 3
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  travel.append(results["directions"])

r = 0
#st.markdown(travel[0])
print("------------------------")
#print(list(travel[0]))
i = 1
for k in range(len(travel)):
   mind = travel[k][0]['duration']
   mini = 0
   for n in range(len(travel[k])):
      t = travel[k][n]['duration']
      if t < mind:
         mind = t
         mini = n
   l[k]["mode"] = travel[k][mini]["travel_mode"]
   l[k]["duration"] = travel[k][mini]['formatted_duration']
   t = travel[k][mini]['trips']
   
   q = []
   for o in t:
      g = []
      if o['travel_mode'] != 'Walking':
         g.append(o['title'])
         g.append(o['stops'][0]["name"] + " to " + o['stops'][-1]["name"])
         q.append(g)
   if len(q) > 0:
        l[k]["tripinfo"] = q

rows = []
for v in range(math.ceil(len(l)/3)):
  rows.append(st.columns(3))

i = 0
for row in rows:
  for col in row:
      if i < len(l):
        tile = col.container(height=400, horizontal_alignment='center')
        tile.image(l[i]["image"])
        tile.markdown("**" + l[i]['title'] + "**", text_alignment='center')
        tile.markdown(l[i]['when'], text_alignment='center')
        tile.markdown(l[i]['address'], text_alignment='center')
        s = l[i]['mode'] + " - " + l[i]['duration']
        with tile.popover(s):
           st.markdown("**" + s + "**", text_alignment='center')
           if "tripinfo" not in l[i]:
              st.markdown(l[i]["address"])
           else:
              for y in l[i]["tripinfo"]:
                 st.markdown("_**" + y[0] + "**_")
                 st.markdown("•   " + y[1])
      i += 1