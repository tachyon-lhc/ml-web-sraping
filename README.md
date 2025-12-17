# ml-web-sraping

## Web scraper para extraer información de propiedades en venta en MercadoLibre Argentina

![Web de MercadoLibre](./images/web_ml.png)

## Ejemplo de datos generados

El scraper genera un archivo CSV con la siguiente estructura:

| id  | price  | rooms | bathrooms | square_meters | zone                  | city  | price_per_m2 |
| --- | ------ | ----- | --------- | ------------- | --------------------- | ----- | ------------ |
| 1   | 90000  | 3     | 1         | 112           | Buenos Aires Interior | Lujan | 804          |
| 2   | 115000 | 4     | 3         | 170           | Buenos Aires Interior | Lujan | 676          |
| 3   | 148000 | 5     | 2         | 140           | Buenos Aires Interior | Lujan | 1057         |
| 4   | 160000 | 4     | 2         | 210           | Buenos Aires Interior | Lujan | 762          |
| 5   | 175000 | 4     | 3         | 900           | Buenos Aires Interior | Lujan | 194          |

## Estructura base

<pre>
ml-web-scraping/
├── images/
├── src/
│   ├── analysis/
│   ├── cleaning/
│   ├── processing/
│   ├── scraper/
│   ├── test/
│   └── main.py
├── data/
├── requirements.txt
└── README.md
</pre>
