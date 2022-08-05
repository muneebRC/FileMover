from faulthandler import disable
from ntpath import join
from queue import Empty
import shutil
import os
import threading
import time
from tkinter import filedialog
from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from configparser import ConfigParser
import configparser
import sys
import atexit
import subprocess
from turtle import update

def update_block():
    try:
        parser = ConfigParser()
        parser.read(r'info\versioninfo.ini')
        global current
        current = float(parser.get('version', 'current'))
        parser.read(r'latestversion.ini')
        global latest
        latest = float(parser.get('newversion', 'latest'))
        if current < latest:
            response = messagebox.askyesno('Update Available', 'Would you like to update to the latest version?\n\nCurrent Version: {0} > New version: {1}'.format(current, latest))
            if response == 1:
                subprocess.Popen(r'updater.exe')
                sys.exit()
            else:
                pass
    except Exception as e:
        messagebox.showwarning('Update Warning',f'Version file not found, please notify support@source4.com\n\n{e}')

                
update_block()

def start_message():
    try:
        parser = ConfigParser()
        parser.read(r'info\versioninfo.ini')
        global current
        current = float(parser.get('version', 'current'))
        messagebox.showwarning('FileMover v{0} "Experimental" '.format(current), 'This program is currently experimental, use at your own risk.\nFor questions contact muneeb.chaudhry@Source4.com or support@source4.com')
    except:
        current = "??"
        messagebox.showwarning('FileMover v{0} "Experimental" '.format(current), 'This program is currently experimental, use at your own risk.\nFor questions contact muneeb.chaudhry@Source4.com or support@source4.com')
start_message()

