import runner

city = 'bogota'
m = 250


rn = runner.Runner('../Datos/Datos para el modelov2.xlsx', city, m, 7715778,  1636)
data = rn.run(100)
data.to_csv('results_{}_{}.csv'.format(city, m))