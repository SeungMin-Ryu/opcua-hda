import sys
sys.path.insert(0, "..")
mod = sys.modules[__name__]
import os
import socket

from hda_agg_module.hda_gen_client_module import *
from opcua import ua, Server
from hda_agg_module.hda_agg_module import HistorySQLite
from tkinter import *
from tkinter import filedialog
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from PIL import Image, ImageTk



def open_file():
    filename = filedialog.askopenfilename(initialdir='../CI_image', title='Select A excel File',
                                          filetypes=(("excel file", "*.xlsx"), ("all file", "*.*")))
    wb = load_workbook(filename)
    ws = wb.active

    all_value=[]
    for row in ws.rows:
        row_value = []
        for cell in row:
            row_value.append(cell.value)
        all_value.append(row_value)
        list_box.insert(END, row_value[0] + '-' + row_value[1])


def quit_program():
    win.destroy()
    win.quit()
    server.stop()
    os._exit(1)

def pass_func():
    pass

def DELETE_BUTTON():
    list_box.delete(ANCHOR)


def ADD_BUTTON():
    ip = input1.get()
    node_id = input2.get()
    if len(ip) != 0 and len(node_id) != 0:
        list_box.insert(END, ip+'-'+node_id)


def EXECUTE_BUTTON():
    node = list(list_box.get(first=0, last=END))
    if len(node) != 0:
        for n in node:
            nodesplit = n.split('-')
            client = aggclient(nodesplit[0], nodesplit[1])
            client.connection()
        config_server()
        main()

def START():
    global input1, input2, list_box, ip_label, node_label, execute_btn

    ip_label = Label(win, text = 'Endpoint_Url')
    node_label = Label(win, text= 'Node_Id')

    input1 = Entry(win, width=35)
    input2 = Entry(win, width=35)

    start_btn.config(text='ADD', width=4, height=2, command=ADD_BUTTON, overrelief='solid',
                     relief='ridge', bg='silver')
    delete_btn = Button(win, text='DELETE', overrelief='solid', relief='groove')
    delete_btn.config(width=8,height=2,command=DELETE_BUTTON,bg='silver')

    # scrollbar = Scrollbar(win,orient=VERTICAL)

    list_box = Listbox(win, width=70, height=13)
    # scrollbar.config(command=list_box.yview)


    execute_btn = Button(win, text='EXECUTE')
    execute_btn.config(command=EXECUTE_BUTTON, overrelief='solid', relief='groove', bg='silver',width=85)

    ip_label.place(x=125, y=220)
    node_label.place(x=135, y=250)
    input1.place(x=250, y=220)
    input2.place(x=250, y=250)
    start_btn.place(x=650, y=220)
    delete_btn.place(x=715, y=220)
    excel_btn.place(x=820, y=220)

    list_box.grid(row=3, column=0, columnspan=2,pady=32)

    execute_btn.grid(row=4,column=0, columnspan=2)

def config_server():
    client_node_id = list(Global.node_display.keys())
    client_display_name = list(Global.node_display.values())
    client_variable_type = list(Global.node_type.values())
    address = str(socket.gethostbyname(socket.getfqdn()))
    server.set_endpoint("opc.tcp://"+address+":52520")
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()
    myobj = objects.add_object(idx, "MyObject")
    server.iserver.history_manager.set_storage(HistorySQLite())
    server.start()

    count = 0
    for server_display_name in client_display_name:
        globals()['node_{}'.format(count)] = myobj.add_variable(client_node_id[count],
                                                                server_display_name,
                                                                0,
                                                                client_variable_type[count])
        server.historize_node_data_change(globals()['node_{}'.format(count)], period=None, count=100)
        count += 1




def main():
    localhost = server.endpoint.geturl()
    win1 = Tk()
    win1.geometry('400x100')
    win1.title('RUNNING...')
    win1.resizable(False, False)
    win1.protocol('WM_DELETE_WINDOW', pass_func)
    run_label = Label(win1, text='Listening on ' + localhost + '...')
    quit_btn = Button(win1, text='QUIT',overrelief='solid',relief='groove', width=10)
    quit_btn.config(command=quit_program, bg='silver')


    while True:
        if Global.value and Global.node and Global.vartype is not None:
            print('들어옴')
            for num in range(0, len(Global.node)):
                server.get_node(Global.node[num]).set_value(value=Global.value[num],
                                                            varianttype=Global.vartype[num])
                run_label.place(x=75,y=30)
                quit_btn.place(x=310,y=70)
                win1.update()
                win.update()


if __name__ == "__main__":
    # client = aggclient("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer", "ns=3;i=1001")
    # client = aggclient("opc.tcp://172.21.42.31:4840", "ns=5;i=6023")
        server = Server()
        server_state = 0
        win = Tk()
        win.geometry('1000x632')
        win.resizable(False,False)
        win.title('Historian OPC UA Server generator')
        win.option_add("*Font", "맑은고딕 15")
        KETI = Image.open('../CI_image/KETI.png')
        SMIC = Image.open('../CI_image/SMIC.png')
        keti_resized = KETI.resize((500,250),Image.ANTIALIAS)
        smic_resized = SMIC.resize((500,250),Image.ANTIALIAS)

        KETI1 = ImageTk.PhotoImage(keti_resized)
        SMIC1 = ImageTk.PhotoImage(smic_resized)
        KETI_CI = Label(win, image=KETI1)
        SMIC_CI = Label(win, image=SMIC1)

        KETI_CI.grid(row=0, column=0)
        SMIC_CI.grid(row=0, column=1)

        explanation_label = Label(win, text='A program to generate a mysqlDB connected OPC UA server..')
        explanation_label.place(x=250, y=400)

        start_btn = Button(win, text='START',overrelief='solid',relief='groove', width=35)
        start_btn.config(command=START,bg='silver')
        start_btn.place(x=315, y=580)

        excel_image = Image.open('../CI_image/Excel-Logo.jpg')
        excel_resized = excel_image.resize((65, 50), Image.ANTIALIAS)
        excel = ImageTk.PhotoImage(excel_resized)
        excel_btn = Button(win, image=excel, overrelief='solid', relief='groove')
        excel_btn.config(command=open_file)

        win.mainloop()
