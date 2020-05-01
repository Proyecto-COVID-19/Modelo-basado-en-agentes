import runner

city = 'bogota'
m = 100


rn = runner.Runner('../Datos/Datos para el modelov2.xlsx', city, m, 7715778,  1636)
data = rn.run(6)
data.to_csv('results_{}_{}_l10_45k.csv'.format(city, m))