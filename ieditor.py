from tkinter import *
from tkinter import ttk
import uuid, json, os, io

global my_data_list
my_data_list = []
FilePath = 'item.json'
field01 = 'title'
field02 = 'a'
field03 = 'b'
field04 = 'c'
field05 = 'd'
field06 = 'ans'

def startup_check():
    if os.path.isfile(FilePath) and os.access(FilePath, os.R_OK):
        print("File exists and is readable")
    else:
        print("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(FilePath), 'w') as db_file:
            db_file.write(json.dumps([]))

def load_json_from_file():
    global my_data_list
    with open(FilePath,"r") as file_handler:
        my_data_list = json.load(file_handler)
    file_handler.close
    print('File has been read and closed')

def save_json_to_file():
    global my_data_list
    with open(FilePath, "w") as file_handler:
        json.dump(my_data_list, file_handler, indent=4)
    file_handler.close
    print('File has been written to and closed')

def remove_all_data_from_trv():
    for item in trv.get_children():
        trv.delete(item)

def load_trv_with_json():
    global my_data_list
    remove_all_data_from_trv()
    rowIndex=1

    for key in my_data_list:
        guid_value = key["id"]
        title = key[field01]
        a = key[field02]
        b = key[field03]
        c = key[field04]
        d = key[field05]
        ans = key[field06]
        trv.insert('',index='end',iid=rowIndex,text="",values=(guid_value,title,a,b,c,d,ans))    
        rowIndex=rowIndex+1

def clear_all_fields():
    crm_title.delete(0,END)
    crm_a.delete(0,END)
    crm_b.delete(0,END)
    crm_c.delete(0,END)
    crm_d.delete(0,END)
    crm_ans.delete(0,END)
    crm_id.configure(text="")
    crm_title.focus_set()
    id_value.set(uuid.uuid4())
    change_background_color("#FFFFFF")

def find_row_in_my_data_list(guid_value):
    global my_data_list
    row     = 0
    found   = False

    for rec in my_data_list:
        if rec["id"] == guid_value:
            found = True
            break
        row = row+1

    if(found==True):
        return(row)

    return(-1)

def change_background_color(new_color):
    crm_title.config(bg=new_color)
    crm_a.config(bg=new_color)
    crm_b.config(bg=new_color)
    crm_c.config(bg=new_color)
    crm_d.config(bg=new_color)
    crm_ans.config(bg=new_color)

def change_enabled_state(state):

    if state == 'Edit':
        btnUpdate["state"]="normal"
        btnDelete["state"]="normal"
        btnAdd["state"]="disabled"
    elif state=='Cancel':
        btnUpdate["state"]="disabled"
        btnDelete["state"]="disabled"
        btnAdd["state"]="disabled"
    else:
        btnUpdate["state"]="disabled"
        btnDelete["state"]="disabled"
        btnAdd["state"]="normal"

def load_edit_field_with_row_data(_tuple):
    if len(_tuple)==0:
        return

    id_value.set(_tuple[0])
    crm_title.delete(0,END)
    crm_title.insert(0,_tuple[1])
    crm_a.delete(0,END)
    crm_a.insert(0,_tuple[2])
    crm_b.delete(0,END)
    crm_b.insert(0,_tuple[3])
    crm_c.delete(0,END)
    crm_c.insert(0,_tuple[4])
    crm_d.delete(0,END)
    crm_d.insert(0,_tuple[5])
    crm_ans.delete(0,END)
    crm_ans.insert(0,_tuple[6])

def cancel():
    clear_all_fields()
    change_enabled_state('New')

def print_all_entries():
    global my_data_list

    for rec in my_data_list:
        print(rec)

    crm_title.focus_set()

def add_entry():
    guid_value = id_value.get()
    title = crm_title.get()
    a = crm_a.get()
    b = crm_b.get()
    c = crm_c.get()
    d = crm_d.get()
    ans = crm_ans.get()

    if len(title)==0:
        change_background_color("#FFB2AE")
        return

    process_request('_INSERT_',guid_value,title,a,b,c,d,ans)

def update_entry():
    guid_value = id_value.get()
    title = crm_title.get()
    a = crm_a.get()
    b = crm_b.get()
    c = crm_c.get()
    d = crm_d.get()
    ans = crm_ans.get()

    if len(title)==0:
        change_background_color("#FFB2AE")
        return

    process_request('_UPDATE_',guid_value,title,a,b,c,d,ans)

def delete_entry():
    guid_value = id_value.get()
    process_request('_DELETE_',guid_value,None,None,None,None,None,None)

def process_request(command_type,guid_value,title,a,b,c,d,ans):
    global my_data_list

    if command_type == "_UPDATE_":
        row = find_row_in_my_data_list(guid_value)
        if row >= 0:
            dict = {"id":guid_value, field01:title, 
                    field02:a, field03:b, field04:c, field05:d, field06:ans}
            my_data_list[row]=dict

    elif command_type == "_INSERT_":
        dict = {"id":guid_value, field01:title, 
                field02:a, field03:b, field04:c, field05:d, field06:ans}
        my_data_list.append(dict)

    elif command_type == "_DELETE_":
        row = find_row_in_my_data_list(guid_value)
        if row >= 0:
            del my_data_list[row]

    save_json_to_file()
    load_trv_with_json()
    clear_all_fields()

def MouseButtonUpCallBack(event):
    try:
        currentRowIndex = trv.selection()[0]
        lastTuple = (trv.item(currentRowIndex,'values'))
        load_edit_field_with_row_data(lastTuple)
        change_enabled_state('Edit')
    except IndexError:
        print("Index width has been adjusted")

root = Tk()
root.title('Item Editor')
root.geometry("1024x768")
root.configure(bg='lightgray')

margin = Label(text=" ",bg="lightgray")
margin.grid(row=0,column=0)

input_frame = LabelFrame(root,text='Info',bg="lightgray",font=('Consolas',14))
input_frame.grid(row=0,column=1,rowspan=7,columnspan=4)

l1 = Label(input_frame, anchor="w", width=24,
           height=1, relief="ridge", text="id",
           font=('Consolas',14)).grid(row=1, column=0)

l2 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text=field01,
           font=('Consolas',14)).grid(row=2, column=0)

