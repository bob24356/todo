from tkinter import Tk, END, messagebox, filedialog, Scale, Label
from ttkbootstrap import Button, Text, Scrollbar, Treeview, Style
from warnings import filterwarnings
from datetime import datetime
from pygame.mixer import init
from pygame.mixer import music
filterwarnings('ignore')
value = ''
init()
window = Tk()
window.geometry('550x350')
window.title('待办')
window.attributes('-topmost', True)
window.resizable(False, False)
try:
    window.iconbitmap('favicon.ico')
except:
    pass

# 定义优先级颜色
PRIORITY_INFO = {
    '高等级': {'color': '#ffcccc', 'order': 3},  # 浅红色，最高优先级
    '中等级': {'color': '#ffffcc', 'order': 2},  # 浅黄色，中等优先级
    '低等级': {'color': '#ccffcc', 'order': 1},  # 浅绿色，最低优先级
}
isplay = False
ispaused = False
def open_file():
    # 打开文件对话框
    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=[
            ("文本文件", "*.txt")
        ]
    )

    if file_path:  # 用户选择了文件
        try:
            tasks = []
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for line in content.splitlines():
                    if line.strip():  # 过滤空行
                        # 解析行内容，格式应为"任务内容------优先级"
                        if '------' in line:
                            task_text, priority = line.split('------', 1)
                            tasks.append((task_text.strip(), priority.strip()))
                        else:
                            # 如果没有优先级信息，默认设为低等级
                            tasks.append((line.strip(), '低等级'))

            # 清空现有任务
            for item in treeview.get_children():
                treeview.delete(item)

            # 按优先级排序后添加
            sorted_tasks = sort_tasks_by_priority(tasks)
            for task_text, priority in sorted_tasks:
                add_task_to_treeview(task_text, priority)

        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")

def open_music():
    global music_load
    music_load = ""
    # 打开文件对话框
    file_path = filedialog.askopenfilename(
        title="选择音乐",
        filetypes=[
            ("mp3文件", "*.mp3")
        ]
    )

    if file_path:  # 用户选择了文件
        try:
            music_load = file_path
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")

def save_file():
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
            with open(file_path, 'w', encoding='utf-8') as file:
                # 按优先级排序后保存
                tasks = []
                for item in treeview.get_children():
                    task_text = treeview.item(item, 'values')[0]
                    priority = treeview.item(item, 'values')[1]
                    tasks.append((task_text, priority))

                sorted_tasks = sort_tasks_by_priority(tasks)
                for task_text, priority in sorted_tasks:
                    file.write(f"{task_text}------{priority}\n")

            messagebox.showinfo("成功", "文件保存成功！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败:\n{str(e)}")

def play_():
    global isplay, ispaused, music_load
    if ispaused:
        music.unpause()
        ispaused = False
        isplay = True
    else:
        try:
            music.load(music_load)
            music.play(loops=-1)
            ispaused = False
            isplay = True
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")

def stop_():
    global isplay, ispaused
    music.stop()
    ispaused = False
    isplay = False

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
    selected_items = treeview.selection()

    if not selected_items:
        messagebox.showinfo("提示", "请先选择项目")
        return

    # 询问确认
    if messagebox.askyesno("确认", f"确定要删除选中的 {len(selected_items)} 个项目吗？"):
        for item in selected_items:
            treeview.delete(item)

def sort_tasks_by_priority(tasks):
    """按优先级排序任务列表"""
    return sorted(tasks, key=lambda x: PRIORITY_INFO.get(x[1], {'order': 0})['order'], reverse=True)

def add_task_to_treeview(task_text, priority):
    """向Treeview中添加任务并设置颜色"""
    item_id = treeview.insert('', 'end', values=(task_text, priority))

    # 根据优先级设置行颜色
    color_info = PRIORITY_INFO.get(priority, {'color': '#ffffff'})
    color = color_info['color']
    treeview.tag_configure(priority, background=color)
    treeview.item(item_id, tags=(priority,))

def selected():
    global value
    task_text = task_create.get('1.0', END).strip()

    if not task_text:
        messagebox.showinfo("提示", "请先输入内容")
        return

    if value == '':
        value = '低等级'

    # 添加到Treeview
    add_task_to_treeview(task_text, value)
    task_create.delete('1.0', END)

    # 重新按优先级排序所有任务
    resort_tasks()