#Run Macro Loop
def playMacro():
    Run.config(state=DISABLED)
    templatePathc1 = r'{}'.format(folderPathC1.get())
    templatePathc2 = r'{}'.format(folderPathC2.get())
    templatePathc3 = r'{}'.format(folderPathC3.get())
    destC1 = r'{}'.format(DfolderPathC1.get())
    destC2 = r'{}'.format(DfolderPathC2.get())
    destC3 = r'{}'.format(DfolderPathC3.get())
    jig = selected.get()
    pbturns=0
    Doc = Doc_entry.get(1.0, END) #Get str from TextBox
    Doc = Doc.strip('\n')         # Removes trailing new lines. 
    list_doc = (Doc.split('\n'))  #Split str into list along 'spaces' 
    pbmax=len(list_doc)
    if jig == 'C1':
        if templatePathc1 == '' or destC1 == '':
            messagebox.showinfo("Error", 'Please set your source and destination paths.')
            Run.config(state=NORMAL)
            openSourceset()
            return
        else:
            os.chdir(templatePathc1)
            for name in list_doc:
                files = os.listdir(templatePathc1)
                for f in files:
                    if f.startswith(name):
                        shutil.copy(os.path.abspath(f), destC1)
                pbturns += 1
                pb['value']=(pbturns/pbmax)*100
                time.sleep(0.1)
                files1 = os.listdir(destC1)
    elif jig == 'C2':
        if templatePathc2 == '' or destC2 == '':
            messagebox.showinfo("Error", 'Please set your source and destination paths.')
            Run.config(state=NORMAL)
            openSourceset()
            return
        else:
            os.chdir(templatePathc2)
            for name in list_doc:
                files = os.listdir(templatePathc2)
                for f in files:
                    if f.startswith(name):
                        shutil.copy(os.path.abspath(f), destC2)
                pbturns += 1
                pb['value']=(pbturns/pbmax)*100
                time.sleep(0.1)
                files1 = os.listdir(destC2)
    elif jig == 'C3':
        if templatePathc3 == '' or destC3 == '':
            messagebox.showinfo("Error", 'Please set your source and destination paths.')
            Run.config(state=NORMAL)
            openSourceset()
            return
        else:
            os.chdir(templatePathc3)
            for name in list_doc:
                files = os.listdir(templatePathc3)
                for f in files:
                    if f.startswith(name):
                        shutil.copy(os.path.abspath(f), destC3)
                pbturns += 1
                pb['value']=(pbturns/pbmax)*100
                time.sleep(0.1)
                files1 = os.listdir(destC3)
        # else:
        #     response = messagebox.askyesno('Notice', 'You have more than 12 files selected, would you like to continue the the transfer?')
        #     if response == 1:
        #         os.chdir(templatePathc3)
        #         for name in list_doc:
        #             files = os.listdir(templatePathc3)
        #             for f in files:
        #                 if f.startswith(name):
        #                     shutil.copy(os.path.abspath(f), destC3)
        #         pbturns += 1
        #         pb['value']=(pbturns/pbmax)*100
        #         time.sleep(0.1)
        #         files1 = os.listdir(destC1)
        #     elif response ==0:
        #         return

    else:
        messagebox.showinfo("Error", 'Please select one of the options on the left.')
        Run.config(state=NORMAL) 
        return
    pb['value']=0
    Run.config(state=NORMAL) 
    if len(files1) < len(list_doc):
        if jig == 'C1':
            os.chdir(destC1)
            files = os.listdir(destC1)
            filesstriped = [i.strip('.txt') for i in files]
            notfound = [x for x in list_doc if x not in filesstriped]

        if jig == 'C2':
            os.chdir(destC2)
            files = os.listdir(destC2)
            filesstriped = [i.strip('.txt') for i in files]
            notfound = [x for x in list_doc if x not in filesstriped]

        if jig == 'C3':
            os.chdir(destC3)
            files = os.listdir(destC3)
            filesstriped = [i.strip('.txt') for i in files]
            notfound = [x for x in list_doc if x not in filesstriped]

        # messagebox.showinfo("Transfer Complete", 'A total of {0} out of {1} files were transfered'.format(len(files1), pbmax))
        messagebox.showinfo("Transfer Complete", 'A total of {0} out of {1} file(s) were transfered\nFollowing file(s) were not found:\n\n{2}'.format(len(files1), pbmax, ' \n'.join(str(e) for e in notfound)))
    elif len(files1) > len(list_doc):
        messagebox.showinfo("Notice", "A total of {0} files were transfered, this is greater than the {1} file(s) requested. Please check for duplicates and be aware of multiple items per order".format(len(files1), pbmax))
    else:
        messagebox.showinfo("Transfer Complete", 'A total of {0} out of {1} file(s) were transfered'.format(pbturns, pbmax))

def start_thread_play():
    global start_thread_macro
    start_thread_macro=threading.Thread(target=playMacro)
    start_thread_macro.start()

#Clear TextBox
def clear():
    Doc_entry.delete(1.0, END)
    pb['value']=0

    #--------------------------------------------

def getFolderPathC1():
    folder_selected = filedialog.askdirectory()
    C1path = folderPathC1.set(folder_selected)

def getFolderPathC2():
    folder_selected = filedialog.askdirectory()
    C2path = folderPathC2.set(folder_selected)

def getFolderPathC3():
    folder_selected = filedialog.askdirectory()
    C3path = folderPathC3.set(folder_selected)

    #------------------------------------------

def destFolderPathC1():
    folder_selected = filedialog.askdirectory()
    C1dest = DfolderPathC1.set(folder_selected)

def desFolderPathC2():
    folder_selected = filedialog.askdirectory()
    C2dest = DfolderPathC2.set(folder_selected)

def destFolderPathC3():
    folder_selected = filedialog.askdirectory()
    C3dest = DfolderPathC3.set(folder_selected)

#---------------------------------------------

