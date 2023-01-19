import tkinter
from tkinter import*
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
from tkinter import font
from tkinter import colorchooser
import pyttsx3

#initialize Speech Engine
engine=pyttsx3.init()

root=Tk()
root.title("My Word Editor")
root.geometry("800x500+200+55")
root.resizable(0,0)


#Functions
def open_file():
    file=askopenfilename(initialdir="/Desktop",title="Open a File",filetypes=(("Text Files","*.txt"),("Python Files","*.py"),("CSV Files","*.csv")))
    text=open(file,"r")
    content=text.read()
    editor.delete("1.0",END)
    editor.insert("1.0",content)
    text.close()

    #change app_title
    root.title(f"My Cool Editor---->{os.path.basename(file)}")
            #changing the status bar name
    status_bar.config(text=f'Currently opened file---->{os.path.dirname(file)}')

def save_file():
    file=asksaveasfilename(initialdir="/Desktop",title="Open a File",filetypes=(("Text Files","*.txt"),("Python Files","*.py"),("CSV Files","*.csv"),),defaultextension="*.py")

    content=editor.get("1.0",END) # we would use editor instead of content
    with open(file,"w") as text:
        text.write(content)
"""
1.Create a font object and set the weight
2.Configure the edito tags for comparison with current tags 
3.Create or get the editor tag
4.Apply the formatting
"""

def bold_text():
    #Create Font
    bold_var=font.Font(editor,editor.cget("font")) #1
    bold_var.configure(weight="bold")
    #Configure Tag for comparison with current tag
    editor.tag_configure("bold",font=bold_var)
    #Define current tag
    current_tag=editor.tag_names("sel.first") # it should apply to the selected text
    
    if "bold" in current_tag:
        editor.tag_remove("bold","sel.first",'sel.last') # gets the index of the selected text and apply the formatting to it
    else:
        editor.tag_add("bold","sel.first","sel.last") # checking if the else is not bold, it should bolden it

def italic_text():
     #Create Font
    italic_var=font.Font(editor,editor.cget("font")) #1
    italic_var.configure(slant="italic")
    #Configure Tag for comparison with current tag
    editor.tag_configure("italic",font=italic_var)
    #Define current tag
    current_tag=editor.tag_names("sel.first") # it should apply to the selected text
    
    if "italic" in current_tag:
        editor.tag_remove("italic","sel.first",'sel.last') # gets the index of the selected text and apply the formatting to it
    else:
        editor.tag_add("italic","sel.first","sel.last") # checking if the else is not bold, it should bolden it

def underline_text():
    underline_var=font.Font(editor,editor.cget("font")) #1
    underline_var.configure(underline=True)
    #Configure Tag for comparison with current tag
    editor.tag_configure("underline",font=underline_var)
    #Define current tag
    current_tag=editor.tag_names("sel.first") # it should apply to the selected text
    
    if "underline" in current_tag:
        editor.tag_remove("underline","sel.first",'sel.last') # gets the index of the selected text and apply the formatting to it
    else:
        editor.tag_add("underline","sel.first","sel.last") # checking if the else is not bold, it should bolden it

def change_color():
    color=colorchooser.askcolor()[1]  # the index one allows us to chose the "#hex" format
    
    if color:
            #Create Font
        color_var=font.Font(editor,editor.cget("font")) #1
        #Configure Tag for comparison with current tag
        editor.tag_configure("colored",font=color_var,foreground=color)
        #Define current tag
        current_tag=editor.tag_names("sel.first") # it should apply to the selected text
    
        if "colored" in current_tag:
            editor.tag_remove("colored","sel.first","sel.last")    
        else:
            editor.tag_add("colored","sel.first","sel.last")

def change_all_text():
    color=colorchooser.askcolor()[1]

    if color:
        #Configure  the editor
        editor.config(foreground=color)

def change_bg():
    color=colorchooser.askcolor()[1]

    if color:
        #Configure  the editor
        editor.config(background=color)


def copy_text():
    global selected_text
    if editor.selection_get():
        selected_text=editor.selection_get()
        #Clear the clipboard and apend selected text to the clipboard
        root.clipboard_clear()
        root.clipboard_append(selected_text)

def cut_text():
    global selected_text
    if editor.selection_get():
        selected_text=editor.selection_get()
        editor.delete("sel.first","sel.last") #removing it from the editor
        #Clear the clipboard and apend selected text to the clipboard
        root.clipboard_clear()
        root.clipboard_append(selected_text)

def paste_text():
    global selected_text
    #since we've already selected and appended on the clipboard
    if selected_text:
        cursor_pos=editor.index(INSERT) # trying to put where ever the cursor is in insert mood
        editor.insert(cursor_pos,selected_text)# trying to insert at the selected text

def select_all():
    editor.tag_add("sel","1.0","end")
    editor.tag_config("sel",background="blue",foreground="green")

def undo_action():
    editor.edit_undo()

def redo_action():
    editor.edit_redo() 

def clear_all():
    editor.delete(1.0,END)   

