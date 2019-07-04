import requests
from bs4 import BeautifulSoup
from tinybird import Datasource


URL = 'http://informo.munimadrid.es/informo/tmadrid/pm.xml'
ATTRS = ['idelem', 'descripcion', 'accesoAsociado', 'intensidad', 'ocupacion', 'carga', 'velocidad', 'nivelServicio', 'intensidadSat', 'error', 'subarea', 'st_x', 'st_y']

def run(create_token):
    r = requests.get(URL)
    if r.status_code == 200:
        xml = BeautifulSoup(r.content, "xml")
        timestamp = xml.fecha_hora.string
        rows = []

        with Datasource('madrid_rt_traffic', create_token) as tinyb:
            # timestamp
            tinyb.header(['timestamp'] + ATTRS)
            for el in xml.find_all("pm"):
                row = [getattr(el, x, None) for x in ATTRS]
                tinyb << [timestamp] + [x.string if x else None for x in row]


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) < 2:
        print("needs two arguments")
        sys.exit()
    run(sys.argv[1])
