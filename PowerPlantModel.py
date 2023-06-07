from flask import jsonify
from PowerPlantType import PowerPlantType

class PowerPlant:
    def __init__(self, name, plantType, efficiency, pmax, pmin):
        self.name = name
        self.plantType = plantType
        self.efficiency = efficiency
        self.pmax = pmax
        self.pmin = pmin
        

class PowerPlantModel:
    def __init__(self):
        self.powerPlants = []
        
    def addPowerPlant(self, name, plantType, efficiency, pmax, pmin):
        powerPlant = PowerPlant(name, plantType, efficiency, pmax, pmin)
        self.powerPlants.append(powerPlant)

    def orderedMerit(self, fuels):
        sortedPowerPlants = sorted(self.powerPlants, key=lambda powerPlant: self.calculateGenerationCost(powerPlant, fuels))
        return sortedPowerPlants
    
    def calculateGenerationCost(self,powerPlant, fuels):
        generationCostLookup = {
            PowerPlantType.WINDTURBINE.value: 0,
            PowerPlantType.GASFIRED.value: fuels["gas(euro/MWh)"] * (1 / powerPlant.efficiency),
            PowerPlantType.TURBOJET.value: fuels["kerosine(euro/MWh)"] * (1 / powerPlant.efficiency)
        }
        return generationCostLookup.get(powerPlant.plantType, 0)
    
    def updateWindTurbinePminAndPmax(self,fuels):
        for powerPlant in self.powerPlants:
            if PowerPlantType.WINDTURBINE.value==powerPlant.plantType:
                powerPlant.pmax = powerPlant.pmax*fuels["wind(%)"]/100
                powerPlant.pmin = powerPlant.pmin*fuels["wind(%)"]/100
                
    def generatePower(self, load, fuels):
        remainLoad = load 
        plan = []
        self.updateWindTurbinePminAndPmax(fuels)
        merit = self.orderedMerit(fuels)
        for index, powerplant in enumerate(merit):
            if remainLoad == 0:
                plan.append({'name': powerplant.name,'p': 0})
            else:
                if remainLoad >= powerplant.pmin:
                    if powerplant.pmax < remainLoad:
                        #check the next one 
                        tmp = index +1 
                        if( tmp<len(merit)):
                            nextPowerPlan = merit[index+1]
                            if (remainLoad - powerplant.pmax ) < nextPowerPlan.pmin:
                                p = remainLoad - merit[index+1].pmin
                                plan.append({'name': powerplant.name,'p': p})
                                remainLoad = nextPowerPlan.pmin
                            else:
                                plan.append({'name': powerplant.name,'p': powerplant.pmax})
                                remainLoad = remainLoad - powerplant.pmax
                        else: 
                            raise Exception("Load exceeds the capacity of all power plants.")
 
                    else:
                        plan.append({'name': powerplant.name,'p': remainLoad})
                        remainLoad = 0
                else:
                    pass
                
        return plan