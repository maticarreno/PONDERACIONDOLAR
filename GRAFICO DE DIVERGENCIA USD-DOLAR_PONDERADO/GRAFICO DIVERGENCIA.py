import requests
import pandas as pd
import matplotlib.pyplot as plt

#Añadir Token de https://estadisticasbcra.com/api/registracion
token = "BEARER  "

def get_historical_data(endpoint):
    url = "https://api.estadisticasbcra.com/" + endpoint
    headers = {"Authorization": token}
    data_json = requests.get(url, headers=headers).json()
    data = pd.DataFrame(data_json)
    data.set_index("d", inplace=True, drop=True)
    return data

def calculo_dolar_ponderado(base_monetaria, leliq, lebac, reserva_internacional):
    return (base_monetaria + leliq + lebac) / reserva_internacional

#Reemplazar usd_of por cualquier endpoint para comparar otra variable
dolar_oficial_data = get_historical_data("usd_of")
base_monetaria_data = get_historical_data("base")
leliq_data = get_historical_data("leliq")
lebac_data = get_historical_data("lebac")
reserva_internacional_data = get_historical_data("reservas")

dolar_ponderado = calculo_dolar_ponderado(base_monetaria_data['v'], leliq_data['v'], lebac_data['v'], reserva_internacional_data['v'])

fechas_comunes = dolar_oficial_data.index.intersection(dolar_ponderado.index)

dolar_oficial_filtrado = dolar_oficial_data.loc[fechas_comunes]
dolar_ponderado_filtrado = dolar_ponderado.loc[fechas_comunes]

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [15, 6]

plt.plot(dolar_oficial_filtrado.index, dolar_oficial_filtrado['v'], label='dolar_of', color='blue', linestyle=':')
plt.plot(dolar_oficial_filtrado.index, dolar_ponderado_filtrado, label='dolar_ponderado', color='red', linestyle=':')
plt.xlabel('d')
plt.ylabel('v')
plt.title('Divergencia')

plt.legend()
plt.grid(True)
plt.show()