def openSourceset():
    newwindow1 = Toplevel()
    newwindow1.attributes('-topmost', 1)
    # newwindow1.attributes('-topmost', False)
    newwindow1.after_idle(newwindow1.attributes,'-topmost',False)
    newwindow1.title('Select Paths')
    newwindow1.geometry('420x240+250+380')
    mainsource = Frame(newwindow1)
    mainsource.pack(pady=1, padx=4, fill='x', expand=True)

    Sourcepath = LabelFrame(mainsource, text = 'Source Path')
    Sourcepath.pack(fill='both', padx=2,pady=2, expand=True,)

    op2 = Frame(Sourcepath)
    op2.pack( fill='x', expand=True,padx=5, pady=(1,5))

    opSourcelab = Frame(op2)
    opSourcelab.pack(fill='x', side=LEFT)

    opSource1 = Frame(op2)
    opSource1.pack(fill='x', expand=True)

    opSource2 = Frame(op2)
    opSource2.pack(fill='x', expand=True)

    opSource3 = Frame(op2)
    opSource3.pack(fill='x', expand=True)

    c1source = ttk.Label(opSourcelab, text ='{}: '.format(opt1name.get()) ).pack(pady=3, anchor = tk.E)
    c1sourceEntry = ttk.Entry(opSource1, textvariable=folderPathC1, state=DISABLED).pack(side=LEFT,  fill='x', expand=True)
    c1source = ttk.Button(opSource1, text='Select Path', command=getFolderPathC1).pack(side=RIGHT)

    c2source = ttk.Label(opSourcelab, text ='{}: '.format(opt2name.get()) ).pack(pady=3, anchor = tk.E)
    c2sourceEntry = ttk.Entry(opSource2, textvariable=folderPathC2, state=DISABLED).pack(side=LEFT,  fill='x', expand=True)
    c2source = ttk.Button(opSource2, text='Select Path', command=getFolderPathC2).pack(side=RIGHT)

    c3source = ttk.Label(opSourcelab, text ='{}: '.format(opt3name.get()) ).pack(pady=3, anchor = tk.E)
    c3sourceEntry = ttk.Entry(opSource3, textvariable=folderPathC3, state=DISABLED).pack(side=LEFT, fill='x', expand=True)
    c3source = ttk.Button(opSource3, text='Select Path', command=getFolderPathC3).pack(side=RIGHT)

    destpath = LabelFrame(mainsource, text = 'Destination Path')
    destpath.pack(fill='both', padx=2,pady=2, expand=True,)

    op1 = Frame(destpath)
    op1.pack( fill='x', expand=True,padx=5, pady=(1,5))

    opDestlab = Frame(op1)
    opDestlab.pack(fill='x', side=LEFT)

    opDest1 = Frame(op1)
    opDest1.pack( fill='x', expand=True)

    opDest2 = Frame(op1)
    opDest2.pack( fill='x', expand=True)

    opDest3 = Frame(op1)
    opDest3.pack( fill='x', expand=True)

    c1destination = ttk.Label(opDestlab, text ='{}: '.format(opt1name.get())).pack(pady=3, anchor = tk.E)
    c1destinationEntry = ttk.Entry(opDest1, textvariable=DfolderPathC1, state=DISABLED).pack(side=LEFT, fill='x', expand=True)
    c1destination = ttk.Button(opDest1, text='Select Path', command=destFolderPathC1).pack(side=RIGHT)

    c2destination = ttk.Label(opDestlab, text ='{}: '.format(opt2name.get())).pack(pady=3, anchor = tk.E)
    c2destinationEntry = ttk.Entry(opDest2, textvariable=DfolderPathC2, state=DISABLED).pack(side=LEFT,fill='x', expand=True)
    c2destination = ttk.Button(opDest2, text='Select Path', command=desFolderPathC2).pack(side=RIGHT)

    c3destination = ttk.Label(opDestlab, text ='{}: '.format(opt3name.get())).pack(pady=3, anchor = tk.E)
    c3destinationEntry = ttk.Entry(opDest3, textvariable=DfolderPathC3, state=DISABLED).pack(side=LEFT,fill='x', expand=True)
    c3destination = ttk.Button(opDest3, text='Select Path', command=destFolderPathC3).pack(side=RIGHT)

    clearok = Frame(newwindow1)
    clearok.pack( fill='both', expand=True, padx=5,pady=(0,5))

    ok1 = ttk.Button(clearok, text='Ok', command= newwindow1.destroy).pack(padx=1, fill='y', side=RIGHT, expand=True)

