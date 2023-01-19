from os import getenv
import pymssql
from print import print_label

# Zmienne środowiskowe z pliku env
server = getenv("PYMSSQL_TEST_SERVER")
user = getenv("PYMSSQL_TEST_USERNAME")
password = getenv("PYMSSQL_TEST_PASSWORD")
database = getenv("PYMSSQL_TEST_DATABASE")

conn = pymssql.connect(server, user, password, database)


# można też tak, ale sensowniej jest jak wyżej z pliku env
# conn = pymssql.connect(
#     host=r'dbhostname\myinstance',
#     user=r'companydomain\username',
#     password=PASSWORD,
#     database='GastroAdong'
# )

def puknijDoBazy():
    cursor = conn.cursor(as_dict=True)
    plu_end = 300
    poziom_cenowy_id = '745B467C-2477-416E-9E40-B313B3E6D792'

    query = f"""SELECT 
        TOP 2 
            t.NumerPLU as PLU, 
            t.NazwaTowaru, 
            t.ID, c.Cena as 'CenaLokal' 
        FROM NgastroTowar t 
        LEFT JOIN NGastroCena c ON c.TowarID=t.ID 
            AND c.PoziomCenowyID='{poziom_cenowy_id}'
        WHERE 
            t.NumerPLU<{plu_end}
    """
    cursor.execute(query)
    for row in cursor:
        print(f"ID:{row['ID']}, Nazwa:{row['NazwaTowaru']} PLU:{row['PLU']} Cena w lokalu:{row['CenaLokal']}")

    # wywolajProcedure(poziom_cenowy_id)
    conn.close()


def wywolajProcedure(param1):
    cursor = conn.cursor(as_dict=True)
    cursor.callproc('pv_NGastroPosTowarCena_PoziomCenowyID', (param1,))
    for row in cursor:
        print("TowarID=%s, Name=%s" % (row['TowarID'], row['Cena']))


def mojaFunkcjaWitaj(name):
    print(f'Witaj, {name}')


if __name__ == '__main__':
    mojaFunkcjaWitaj('Darek')
    puknijDoBazy()
    result_print = print_label('Kaczka dziwaczka', '1 z (3)', 'ID_2344', 'L_332')
    print(result_print)
