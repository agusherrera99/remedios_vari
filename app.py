import json
import streamlit as st
import matplotlib.pyplot as plt

with open('base.json', 'r') as file:
    base = json.load(file)

st.header(F'Precio de Medicamentos - 2023 (Variación Anual Disponible)')

drug_name = st.selectbox(label='Selecciona un medicamento:', options=base.keys())
power_options = st.selectbox(label='Seleciona la potencia:', options=base[drug_name]['Potencia'].keys())
units_options = st.selectbox(label='Selecciona las unidades:', options=base[drug_name]['Potencia'][power_options]['Unidades'].keys())
prod_form = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Forma Farmaceutica']

months = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Meses']
ars_price = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Precios']
usd_price = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['USD_Precios']

def create_plots(currency, dollar=False, fontsize=14):

    def addValueToBar(bars, dollar=False):
        for bar in bars:
            yval = bar.get_height()
            if dollar:
                formatted_yval = "${:,.2f}".format(yval)
                ax.text((bar.get_x() + bar.get_width() / 2), (yval), formatted_yval, ha='center', va='bottom', fontsize=fontsize)
            else:
                formatted_yval = "${:,.0f}".format(round(yval))
                ax.text((bar.get_x() + bar.get_width() / 2), (yval), formatted_yval, ha='center', va='bottom', fontsize=fontsize)

    x = months
    y = currency

    fig, ax = plt.subplots(figsize=(12, 10))
    
    if dollar:
        bars = ax.bar(x=x, height=y, tick_label=x, color='#4ade80')
        ax.set_title(F'Variación del Precio en Dólares\n Medicamento: {drug_name.title()}', fontsize=fontsize)
        ax.set_xlabel('Meses', fontsize=fontsize)
        ax.set_ylabel('Precio en Dólares', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)

        addValueToBar(bars, dollar=True)
    else:
        bars = ax.bar(x=x, height=y, tick_label=x, color='#60a5fa')
        ax.set_title(F'Variación del Precio\n Medicamento: {drug_name.title()}', fontsize=fontsize)
        ax.set_xlabel('Meses', fontsize=fontsize)
        ax.set_ylabel('Precio en Pesos', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)

        addValueToBar(bars)

    st.pyplot(fig)

st.subheader(F'Precio actúal {"${:,.0f}".format(ars_price[-1])}')

plot_check = st.checkbox(label='Ver Variación Anual')
if plot_check:
    create_plots(ars_price)
    create_plots(usd_price, dollar=True)
st.info('Data: https://www.argentina.gob.ar/salud/seguimiento-de-precios/ano-2023 | GitHub: https://github.com/agusherrera99/remedios_vari | Autor: agustinherrera.dev@gmail.com')