def read_sel():
    #get the words
    words=editor.selection_get()
    #Define speech speed("rate",)
    rate=engine.getProperty("rate")
    
    #Define speech volume
    volume=engine.setProperty("volume",1.0)
    
    #say the words
    engine.say(words)
    engine.runAndWait()

def read_all():
    words=editor.get("1.0",END)
    rate=engine.getProperty("rate")
    
    #Define speech volume
    volume=engine.setProperty("volume",1.0)
    #say the words
    engine.say(words)
    engine.runAndWait()

def read_text_female():
    #get the words
    words=editor.selection_get()
    #Define speech speed(Rate)
    rate=engine.getProperty("rate")
    
    #Define speech volume
    volume=engine.setProperty("volume",1.0)
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[1].id)
    #say the words
    engine.say(words)
    engine.runAndWait()

def read_all_female():
    #get the words
    words=editor.get("1.0",END)
    #Define speech speed(Rate)
    rate=engine.getProperty("rate")
    #Define speech volume
    volume=engine.setProperty("volume",1.0)
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[1].id)
    #say the words
    engine.say(words)
    engine.runAndWait()

#UI
menubar=Menu(root)
root.config(menu=menubar)


filemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)

#filekeys
filemenu.add_command(label="Open",accelerator="Ctrl+O",command=open_file)
filemenu.add_command(label="Save",accelerator="Ctrl+S",command=save_file)
filemenu.add_separator() # the separator adds the line
filemenu.add_command(label="QUIT",accelerator="Ctrl+Q")

#editmenu
editmenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=copy_text)
editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=cut_text)
editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=paste_text)
editmenu.add_command(label="Select All",accelerator="Ctrl+A",command=select_all)
editmenu.add_command(label="Undo",accelerator="Ctrl+Z",command=undo_action)
editmenu.add_command(label="Redo",accelerator="Ctrl+Y",command=redo_action)
editmenu.add_command(label="Clear All",accelerator="Ctrl+V",command=clear_all)
editmenu.add_separator()
editmenu.add_command(label="QUIT",accelerator="Ctrl+Q")


#Color Menu
colormenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Color",menu=colormenu)
colormenu.add_command(label="Change Text Color",command=change_color)
colormenu.add_command(label="Change bg color",command=change_bg)
colormenu.add_cascade(label="Change all Text color",command=change_all_text)

#editmenu
read_menu=Menu(menubar,tearoff=False)
menubar.add_cascade(label="Read",menu=read_menu)
#read selected sub menu
read_sub_menu=Menu(read_menu,tearoff=False)
read_sub_menu.add_command(label="Male Voice",command=read_sel)
read_sub_menu.add_command(label="Female Voice",command=read_text_female)
#read selected menu
read_menu.add_cascade(label="Read Selected",menu=read_sub_menu)


#read selected all sub menu
read_sub_menu_all=Menu(read_menu,tearoff=False)
read_sub_menu_all.add_command(label="Male Voice",command=read_all)
read_sub_menu_all.add_command(label="Female Voice",comman=read_all_female)
#read selected menu
read_menu.add_cascade(label="Read All",menu=read_sub_menu_all)

frame=Frame(root,bg="#e2e2e2")
frame.pack(pady=2)

toolbar=Frame(frame,)
toolbar.pack(pady=5,padx=5,fill=X) # even if you dont have element in it it will still fill the X

editor_frame=Frame(frame)
editor_frame.pack(fill=BOTH)

#toolbar icons
open_btn=Button(toolbar,text="Open",fg="black",command=open_file)
open_btn.pack(side=LEFT)

save_btn=Button(toolbar,text="Save",fg="black",command=save_file)
save_btn.pack(side=LEFT)

bold_btn=Button(toolbar,text="B",fg="Black",font=("open sans",12,"bold"),command=bold_text)
bold_btn.pack(side=LEFT)

italic_btn=Button(toolbar,text="I",fg="Black",font=("open sans",12,"italic"),command=italic_text)
italic_btn.pack(side=LEFT)

underline_btn=Button(toolbar,text="U",fg="Black",font=("open sans",12,"underline"),command=underline_text)
underline_btn.pack(side=LEFT)

change_color_btn=Button(toolbar,text="Text Color",font=("open sans",12),fg="Black",command=change_color)
change_color_btn.pack(side=LEFT)

read_btn=Button(toolbar,text="Read_text",command=read_sel,fg="black")
read_btn.pack(side="left",padx=5)

read_menu=Button(toolbar,text="Read_All",command=read_all,fg="black")
read_menu.pack(side="left",padx=5)


#scrollbar
"""
1.create it 
2.configure
3.set widget commas
"""
vscroll=Scrollbar(editor_frame,)# the orientation is vertical by default
vscroll.pack(side=RIGHT,fill=Y)

#Editor-This refers to the text area
editor=Text(editor_frame,width=400,height=24,font=("open sans",15,"normal"),undo=True,yscrollcommand=vscroll.set)
editor.pack(fill=BOTH,expand=YES,padx=15)

vscroll.config(command=editor.yview)

#status bar
status_bar=Label(root,text="Status Bar",bg="light green",fg="black",anchor=W)
status_bar.pack(side=BOTTOM,fill=X,pady=3)


root.mainloop()