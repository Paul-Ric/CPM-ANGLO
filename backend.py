from flask import Flask, jsonify

app = Flask(__name__)

# Dados de exemplo
dados = [
    {
			"National ID": "37981222613",
			"Worker ID": "AAOPWK00003243",
			"First Name": "Taishi",
			"Last Name": "Yoshikawa",
			"Worker Email": "jeanaranteslopes@gmail.com",
			"Vendor Number": "GHRAL",
			"Vendor Name": "GHB REVEGETACAO AMBIENTAL LTDA",
			"Work schedule": "Turno",
			"Site Name": "Minas Rio / C. Mato Dentro",
			"Work Location Name": "",
			"Work Location Code": "",
			"Permission to access the restaurant": "Sim",
			"Organization Unit": "I003_QP8",
			"Contract number": "AAOPWO00003544",
			"Contractor area": "Seguranca Patrimonial",
			"Contractor management": "Jose de Arimateia",
			"Contractor inspector (fiscal)": "Maria Madalena",
			"Cost Center Code": "14186745",
            "Start Date": "06/05/2024",
			"End Date": "27/09/2024",
			"ATO": "Sim",
			"ATW": "Nao"
		},
        {
			"National ID": "96019244695",
			"Worker ID": "AAOPWK00003249",
			"First Name": "Fernando",
			"Last Name": "Oliveira",
			"Worker Email": "Fernando.Oliveira@gmail.com",
			"Vendor Number": "Komatzo",
			"Vendor Name": "Komatzo Industria de Transporte",
			"Work schedule": "Administrativo",
			"Site Name": "Minas Rio / C. Mato Dentro",
			"Work Location Name": "",
			"Work Location Code": "",
			"Permission to access the restaurant": "Sim",
			"Organization Unit": "I003_QP8",
			"Contract number": "AAOPWO00003588",
			"Contractor area": "IM",
			"Contractor management": "Daniel Oliveira",
			"Contractor inspector (fiscal)": "Eliane Silva",
			"Cost Center Code": "14186788",
            "Start Date": "06/05/2024",
			"End Date": "31/12/2024",
			"ATO": "Sim",
			"ATW": "Sim"
		}
]

@app.route('/dados', methods=['GET'])
def obter_dados():
    return jsonify({"data": dados})

if __name__ == '__main__':
    app.run(debug=True,port=5001)
