import json
import streamlit as st
import matplotlib.pyplot as plt

with open('base.json', 'r') as file:
    base = json.load(file)

fontsize = 14

def addValueToBar(bars):
        for bar in bars:
            yval = bar.get_height()
            formatted_yval = "${:,.0f}".format(round(yval))
            ax.text((bar.get_x() + bar.get_width() / 2), (yval), formatted_yval, ha='center', va='bottom', fontsize=fontsize)

st.header(F'Precio de Medicamentos - 2023 (Variación Anual Disponible)')

drug_name = st.selectbox(label='Selecciona un medicamento:', options=base.keys())
power_options = st.selectbox(label='Seleciona la potencia:', options=base[drug_name]['Potencia'].keys())
units_options = st.selectbox(label='Selecciona las unidades:', options=base[drug_name]['Potencia'][power_options]['Unidades'].keys())
prod_form = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Forma Farmaceutica']

months = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Meses']
prices = base[drug_name]['Potencia'][power_options]['Unidades'][units_options]['Precios']

x = months
y = prices

fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.bar(x=x, height=y)

ax.set_title(F'Variación del Precio\n Medicamento: {drug_name.title()}', fontsize=fontsize)
ax.set_xlabel('Meses', fontsize=fontsize)
ax.set_ylabel('Precio en Pesos', fontsize=fontsize)
ax.tick_params(axis='both', labelsize=fontsize)

addValueToBar(bars)

st.subheader(F'Precio actúal {"${:,.0f}".format(prices[-1])}')

plot_check = st.checkbox(label='Ver Variación Anual')
if plot_check:
    st.pyplot(fig)
st.info('Data: https://www.argentina.gob.ar/salud/seguimiento-de-precios/ano-2023 | GitHub: https://github.com/agusherrera99/remedios_vari | Autor: agustinherrera.dev@gmail.com')