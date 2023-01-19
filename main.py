import os
from os import getenv
from urllib.parse import urlparse, urlencode

import customtkinter
import pymssql
from winotify import Notification, audio

from print import print_label
from win10toast import ToastNotifier

from window import App

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Zmienne środowiskowe z pliku env
server = getenv("PYMSSQL_TEST_SERVER")
user = getenv("PYMSSQL_TEST_USERNAME")
password = getenv("PYMSSQL_TEST_PASSWORD")
database = getenv("PYMSSQL_TEST_DATABASE")
port = getenv("PYMSSQL_TEST_PORT")
charset = 'WINDOWS-1252'
# charset = 'UTF-8'
# charset = 'utf8'
# charset = 'Polish_CI_AS'
# charset = "ISO-8859-1"
# charset = "LATIN1"
# charset='iso-8859-1'
# conn = pymssql.connect(server, user, password, database)

# https://www.pymssql.org/ref/pymssql.html
conn = pymssql.connect(server=server, user=user, password=password, database=database, timeout=0, login_timeout=60, charset=charset, as_dict=True, host='', appname=None, port=port)
print(pymssql.version_info())

# można też tak, ale sensowniej jest jak wyżej z pliku env
# conn = pymssql.connect(
#     host=r'dbhostname\myinstance',
#     user=r'companydomain\username',
#     password=PASSWORD,
#     database='GastroAdong'
# )

products = list()


def puknijDoBazy():
    cursor = conn.cursor(as_dict=True)

    plu_end = 300
    poziom_cenowy_id = '745B467C-2477-416E-9E40-B313B3E6D792'

    query = f"""SELECT 
        TOP 12 
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
        # name = row['NazwaTowaru'].encode('UTF-8', "ignore")
        print(f"ID:{row['ID']}, Nazwa:{row['NazwaTowaru']} PLU:{row['PLU']} Cena w lokalu:{row['CenaLokal']}")
        products.append(row)

    # wywolajProcedure(poziom_cenowy_id)
    conn.close()




def drukujEtykiety():
    print('drukuje etykiety')
    print(products)
    for product in products:
        result_print = print_label(product['NazwaTowaru'], '1 z (3)', 'ID_2344', 'L_332')
        print(result_print)


def wywolajProcedure(param1):
    cursor = conn.cursor(as_dict=True)
    cursor.callproc('pv_NGastroPosTowarCena_PoziomCenowyID', (param1,))
    for row in cursor:
        print("TowarID=%s, Name=%s" % (row['TowarID'], row['Cena']))


def mojaFunkcjaWitaj(name):
    print(f'Witaj, {name}')


def pokazToast():
    t = ToastNotifier()
    t.show_toast("Tytuł tosta", "Zrobione złotko co sądzisz o wyniku w konsoli", duration=4)


def pokazToast2():
    script_dir = os.path.dirname(__file__)
    rel_path = "favicon.png"
    icon = os.path.join(script_dir, rel_path)
    message = "Wiadomość do wyświetlenia  \nWiadomość do wyświetlenia  \nWiadomość do wyświetlenia  \nWiadomość do wyświetlenia "
    toast = Notification(app_id="A-DONG Darek",
                         title="W konsoli pokazuje się status pobrania danych z bazy gastro",
                         msg=message,
                         duration="long",
                         icon=icon,
                         )
    # dzwięk
    toast.set_audio(audio.Mail, loop=False)
    # Akcja
    # https://a-donggdansk.pl/admin/orders?selected_order_id=230&archive=1
    url = "https://a-donggdansk.pl/admin/orders"
    params = {'selected_order_id': '230', 'archive': '1'}

    # url += ('&' if urlparse(url).query else '?') + urlencode(params)
    print(url)
    toast.add_actions(label="Zobacz nowe zamówienie 230", launch=url)
    toast.show()


def okienko():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')
    root = customtkinter.CTk()
    root.geometry("500x300")
    root.title("Tytuł okienka")
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=frame, text="Hello World")
    label.pack(pady=12, padx=10)
    # button = customtkinter.CTkButton(master=frame, text="Pokaż tost windows", command=pokazToast)
    # button.pack(pady=12, padx=10)
    button2 = customtkinter.CTkButton(master=frame, text="Pokaż tost 2 windows", command=pokazToast2)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame, text="Drukuj etykiety", command=drukujEtykiety)
    button3.pack(pady=12, padx=10)

    root.mainloop()


if __name__ == '__main__':
    mojaFunkcjaWitaj('Darek')
    puknijDoBazy()
    # result_print = print_label('Kaczka dziwaczka', '1 z (3)', 'ID_2344', 'L_332')
    # print(result_print)
    # pokazToast()
    okienko()
    # app = App()
    # app.mainloop()