def resort_tasks():
    """重新按优先级排序Treeview中的所有任务"""
    # 获取所有任务
    tasks = []
    for item in treeview.get_children():
        task_text = treeview.item(item, 'values')[0]
        priority = treeview.item(item, 'values')[1]
        tasks.append((task_text, priority))

    # 清空Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # 按优先级排序后重新添加
    sorted_tasks = sort_tasks_by_priority(tasks)
    for task_text, priority in sorted_tasks:
        add_task_to_treeview(task_text, priority)

def volume(val):
    volume_ = float(val) / 100
    music.set_volume(volume_)

def sort_by_priority():
    """按优先级排序按钮"""
    resort_tasks()
    messagebox.showinfo("提示", "已按优先级排序")

def sort_by_task():
    """按任务名称排序按钮"""
    # 获取所有任务
    tasks = []
    for item in treeview.get_children():
        task_text = treeview.item(item, 'values')[0]
        priority = treeview.item(item, 'values')[1]
        tasks.append((task_text, priority))

    # 按任务名称排序
    sorted_tasks = sorted(tasks, key=lambda x: x[0])

    # 清空Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # 重新添加
    for task_text, priority in sorted_tasks:
        add_task_to_treeview(task_text, priority)

    messagebox.showinfo("提示", "已按任务名称排序")

# 创建Treeview（两列列表）
columns = ('任务', '优先级')
treeview = Treeview(window, columns=columns, show='headings', height=9, selectmode='extended')

# 设置列标题
treeview.heading('任务', text='任务内容')
treeview.heading('优先级', text='优先级')

# 设置列宽度
treeview.column('任务', width=250, anchor='w')
treeview.column('优先级', width=80, anchor='center')

# 创建滚动条
scrollbar = Scrollbar(window, bootstyle="round")

# 配置滚动条与Treeview的关联
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=treeview.yview)

# 创建其他控件
task_high = Button(window, text='高等级', padding=(10, 5), command=high)
task_mid = Button(window, text='中等级', padding=(10, 5), command=mid)
task_low = Button(window, text='低等级', padding=(10, 5), command=low)
open_ = Button(window, text='打开', padding=(20, 5), command=open_file, bootstyle='info')
save_ = Button(window, text='保存', padding=(20, 5), command=save_file, bootstyle='info')
task_create = Text(window, width=35, height=1)
task_created = Button(window, text='创建', padding=(15, 5), command=selected, bootstyle='success')
delete = Button(window, text='删除', padding=(15, 5), command=delete_selected, bootstyle='danger')
start = Button(window, text='开始', padding=(10, 2), command=play_)
pause = Button(window, text='暂停', padding=(10, 2), command=pause_)
stop = Button(window, text='停止', padding=(10, 2), command=stop_)
music_load_btn = Button(window, text='导入音乐', padding=(10, 2), command=open_music)
volume_scale = Scale(window, from_=0, to=100, orient='vertical', length=180, bg="#f0f0f0", command=volume)
volume_scale.set(70)  # 默认音量
l1 = Label(window, text='0%')
l2 = Label(window, text='100%')

# 添加排序按钮
sort_priority_btn = Button(window, text='按优先级排序', padding=(10, 2), command=sort_by_priority, bootstyle='warning')
sort_task_btn = Button(window, text='按名称排序', padding=(10, 2), command=sort_by_task, bootstyle='warning')

# 布局控件
music_load_btn.place(x=440, y=310)
volume_scale.place(x=470, y=10)
scrollbar.place(x=440, y=100, width=15, height=190)
treeview.place(x=10, y=100)
task_high.place(x=10, y=10)
task_mid.place(x=80, y=10)
task_low.place(x=150, y=10)
task_create.place(x=10, y=60)
task_created.place(x=270, y=60)
delete.place(x=220, y=10)
open_.place(x=370, y=10)
save_.place(x=370, y=60)
start.place(x=470, y=195)
pause.place(x=470, y=225)
stop.place(x=470, y=255)
l1.place(x=500, y=5)
l2.place(x=500, y=160)
sort_priority_btn.place(x=10, y=310)
sort_task_btn.place(x=120, y=310)
window.mainloop()
