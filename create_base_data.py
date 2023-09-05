import json
import pandas as pd

def create_base():
    base = {}
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto']

    def set_drugs():
        df = pd.read_excel('xlsxs/agosto.xlsx')
        drugs = [x for x in df['Principio activo'].values]

        for drug in drugs:
            if drug not in base:
                base.setdefault(drug, {'Potencia': {}})

    def set_powers():
        df = pd.read_excel(F'xlsxs/agosto.xlsx')

        for index, row in df.iterrows():
            drug = row['Principio activo']
            power = row['Potencia']
            units = row['Unidades']
            if drug in base.keys():
                if power in base[drug]['Potencia'].keys():
                    base[drug]['Potencia'][power]['Unidades'].update({units: {'Meses': [], 'Precios': []}})
                else:
                    base[drug]['Potencia'].update({power: {'Unidades': {units: {'Meses': [], 'Precios': []}}}})

    def set_prices():
        for month in months:
            df = pd.read_excel(F'xlsxs/{month}.xlsx')

            for index, row in df.iterrows():
                drug = row['Principio activo']
                power = row['Potencia']
                units = row['Unidades']
                price = row['Precio de referencia']
                try:
                    base[drug]['Potencia'][power]['Unidades'][units]['Meses'].append(month)
                    base[drug]['Potencia'][power]['Unidades'][units]['Precios'].append(price)
                except:
                    pass
                
    set_drugs()
    set_powers()
    set_prices()

    with open('base.json', 'w') as file:
        json.dump(base, file, indent=4)

    return base

base = create_base()