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
            unit_power_type = row['Unidad de potencia']
            units = row['Unidades']
            prod_type = row['Tipo']
            if drug in base.keys():
                if power in base[drug]['Potencia'].keys():
                    base[drug]['Potencia'][F'{power} {unit_power_type}']['Unidades'].update({F'{units} {prod_type}': {'Meses': [], 'Precios': [], 'USD_Precios': []}})
                else:
                    base[drug]['Potencia'].update({F'{power} {unit_power_type}': {'Unidades': {F'{units} {prod_type}': {'Meses': [], 'Precios': [], 'USD_Precios': []}}}})

    def set_prices():
        dls_vpm = pd.read_excel('xlsxs/dollar_value_per_month.xlsx')

        for month in months:
            df = pd.read_excel(F'xlsxs/{month}.xlsx')

            for index, row in df.iterrows():
                drug = row['Principio activo']
                power = row['Potencia']
                units = row['Unidades']
                unit_power_type = row['Unidad de potencia']
                prod_type = row['Tipo']
                prod_form = row['Forma farmacéutica']
                price = row['Precio de referencia']
                try:
                    base[drug]['Potencia'][F'{power} {unit_power_type}']['Unidades'][F'{units} {prod_type}']['Meses'].append(month)
                    base[drug]['Potencia'][F'{power} {unit_power_type}']['Unidades'][F'{units} {prod_type}']['Precios'].append(price)
                    base[drug]['Potencia'][F'{power} {unit_power_type}']['Unidades'][F'{units} {prod_type}']['Forma Farmaceutica'] = prod_form
                    base[drug]['Potencia'][F'{power} {unit_power_type}']['Unidades'][F'{units} {prod_type}']['USD_Precios'].append(price / dls_vpm[month].values[0])
                except:
                    pass
                
    set_drugs()
    set_powers()
    set_prices()

    with open('base.json', 'w') as file:
        json.dump(base, file, indent=4)

    return base

base = create_base()