# def openDestinationset():
#     newwindow2 = Toplevel()
#     newwindow2.attributes('-topmost', True)
#     newwindow2.title('Select Destination Paths')
#     newwindow2.geometry('400x135')
#     mainDestination = Frame(newwindow2)
#     mainDestination.pack(pady=1, padx=4, fill='x', expand=True)

#     Destcepath = ttk.Label(mainDestination, text='Destination Path').pack( fill='x', expand=True)

#     opDest1 = Frame(mainDestination)
#     opDest1.pack( fill='x', expand=True)

#     opDest2 = Frame(mainDestination)
#     opDest2.pack( fill='x', expand=True)

#     opDest3 = Frame(mainDestination)
#     opDest3.pack( fill='x', expand=True)

#     c1destination = ttk.Label(opDest1, text='C1:').pack(side=LEFT)
#     c1destinationEntry = ttk.Entry(opDest1, textvariable=DfolderPathC1, state=DISABLED).pack(side=LEFT, fill='x', expand=True)
#     c1destination = ttk.Button(opDest1, text='Set Path', command=destFolderPathC1).pack(side=RIGHT)

#     c2destination = ttk.Label(opDest2, text='C2:').pack(side=LEFT)
#     c2destinationEntry = ttk.Entry(opDest2, textvariable=DfolderPathC2, state=DISABLED).pack(side=LEFT,fill='x', expand=True)
#     c2destination = ttk.Button(opDest2, text='Set Path', command=desFolderPathC2).pack(side=RIGHT)
#     c3destination = ttk.Label(opDest3, text='C3:').pack(side=LEFT)
#     c3destinationEntry = ttk.Entry(opDest3, textvariable=DfolderPathC3, state=DISABLED).pack(side=LEFT,fill='x', expand=True)
#     c3destination = ttk.Button(opDest3, text='Set Path', command=destFolderPathC3).pack(side=RIGHT)

#     clearok = Frame(newwindow2)
#     clearok.pack( fill='both', expand=True, padx=1,pady=1, side=LEFT)

#     ok1 = ttk.Button(clearok, text='Ok', command= newwindow2.destroy).pack(padx=1, fill='y', side=RIGHT, expand=True)


