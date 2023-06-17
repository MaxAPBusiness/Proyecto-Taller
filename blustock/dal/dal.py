"""Este módulo contiene una clase para gestionar el envío de datos
entre la base de datos y la IU.

Clases
------
    DAL():
"""
import os
from db.bdd import bdd

class DAL():
    """Esta clase contiene métodos que gestionan el envío de datos
    entre la base de datos y la IU.
    
    Métodos
    ---------
        obtenerDatos(self, tabla: str, busqueda: str, 
        filtrosExtra: list | tuple | dict | None = None):
    """
    def obtenerDatos(self, tabla: str, busqueda: str, 
        filtrosExtra: list | tuple | dict | None = None) -> list:
        """Este método obtiene y devuelve datos de la base de datos

        Parámetros
        ----------
            tabla: str
                La tabla de la base de datos de la que se obtendrán los
                datos.
            busqueda: str
                El texto ingresado en la barra de búsqueda de la ui,
                que se usará como filtro de los datos.
            filtrosExtra: list | tuple | dict | None = None
                Un objeto iterable (lista, tupla o diccionario) que 
                contendrá todos los filtros extra que se quieran usar
                para filtrar la obtención de los datos.
                Default: None.
        
        Devuelve
        --------
            list: los datos obtenidos organizados en una lista.
        """
        # Abriendo el archivo sql con la consulta usando la tabla
        # pedida...
        with open(f"{os.getcwd()}{os.sep}blustock{os.sep}dal{os.sep}queries{os.sep}{tabla}.sql", 'r') as queryText:
            # Obtenemos y guardamos el código sql como texto
            query=queryText.read()
            # Inicializamos la lista con los filtros que se usarán en
            # la obtención.
            filtro = []
            # Si se han aportado filtros extra...
            if filtrosExtra:
                # Obtenemos la cantidad de filtros extra aportados
                cantFiltrosExtra=len(filtrosExtra)
                # Insertamos los filtros extra en la lista de filtros
                filtro.extend(filtrosExtra)
            else:
                # Se establece que la cantidad de filtros extra es 0
                cantFiltrosExtra=0
            # Cada "?" en el código sql indica que usaremos un dato de
            # python. Para aplicar la búsqueda en la obtención
            # correctamente, debemos ver si algún campo de la tabla 
            # contiene lo buscado. Por eso, por cada campo que queramos
            # comparar con la búsqeda debe haber un "?". Tenemos que
            # aportar una lista o tupla que contenga un elemento de
            # texto por cada "?". Por ejemplo, si queremos consultar
            # por 6 campos por cada fila, tendremos que pasar una lista
            # con 6 elementos iguales, todos siendo el texto de
            # búsqueda. El bucle de abajo mira cuantos "?" tiene la 
            # consulta y agrega a la lista filtro (que se va a pasar
            # como filtro en la obtención) la cantidad de textos de 
            # búsqueda adecuados. NOTA: Como también puede haber
            # filtros extra, y va a haber un "?" por cada filtro extra,
            # la cantidad de comparaciones de búsqueda se obtiene
            # contando los "?" y restando la cantidad de filtros extra.
            for i in range(query.count('?')-cantFiltrosExtra):
                filtro.append(f"%{busqueda}%")
            # Consulta los datos y los devuelve.
            return bdd.cur.execute(query, filtro).fetchall()


# Se crea el objeto que será usado por los demás módulos para acceder
# a las funciones.
dal=DAL()