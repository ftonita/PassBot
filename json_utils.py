import json

async def createJSON(_pass):
	dictionary = {
		"pass_id": f"#{_pass[0]}",
		"guest_name": f"{_pass[1]}",
		"doc_number": f"{_pass[2]}",
		"date": f"{_pass[3]}",
		"hour": f"{_pass[4]}:00",
		"status": f"{_pass[5]}",
		"inviter": f"{_pass[6]}"
	}
	jsonString = json.dumps(dictionary, indent=4)
	f = open(f'httpd/html/{_pass[0]}.json', 'w')
	f.write(jsonString)
	f.close()