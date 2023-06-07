from flask import Flask, jsonify, request
from PowerPlantType import PowerPlantType
from PowerPlantModel import PowerPlantModel

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def optimize_cost():
    payload= request.json
    load = payload['load']
    fuels = payload['fuels']
    powerplants = payload['powerplants']
    model = PowerPlantModel()
    powerPlantType = [member.value for member in PowerPlantType]
    for powerplant in powerplants:
        
        if powerplant["efficiency"] == 0 : 
            return jsonify({'error': 'Invalid power plant efficiency'}), 400

        if powerplant['type'] not in powerPlantType:
            return jsonify({'error': 'Invalid power plant type'}), 400
        
        model.addPowerPlant(powerplant["name"], powerplant["type"], powerplant["efficiency"],powerplant["pmax"],powerplant["pmin"])
    
    try:
        response = model.generatePower(load,fuels)
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message }), 400
    return jsonify(response)
        
        
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8888')