def opensetopt():
    newwindow3 = Toplevel()
    newwindow3.attributes('-topmost', True)
    newwindow3.title('Select Source Paths')
    newwindow3.geometry('150x192+695+410')
    mainsource = Frame(newwindow3)
    mainsource.pack(pady=1, padx=4, fill='x', expand=True)


    setoptname = LabelFrame(mainsource, text = 'Set Name')
    setoptname.pack(fill='both', padx=2,pady=2, expand=True,)

    op2name = Frame(setoptname)
    op2name.pack( fill='x', expand=True,padx=5, pady=(1,5))

    opSourcelabname = Frame(op2name)
    opSourcelabname.pack(fill='x', side=LEFT)

    opSource1name = Frame(op2name)
    opSource1name.pack(fill='x', expand=True)

    optnamelab1 = ttk.Label(opSourcelabname, text='Name: ').pack(pady=3)
    optname1entry = ttk.Entry(opSource1name, textvariable=optname).pack(side=LEFT,  fill='x', expand=True) 

    setopt = LabelFrame(mainsource, text = 'Set Options')
    setopt.pack(fill='both', padx=2,pady=2, expand=True,)

    op2 = Frame(setopt)
    op2.pack( fill='x', expand=True,padx=5, pady=(1,5))

    opSourcelab = Frame(op2)
    opSourcelab.pack(fill='x', side=LEFT)

    opSource1 = Frame(op2)
    opSource1.pack(fill='x', expand=True)

    opSource2 = Frame(op2)
    opSource2.pack(fill='x', expand=True)

    opSource3 = Frame(op2)
    opSource3.pack(fill='x', expand=True)

    c1source = ttk.Label(opSourcelab, text='Option 1: ').pack(pady=3)
    c1sourceEntry = ttk.Entry(opSource1, textvariable=opt1name).pack(side=LEFT,  fill='x', expand=True)
    # c1source = ttk.Button(opSource1, text='Set').pack(side=RIGHT)

    c2source = ttk.Label(opSourcelab, text='Option 2: ').pack(pady=3)
    c2sourceEntry = ttk.Entry(opSource2, textvariable=opt2name).pack(side=LEFT,  fill='x', expand=True)
    # c2source = ttk.Button(opSource2, text='Set').pack(side=RIGHT)

    c3source = ttk.Label(opSourcelab, text='Option 3: ').pack(pady=3)
    c3sourceEntry = ttk.Entry(opSource3, textvariable=opt3name).pack(side=LEFT, fill='x', expand=True)
    # c3source = ttk.Button(opSource3, text='Set').pack(side=RIGHT)

    clearok = Frame(newwindow3)
    clearok.pack(fill='both',expand=True, padx=5,pady=(0,5))

    def nameupdate():
        RadioFrame.config(text=optname.get())
        r1.config(text=opt1name.get())
        r2.config(text=opt2name.get())
        r3.config(text=opt3name.get())
        newwindow3.destroy()
        return

    ok1 = ttk.Button(clearok, text='Set', command=nameupdate)
    ok1.pack( fill='x', side=LEFT, expand=True)
    newwindow3.attributes('-topmost', False)



def saveconfig():
    parser = ConfigParser()
    parser.read(r'info\config.ini')
    parser.set('source', 'c1', folderPathC1.get())
    parser.set('source', 'c2', folderPathC2.get())
    parser.set('source', 'c3', folderPathC3.get())

    parser.set('destination', 'c1', DfolderPathC1.get())
    parser.set('destination', 'c2', DfolderPathC2.get())
    parser.set('destination', 'c3', DfolderPathC3.get())

    parser.set('name', 'option1', opt1name.get())
    parser.set('name', 'option2', opt2name.get())
    parser.set('name', 'option3', opt3name.get())
    parser.set('name', 'option4', optname.get())
    with open(r'info\config.ini', 'w') as configfile:
        parser.write(configfile)

atexit.register(saveconfig)


def loadconfig():
    try:
        global folderPathC1,folderPathC2,folderPathC3,DfolderPathC1,DfolderPathC2,DfolderPathC3
        parser = ConfigParser()
        parser.read(r'info\config.ini')
        c1a = parser.get('source', 'c1')
        c2a = parser.get('source', 'c2')
        c3a = parser.get('source', 'c3')
        c1b = parser.get('destination', 'c1')
        c2b = parser.get('destination', 'c2')
        c3b = parser.get('destination', 'c3')
        c1c = parser.get('name', 'option1')
        c2c = parser.get('name', 'option2')
        c3c = parser.get('name', 'option3')
        folderPathC1.set(c1a)
        folderPathC2.set(c2a)
        folderPathC3.set(c3a)
        DfolderPathC1.set(c1b)
        DfolderPathC2.set(c2b)
        DfolderPathC3.set(c3b)
    except:
        messagebox.showwarning('Warning','Config file not found, press OK to load defualts')
        c1a = ''
        c2a = ''
        c3a = ''
        c1b = ''
        c2b = ''
        c3b = ''
        c1c = 'Option 1'
        c2c = 'Option 2'
        c3c = 'Option 3'
        folderPathC1.set(c1a)
        folderPathC2.set(c2a)
        folderPathC3.set(c3a)
        DfolderPathC1.set(c1b)
        DfolderPathC2.set(c2b)
        DfolderPathC3.set(c3b)


