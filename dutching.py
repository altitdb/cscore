def calculate_dutching_stakes(probabilidades, aposta_total):
    inversos = [1 / odd for odd in probabilidades]
    soma_inversos = sum(inversos)
    apostas = [aposta_total / (odd * soma_inversos) for odd in probabilidades]
    return apostas


def calculate_dutching_gain(probabilidades, aposta_total):
    apostas = [aposta_total / odd for odd in probabilidades]
    return apostas


probabilidades_neutras = [6.8,6.4,12,32,8.4,6.2,11,30,19.5,14,21,60,60,50,75,180,8.8,7.8,130]
probabilidades_neutras = [6.8]
probabilidades_valor = [6.8,6.4,12,32,8.4,6.2,11,30,19.5,14,21,60,60,50,75,180,8.8,7.8,130]
probabilidades_valor = [6.4,11.5,9.2,6.6,11.5]
stake = 50

apostas_neutras = calculate_dutching_gain(probabilidades_neutras, stake)
stake_neutra = sum(apostas_neutras)
print(f'Aposta neutra: {stake_neutra:.2f}')

stake_valor = stake - stake_neutra
print(f'Aposta valor: {stake_valor:.2f}')

print('Stakes neutras')
apostas = calculate_dutching_stakes(probabilidades_neutras, stake_neutra)
for i, aposta in enumerate(apostas):
    print(f"Aposta {i+1}: {aposta:.2f}")

print('Stakes valor')
apostas = calculate_dutching_stakes(probabilidades_valor, stake_valor)
for i, aposta in enumerate(apostas):
    print(f"Aposta {i+1}: {aposta:.2f}")

print('Expected profit')
expected_profit = 0
for i, aposta in enumerate(apostas):
    expected_profit += (probabilidades_valor[i] * aposta)
profit = expected_profit / len(apostas) - 100
print(f"Profit {profit:.2f}")