#!/usr/bin/env python3
import string
from keyword import kwlist
import tkinter
import tkinter.scrolledtext
from tkinter.filedialog import *
import os
import tkinter.messagebox
from tkinter.messagebox import *
import pyautogui
import getpass
save=False
root=tkinter.Tk()
bifs=dir(__builtins__)
kws=kwlist
Area=tkinter.scrolledtext.ScrolledText(root, font=('consolas', 16))
Area.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)
root.iconbitmap(os.path.join(r"icons\19536.ico"))


def sav_e():
    global filepath
    global save
    filepath=asksaveasfilename(defaultextension=".py")
    msg=Area.get(1.0, tkinter.END)
    fh=open(filepath, "w", encoding='utf-8', errors='ignore')
    fh.write(msg)
    fh.close()
    save=True


def op_en():
    global save
    global file_path
    file_path=askopenfilename(defaultextension=".py", filetypes=[('python files', '*.py'), ('All files', "*")])
    if file_path !='':
        Area.delete(1.0, tkinter.END)
        file=open(file_path, "r", encoding='utf-8', errors="ignore")
        Area.insert(1.0, file.read())
        file.close()
        save=True


def run():
    if not save:
        to_save=askokcancel("Save to run", "Do you want to save your file?File must be saved to run")
        if to_save:
            sav_e()
            run()
        else:
            pass
        pass
    else:
        try:
            com="python "+file_path
        except NameError:
            try:
                com = "python " +filepath
            except NameError:
                pass
        fout=os.popen(com)
        out=fout.read()
        run_root=tkinter.Tk()
        label=tkinter.Label(run_root, text=out)
        label.pack()
        button_con=tkinter.Button(run_root, text="confirm", command=run_root.destroy)
        button_con.pack()
        run_root.mainloop()


def copy():
    pyautogui.hotkey("ctrl", "c")


def paste():
    pyautogui.hotkey("ctrl", "v")


def new():
    Area.delete(1.0, tkinter.END)


def console():
    try:
        user=getpass.getuser()
        locate=r"C:/Users/" + user + "/AppData/Local/Programs/Python/Python39/python.exe"
        os.startfile(locate)
    except (FileNotFoundError, OSError):
        install_python=askokcancel("Install Python Interpreter", "Do you want to install python Interpreter?")
        if install_python:
            try:
                os.startfile("python-3.9.0-amd64.exe")
                pass
            except (FileNotFoundError, OSError):
                raise PythonInterpreterNotFoundError
        else:
            raise PythonInterpreterNotFoundError
        exit(0)

def button_set():
    menu = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu, tearoff=False)
    file_menu.add_command(label="new", command=new)
    file_menu.add_command(label="save", command=sav_e)
    file_menu.add_command(label="open", command=op_en)
    menu.add_cascade(label="file", menu=file_menu)
    menu.add_command(label="run", command=run)
    menu.add_command(label="copy", command=copy)
    menu.add_command(label="paste", command=paste)
    menu.add_command(label="console", command=console)
    root.config(menu=menu)
    button = tkinter.Button(root, text="save", command=sav_e)
    button.pack()
    button1 = tkinter.Button(root, text="open", command=op_en)
    button1.pack()
    button2 = tkinter.Button(root, text='run', command=run)
    button2.pack()
    button3 = tkinter.Button(root, text="copy", command=copy)
    button3.pack()
    button4 = tkinter.Button(root, text="paste", command=paste)
    button4.pack()


class PythonInterpreterNotFoundError(FileNotFoundError):
    pass


def process(key):
    line_num, col_num=map(int, Area.index(tkinter.INSERT).split('.'))
    if key.keycode==13:
        last_line_num=line_num-1
        last_line=Area.get(f"{last_line_num}.0", tkinter.INSERT).rstrip()
        num=len(last_line)-len(last_line.lstrip(''))
        if last_line.endswith(":") or (":" in last_line and last_line.split(':')[-1].strip().startswith("#")):
            num=num+4
        elif last_line.strip().startswith(('return', 'break', 'continue', 'pass', 'raise')):
            num=num-4
        Area.insert(tkinter.INSERT, "   "*num)
    elif key.keysym=="Backspace":
        cul_line=Area.get(f"{line_num}.0", f"{line_num}.{col_num}")
        num=len(cul_line)-len(cul_line.rstrip())
        num=min(3, num)
        if num>1:
            Area.delete(f'{col_num}.{col_num-num}', f'{col_num}.{col_num}')
            pass
        pass
    else:
        lines=Area.get('0.0', tkinter.END).rstrip('\n').splitlines(keepends=True)
        Area.delete('0.0', tkinter.END)
        for line in lines:
            flag1, flag2, flag3=False, False, False
            for index, ch in enumerate(line):
                if ch=="'" and not flag2:
                    flag3=not flag3
                    Area.insert(tkinter.INSERT, ch, 'string')
                elif ch=='"' and not flag3:
                    flag2=not flag2
                    Area.insert(tkinter.INSERT, ch, 'string')
                elif flag2 or flag3:
                    Area.insert(tkinter.INSERT, ch, 'string')
                else:
                    if ch not in string.ascii_letters:
                        if flag1:
                            flag1=False
                            word=line[start:index]
                            if word in bifs:
                                Area.insert(tkinter.INSERT, word, 'bif')
                            elif word in kws:
                                Area.insert(tkinter.INSERT, word, 'kw')
                            else:
                                Area.insert(tkinter.INSERT, word)
                                pass
                            pass
                        if ch=="#":
                            Area.insert(tkinter.INSERT, line[index:], 'comment')
                            break
                        else:
                            Area.insert(tkinter.INSERT, ch)
                            pass
                        pass
                    else:
                        if not flag1:
                            flag1=True
                            start=index
                            pass
                        pass
                    pass
                pass
            if flag1:
                flag1=False
                word=line[start:]
                if word in bifs:
                    Area.insert(tkinter.INSERT, word, 'bif')
                elif word in kws:
                    Area.insert(tkinter.INSERT, word, 'kws')
                else:
                    Area.insert(tkinter.INSERT, word)
                    pass
                pass
            Area.mark_set('index', f"{line_num}.{col_num}")
        pass
    pass


def paint():
    Area.bind('<KeyRelease>', process)
    Area.tag_config('bif', foreground="purple")
    Area.tag_config('kw', foreground="orange")
    Area.tag_config('comment', foreground="red")
    Area.tag_config('string', foreground="green")
    root.mainloop()


def main():
    button_set()
    paint()


if __name__ == '__main__':
    main()