def Clear_paths():
    response = messagebox.askyesno('Warning','Are you sure you want to clear all directory paths?')
    if response == 1:
        global folderPathC1,folderPathC2,folderPathC3,DfolderPathC1,DfolderPathC2,DfolderPathC3
        folderPathC1 = tk.StringVar()
        folderPathC2 = tk.StringVar()
        folderPathC3 = tk.StringVar()
        DfolderPathC1 = tk.StringVar()
        DfolderPathC2 = tk.StringVar()
        DfolderPathC3 = tk.StringVar()
    else:
        pass

#---------------------------------------------------------------------------
root = Tk()
root.title('FileMover v{0}'.format(current))
root.geometry('+700+400')
style = ttk.Style()
style.theme_use('xpnative')
style.configure('TButton', justify='center')
tabs = ttk.Notebook(root)
MainTab = ttk.Frame(tabs)
OpTab = ttk.Frame(tabs)

DocN = tk.StringVar()
selected = tk.StringVar()
folderPathC1 = tk.StringVar()
folderPathC2 = tk.StringVar()
folderPathC3 = tk.StringVar()

DfolderPathC1 = tk.StringVar()
DfolderPathC2 = tk.StringVar()
DfolderPathC3 = tk.StringVar()

optname = tk.StringVar()
opt1name = tk.StringVar()
opt2name = tk.StringVar()
opt3name = tk.StringVar()

def startload():
    try:
        parser = ConfigParser()
        parser.read(r'info\config.ini')
        c1a = parser.get('source', 'c1')
        c2a = parser.get('source', 'c2')
        c3a = parser.get('source', 'c3')
        c1b = parser.get('destination', 'c1')
        c2b = parser.get('destination', 'c2')
        c3b = parser.get('destination', 'c3')
        c1c = parser.get('name', 'option1')
        c2c = parser.get('name', 'option2')
        c3c = parser.get('name', 'option3')
        c4c = parser.get('name', 'option4')

        folderPathC1.set(c1a)
        folderPathC2.set(c2a)
        folderPathC3.set(c3a)
        DfolderPathC1.set(c1b)
        DfolderPathC2.set(c2b)
        DfolderPathC3.set(c3b)

        opt1name.set(c1c)
        opt2name.set(c2c)
        opt3name.set(c3c)
        optname.set(c4c)
    except:
        messagebox.showwarning('Warning','Config file not found, press OK to load defualts')
        c1a = ''
        c2a = ''
        c3a = ''
        c1b = ''
        c2b = ''
        c3b = ''
        c1c = 'Option 1'
        c2c = 'Option 2'
        c3c = 'Option 3'
        c4c = 'Options'
        folderPathC1.set(c1a)
        folderPathC2.set(c2a)
        folderPathC3.set(c3a)
        DfolderPathC1.set(c1b)
        DfolderPathC2.set(c2b)
        DfolderPathC3.set(c3b)

        opt1name.set(c1c)
        opt2name.set(c2c)
        opt3name.set(c3c)
        optname.set(c4c)
        if not os.path.exists('info'):
            os.makedirs('info')
            config_file = configparser.ConfigParser()
    
            config_file["source"]={
            "c1": "",
            "c2": "",
            "c3": "",
            }
            config_file["destination"]={
            "c1":"",
            "c2":"",
            "c3":""
            }
            config_file["name"]={
            "option1": "option 1",
            "option2": "option 2",
            "option3": "option 3",
            "option4": "Options",
            
            }
            with open(r"info\config.ini","w") as file_object:
                config_file.write(file_object)
            # time.sleep(1)
        else:
            config_file = configparser.ConfigParser()
    
            config_file["source"]={
            "c1": "",
            "c2": "",
            "c3": "",
            }
            config_file["destination"]={
            "c1":"",
            "c2":"",
            "c3":""
            }
            config_file["name"]={
            "option1": "option 1",
            "option2": "option 2",
            "option3": "option 3",
            "option4": "Options",
            
            }
            with open(r"info\config.ini","w") as file_object:
                config_file.write(file_object)
            # time.sleep(1)
        