l3 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text=field02,
           font=('Consolas',14)).grid(row=3, column=0) 

l4 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text=field03,
           font=('Consolas',14)).grid(row=4, column=0)

l5 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text=field04,
           font=('Consolas',14)).grid(row=5, column=0)

l6 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text=field05,
           font=('Consolas',14)).grid(row=6, column=0)

l7 = Label(input_frame, anchor="w", width=24, 
           height=1, relief="ridge", text="ans", 
           font=('Consolas',14)).grid(row=7, column=0)

id_value = StringVar()
id_value.set(uuid.uuid4())

crm_id = Label(input_frame, anchor="w", height=1,
           relief="ridge", textvariable=id_value, font=('Consolas',14))
crm_id.grid(row=1, column=1)

crm_title = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_title.grid(row=2, column=1,columnspan=2)

crm_a = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_a.grid(row=3, column=1,columnspan=2)

crm_b = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_b.grid(row=4, column=1,columnspan=2)

crm_c = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_c.grid(row=5, column=1,columnspan=2)

crm_d = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_d.grid(row=6, column=1,columnspan=2)

crm_ans = Entry(input_frame,width=30,borderwidth=2,fg="black",font=('Consolas',14))
crm_ans.grid(row=7, column=1,columnspan=2)

ButtonFrame = LabelFrame(root,text='',bg="lightgray",font=('Consolas',14))
ButtonFrame.grid(row=8,column=0,columnspan=6)

btnShow=Button(ButtonFrame,text="Print",padx=20,pady=10,command=print_all_entries)
btnShow.pack(side=LEFT)

btnAdd=Button(ButtonFrame,text="Add",padx=20,pady=10,command=add_entry)
btnAdd.pack(side=LEFT)

btnUpdate=Button(ButtonFrame,text="Update",padx=20,pady=10,command=update_entry)
btnUpdate.pack(side=LEFT)

btnDelete=Button(ButtonFrame,text="Delete",padx=20,pady=10,command=delete_entry)
btnDelete.pack(side=LEFT)

btnClear=Button(ButtonFrame,text="Cancel",padx=18,pady=10,command=cancel)
btnClear.pack(side=LEFT)

btnExit=Button(ButtonFrame,text="Exit",padx=20,pady=10,command=root.quit)
btnExit.pack(side=LEFT)

trv = ttk.Treeview(root,columns=(1,2,3,4,5,6,7),show="headings",height="16")
trv.grid(row=9,column=0,rowspan=16,columnspan=7)

trv.heading(1,text="id", anchor="center")
trv.heading(2,text=field01, anchor="center")
trv.heading(3,text=field02, anchor="center")
trv.heading(4,text=field03, anchor="center")
trv.heading(5,text=field04, anchor="center")
trv.heading(6,text=field05, anchor="center")
trv.heading(7,text=field06, anchor="center")
trv.column("#1",anchor="w",width=230, stretch=True)
trv.column("#2",anchor="w", width=200, stretch=False)
trv.column("#3",anchor="w", width=100, stretch=False)
trv.column("#4",anchor="w", width=100, stretch=False)
trv.column("#5",anchor="w", width=100, stretch=False)
trv.column("#6",anchor="w", width=100, stretch=False)
trv.column("#7",anchor="w", width=50, stretch=False)
trv.bind("<ButtonRelease>",MouseButtonUpCallBack)

scrollbar = Scrollbar(root, orient=VERTICAL, command=trv.yview)
trv.configure(yscroll=scrollbar.set)
scrollbar.grid(row=9,rowspan=16,column=8,sticky='ns')

startup_check()
load_json_from_file()
load_trv_with_json()
crm_title.focus_set()
root.mainloop()
