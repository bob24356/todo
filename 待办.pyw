from tkinter import Tk,END,Listbox,messagebox,filedialog,Scale
from ttkbootstrap import Button,Text,Scrollbar
from warnings import filterwarnings # 警告处理库
from datetime import datetime
from pygame.mixer import init
from pygame.mixer import music
filterwarnings('ignore')
value = ''
init()

isplay = False
ispaused = False
def open_file():
    global listbox
    # 打开文件对话框
    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=[
            ("文本文件", "*.txt")
        ]
    )

    if file_path:  # 用户选择了文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for i in content.splitlines():
                    if i.strip():  # 过滤空行
                        listbox.insert(END, i.strip())# 显示内容
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")


def save_file():
    global listbox
    # 打开保存文件对话框
    default_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
    file_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        title="保存文件",
        defaultextension=".txt",  # 默认扩展名
        filetypes=[
            ("文本文件", "*.txt")
        ]
    )

    if file_path:  # 用户选择了保存位置
        try:
            # 获取文本区域的内容
            n = listbox.size()
            as_ = []

            with open(file_path, 'a', encoding='utf-8') as file:
                for i in range(n):
                    content = listbox.get(i)
                    as_.append(content)
                for j in as_:
                    file.write(j)
                    file.write("\n")

        except Exception as e:
            messagebox.showerror("错误", f"保存失败:\n{str(e)}")

def play_():
    global isplay, ispaused
    if ispaused:
        music.unpause()
        ispaused = False
        isplay = True
    else:
        music.load('music.mp3')
        music.play(loops=-1)
        ispaused = False
        isplay = True

def pause_():
    global ispaused, isplay
    if isplay and not ispaused:
        music.pause()
        ispaused = True
        isplay = False
def high():
    global value
    value = '高等级'

def mid():
    global value
    value = '中等级'

def low():
    global value
    value = '低等级'

def delete_selected():
    selected_indices = listbox.curselection()

    if not selected_indices:
        messagebox.showinfo("提示", "请先选择项目")
        return

    for index in reversed(selected_indices):
        listbox.delete(index)

def selected():
    global task_create
    global value
    a = task_create.get('1.0', END)
    if a == '\n':
        messagebox.showinfo("提示", "请先输入内容")
        return
    if value == '':
        value = '低等级'
    a = a.strip()
    a += '------' + value
    listbox.insert(END, a)
    task_create.delete('1.0', END)

def volume(val):
    volume_ = float(val) / 100
    global volume_scale
    music.set_volume(volume_)

window = Tk()
window.geometry('470x290')  # 设置窗口大小
window.title('待办')  # 设置窗口标题
window.attributes('-topmost', True)
window.resizable(False, False)
window.iconbitmap('favicon.ico')
task_high = Button(window,text='高等级',padding=(10, 5),command=high)
task_mid = Button(window,text='中等级',padding=(10, 5),command=mid)
task_low = Button(window,text='低等级',padding=(10, 5),command=low)
open_ = Button(window,text='打开',padding=(20, 5),command=open_file,bootstyle='info')
save_ = Button(window,text='保存',padding=(20, 5),command=save_file,bootstyle='info')
task_create = Text(window,width=25,height=1)
task_created = Button(window,text='创建',padding=(15, 5),command=selected,bootstyle='success')
delete = Button(window,text='删除',padding=(15, 5),command=delete_selected,bootstyle='danger')
scrollbar = Scrollbar(window, bootstyle="round")
listbox = Listbox(window,yscrollcommand=scrollbar.set,width=40,height=9,font=("微软雅黑", 10),bg="#2b2b2b",fg="white",selectbackground="#0066cc",selectmode='multiple')
scrollbar.config(command=listbox.yview)
start = Button(window,text='开始',padding=(10, 2),command=play_)
stop = Button(window,text='暂停',padding=(10, 2),command=pause_)
volume_scale = Scale(window, from_=0, to=100, orient = 'vertical', length=200, bg="#f0f0f0",command=volume)
volume_scale.set(70)  # 默认音量


volume_scale.place(x=390, y=10)
scrollbar.place(x=360,y=100,width=15, height=190)
listbox.place(x=10,y=100)
task_high.place(x=10, y=10)
task_mid.place(x=80, y=10)
task_low.place(x=150, y=10)
task_create.place(x=10, y=60)
task_created.place(x=220, y=60)
delete.place(x=220, y=10)
open_.place(x=310, y=10)
save_.place(x=310, y=60)
start.place(x=390, y=220)
stop.place(x=390, y=260)


window.mainloop()