startload()

#------------------------------------------------------------------------------
#Main
#Doc entry frame, run button. 
DocEnter = ttk.Frame(MainTab)
DocEnter.pack(fill='both', padx=2,pady=2, side=RIGHT, expand=True,)

#Doc entry field label
Doc_label = ttk.Label(DocEnter, text='Document #s:')
Doc_label.pack(fill='x', padx=1)

#Doc entry Textbox
Doc_entry = scrolledtext.ScrolledText(DocEnter, wrap = tk.WORD, width = 19, height = 5)
Doc_entry.pack(fill='both', expand=True)
Doc_entry.focus()

DocEnter1 = ttk.Frame(DocEnter)
DocEnter1.pack(fill='x', padx=0,pady=0)

#Clear button
clear_mb = ttk.Button(DocEnter1, text='Clear', command=clear)
clear_mb.pack(fill='x', side=LEFT, expand=True, pady=2)

#Run/Play
Run = ttk.Button(DocEnter1, text='Transfer', command=start_thread_play)
Run.pack(fill='x', side=RIGHT, expand=True, pady=2)

pb = ttk.Progressbar(DocEnter, orient='horizontal', mode='determinate')
pb.pack(fill='x', padx=1)

# ----------------------------

RadioFrame = LabelFrame(MainTab, text = optname.get())
RadioFrame.pack(fill='both', padx=2,pady=2, side=LEFT, expand=True,)

# jigType = ttk.Label(RadioFrame, text="Jig type")
# jigType.pack(padx=5)

r1 = ttk.Radiobutton(RadioFrame, text = opt1name.get(), value='C1', variable=selected)
r1.pack(fill='both', padx=5, pady=5)
r2 = ttk.Radiobutton(RadioFrame, text = opt2name.get(), value='C2', variable=selected)
r2.pack(fill='both', padx=5, pady=5)
r3 = ttk.Radiobutton(RadioFrame, text = opt3name.get(), value='C3', variable=selected)
r3.pack(fill='both', padx=5, pady=5)
set = ttk.Button(RadioFrame, text='Set Options', command=opensetopt).pack(fill='both', padx=5, pady=(12,5))

pathframe = Frame(OpTab)
pathframe.pack( fill='both', expand=True, padx=2,pady=2, side=LEFT)

saveframe = Frame(OpTab)
saveframe.pack( fill='both', expand=True, padx=2,pady=2, side=RIGHT)

SelectSourcebtn = ttk.Button(pathframe, text='Set\nSource/Destination\nPaths', command=openSourceset).pack(pady=1, padx=1,fill='both', expand=True, side=TOP)
# SelectDestinationbtn = ttk.Button(pathframe, text='Set Destination Paths', command=openDestinationset).pack(pady=1, padx=1,fill='both', expand=True, side=BOTTOM)


savebtn = ttk.Button(saveframe, text='Clear Paths', command=Clear_paths).pack(pady=1, padx=1,fill='both', expand=True,side=TOP)
loadbtn = ttk.Button(saveframe, text='Load Config', command=loadconfig).pack( pady=1, padx=1, fill='both', expand=True,side=BOTTOM)



#Tabs
tabs.add(MainTab, text = 'Main')
tabs.add(OpTab, text = 'Options')
tabs.pack(expand = 1, fill ="both")

#----------------
root.lift()
root.attributes('-topmost',1)
root.after_idle(root.attributes,'-topmost',False)
root.mainloop()
