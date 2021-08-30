from flask import Flask, render_template, request, render_template_string
import requests
import json


app = Flask(__name__)


TABLE_TEMPLATE = """
<style>
   table, th, td {
   border: 1px solid black;
   }
</style>
<table style="width: 100%">
   <thead>
      <th>Name</th>
      <th>Gender</th>
      <th>Average Lifespan</th>
      <th>Home Planet Name</th>
      <th>Films</th>
   </thead>
   <tbody>
    <tr>
      {% for row in data %}
         <td>{{ row }}</td>
      {% endfor %}
      </tr>
   </tbody>
</table>
"""
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def index():

    variable = request.form['variable']
    if variable == '':
       return ("Enter Name to search")
    url = 'https://swapi.dev/api/people/'
    url_p = 'https://swapi.dev/api/planets/'
    url_s = 'https://swapi.dev/api/species/'
    url_f = 'https://swapi.dev/api/films/'
    headers = {'Content-Type': 'application/json'}

    filters = [dict({})]
    params = dict(q=json.dumps(dict(filters=filters)))
    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 200
    result = response.json()
    result =result["results"]



    res = []
    num = ''
    num_s = []
    num_f = []
    for sub in result:
        if sub['name'] == variable:
            num = sub['homeworld']
            num_s = sub['species']
            num_f = sub['films']
            res = sub
        
    num = num.split("/")[-2]
    #print(num)


    ######################### home planet name   ###################
  
    filters_p = [dict({})]
    params_p = dict(q=json.dumps(dict(filters=filters_p)))
    response_p = requests.get(url_p, params=params_p, headers=headers)
    assert response_p.status_code == 200
    #print(response_p.json())
    result_p = response_p.json()
    result_p =result_p["results"]
  

    #print(type(num))
    i = 0
    for sub_p in result_p:
        com = i+1
        if str(com) == num:
            plan = sub_p['name']
        i += 1
    
    #########################   average lifespan  ###################
    filters_s = [dict({})]
    params_s = dict(q=json.dumps(dict(filters=filters_s)))
    response_s = requests.get(url_s, params=params_s, headers=headers)
    assert response_s.status_code == 200
    result_s = response_s.json()
    result_s = result_s["results"]
    
    species_num = []
    #print(num_s)
    for sub in num_s:
        species = sub.split('/')[-2]
        species_num.append(species)
    #print(species_num)
    spec = []
    for numb in species_num:
        i = 0
        for spec_i in result_s:
            com = i+1
            if str(com) == numb:
                spec.append(spec_i['average_lifespan'])
            i += 1

    #########################   films  ################### 
    filters_f = [dict({})]
    params_f = dict(q=json.dumps(dict(filters=filters_f)))
    response_f = requests.get(url_f, params=params_f, headers=headers)
    assert response_f.status_code == 200
    result_f = response_f.json()
    result_f = result_f["results"]
    
    film_num = []
    for sub in num_f:
        films = sub.split('/')[-2]
        film_num.append(films)
    film = []
    for numf in film_num:
        i = 0
        for film_i in result_f:
            com = i+1
            if str(com) == numf:
                film.append(film_i['title'])
            i += 1
   

    
    #out='Name:   '+res['name']+'Gender:   '+res['gender']+'   average lifespan:  '+str(spec)+'\n '+str(plan)+'  films:   '+str(film) 
    data = []
    data.append(res['name'])
    data.append(res['gender'])
    data.append(str(spec))
    data.append(str(plan))
    data.append(str(film))

    if(len(res) == 0):
       return "NOT FOUND" 
    else:
        return render_template_string(TABLE_TEMPLATE,
                                  data=data)

   
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)