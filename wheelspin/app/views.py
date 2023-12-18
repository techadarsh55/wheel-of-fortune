from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import mysql.connector
import pandas as pd
import json

def connection():
	try:
		conn = mysql.connector.connect(host="localhost",user="root",password="",database="wheelspin",port=3306)
	except Exception as e:
		print(e)
	return conn 


def predict_key(dictionary):
    total = sum(dictionary.values())
    probabilities = {key: value / total for key, value in dictionary.items()}
    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    predicted_key = sorted_probabilities[0][0]  # Select the key with the highest probability
    return predicted_key



def home(request):
	conn = connection()
	prize=None
	check_qty = pd.read_sql(f"select * from products;", conn)
	print(check_qty.to_dict('records')[0])
	data = check_qty.to_dict('records')[0]

	data_list = {'key1':data['key1'],'key2':data['key2'],'key3':data['key3'],'key4':data['key4']}
	predicted_key = predict_key(data_list)
	print("Predicted key:", predicted_key)
	
	if predicted_key == 'key1':
		#amazoun voucher
		prize = 1
		value = data['key1']
	elif predicted_key == 'key2':
		prize = 2
		value = data['key2']
		 #tupperware
	elif predicted_key == 'key3':
		prize = 3
		value = data['key3']
		 #flask
	else:
		prize = 4
		value = data['key4']
		 #umbrella

	print(prize, value)
	context = {'set_prize': prize, 'value':value}
	return render(request,'index.html', context)

def update_item_qty(request):
	conn = connection()
	item_number = request.POST.get('product_key')
	item_qty = request.POST.get('val')
	print(item_number, item_qty)
	mydb = conn.cursor()
	if item_number == '1':
	 	query = f"update products set key1 = key1 - 1"
	elif item_number == '2':
	 	query = f"update products set key2 = key2 - 1"
	elif item_number == '3':
	 	query = f"update products set key3 = key3 - 1"
	else:
	 	query = f"update products set key4 = key4 - 1"

	mydb.execute(query)
	conn.commit()
	conn.close()
	return HttpResponse(json.dumps({'done':'ok'}), content_type="application/json")