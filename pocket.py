from PySide6.QtWidgets import (QLabel, QTreeWidget,
                               QGridLayout, QPushButton,
                               QLineEdit, QMessageBox, QTreeWidgetItem,
                               QMenu, QDialog, QRadioButton, QFileDialog,
                               QSlider, QMainWindow, QWidget, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from pygame.mixer import init
from pygame.mixer import music
import json
from os import makedirs, path
#import model


class ToDo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status = None
        self.PRIORITY_INFO = {
            'high': '#ffcccc',
            'mid': '#ffffcc',
            'low': '#ccffcc'
        }

        self.setWindowTitle('待办')
        self.setGeometry(300, 300, 600, 371)
        self.mainGrid = QGridLayout()
        self.tGrid = QGridLayout()
        self.bGrid = QGridLayout()

        self.listWindow = QTreeWidget()
        self.listWindow.setColumnCount(2)
        self.listWindow.setHeaderLabels(['名称', '优先级'])
        self.listWindow.setColumnWidth(0, 350)
        self.listWindow.setColumnWidth(1, 80)
        self.listWindow.setSelectionMode(QTreeWidget.MultiSelection)
        self.listWindow.setRootIsDecorated(False)

        self.label = QLabel('待办事项')
        self.label.setAlignment(Qt.AlignCenter)

        self.addPButton = QPushButton('添加')
        self.addPButton.clicked.connect(self.add_item)
        self.deletePButton = QPushButton('删除')
        self.deletePButton.clicked.connect(self.remove_item)

        self.startmPButton = QPushButton('开始')
        self.startmPButton.clicked.connect(self.startmusic)
        self.pausemPButton = QPushButton('暂停')
        self.pausemPButton.clicked.connect(self.pausemusic)
        self.stopmPButton = QPushButton('停止')
        self.stopmPButton.clicked.connect(self.stopmusic)
        
        self.slider = QSlider(Qt.Vertical,self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(10)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.on_value_changed)

        self.isplay = False
        self.ispaused = False
        init()
        self.music_load = ""

        central_widget = QWidget()
        central_widget.setLayout(self.mainGrid)
        self.setCentralWidget(central_widget)

        self.menuBar().clear()
        fileMenu = QMenu('文件', self)
        self.menuBar().addMenu(fileMenu)
        musicMenu = QMenu('音乐', self)
        self.menuBar().addMenu(musicMenu)
        helpMenu = QMenu('帮助', self)
        self.menuBar().addMenu(helpMenu)
        open_file = QAction('打开', self)
        save_file = QAction('保存', self)
        upload_m = QAction('导入音乐', self)
        showhelp = QAction('帮助', self)
        open_file.triggered.connect(self.open_everywhere)
        save_file.triggered.connect(self.save_everywhere)
        upload_m.triggered.connect(self.openmusic)
        showhelp.triggered.connect(self.show_help)
        fileMenu.addAction(open_file)
        fileMenu.addAction(save_file)
        musicMenu.addAction(upload_m)
        helpMenu.addAction(showhelp)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setStyleSheet("color: #d6d6d6")
        self.build()
        self.open_()
        self.create_menu()
    #define variables

    def build(self):
        self.mainGrid.addLayout(self.tGrid, 1, 0)
        self.mainGrid.addLayout(self.bGrid, 1, 1)
        self.tGrid.addWidget(self.label, 0, 0)
        self.tGrid.addWidget(self.listWindow, 2, 0)
        self.bGrid.addWidget(self.addPButton, 0, 0)
        self.bGrid.addWidget(self.deletePButton, 1, 0)
        self.bGrid.addWidget(self.line, 2, 0)
        self.bGrid.addWidget(self.slider,4,0)
        self.bGrid.addWidget(self.startmPButton,5,0)
        self.bGrid.addWidget(self.pausemPButton,6,0)
        self.bGrid.addWidget(self.stopmPButton,7,0)
    #build variable

    def add_item(self):
        a = startDialog()
        if a.exec() == QDialog.Accepted:
            b = a.save()
            item = QTreeWidgetItem(self.listWindow)
            if b[1] == '高等级':
                self.status = 'high'
            elif b[1] == '中等级':
                self.status = 'mid'
            elif b[1] == '低等级':
                self.status = 'low'
            item.setBackground(0, QColor(self.PRIORITY_INFO[self.status]))
            item.setBackground(1, QColor(self.PRIORITY_INFO[self.status]))
            item.setText(0, b[0])
            item.setText(1, b[1])
            self.listWindow.scrollToItem(item)
            self.sorted_()
    #add items

    def remove_item(self):
        if self.listWindow.selectedItems():
            a = QMessageBox.question(
                None,
                "操作中",
                "是否删除选中项目"
            )
            if a:
                for item in self.listWindow.selectedItems():
                    index = self.listWindow.indexOfTopLevelItem(item)
                    self.listWindow.takeTopLevelItem(index)
        else:
            QMessageBox.information(
                None,
                "操作失败",
                "未选中项目"
            )
    #remove items

    def save_model(self, filename):
        tasks = {}
        for i in range(self.listWindow.topLevelItemCount()):
            item = self.listWindow.topLevelItem(i)
            name = item.text(0)
            level = item.text(1)
            task_num = f'task{i + 1}'
            tasks[task_num] = {'name': name, 'level': level}
        if filename:
            makedirs(path.dirname(filename), exist_ok=True)
            with open(filename, 'w+', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False)

    def open_model(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            self.listWindow.clear()
            values_list = [value for value in tasks.values()]
            for value in values_list:
                name = value['name']
                level = value['level']
                if  level == '高等级':
                    status = 'high'
                elif level == '中等级':
                    status = 'mid'
                elif level == '低等级':
                    status = 'low'
                else:
                    status = 'mid'
                item = QTreeWidgetItem(self.listWindow)
                item.setBackground(0, QColor(self.PRIORITY_INFO[status]))
                item.setBackground(1, QColor(self.PRIORITY_INFO[status]))
                item.setText(0, name)
                item.setText(1, level)
                self.listWindow.scrollToItem(item)
        except FileNotFoundError:
            pass
    #open or save
    
    def save(self):
        filename = 'tasks/task.json'
        self.save_model(filename)
    #save backup        

    def save_everywhere(self):
        filename, _ = QFileDialog.getSaveFileName(self, '保存文件', '', "JSON文件 (*.json)")
        self.save_model(filename)
    #custom save


    def open_everywhere(self):
        filename, _ = QFileDialog.getOpenFileName(self, '打开文件', '', "JSON文件 (*.json)")
        if filename:
            self.open_model(filename)
    #custom open
    
    def open_(self):
        self.open_model('tasks/task.json')
    #open backup

    def sorted_(self):
        tasks = []
        priority_order = {"高等级": 3, "中等级": 2, "低等级": 1}
        for i in range(self.listWindow.topLevelItemCount()):
            item = self.listWindow.topLevelItem(i)
            name = item.text(0)
            level = item.text(1)
            if level not in priority_order:
                level = "中等级"
            tasks.append({'name': name, 'level': level})
        tasks.sort(key=lambda x: priority_order[x['level']], reverse=True)
        self.listWindow.clear()
        for task in tasks:
            name = task['name']
            level = task['level']
            if level == '高等级':
                status = 'high'
            elif level == '中等级':
                status = 'mid'
            elif level == '低等级':
                status = 'low'
            else:
                status = 'mid'
            item = QTreeWidgetItem(self.listWindow)
            item.setBackground(0, QColor(self.PRIORITY_INFO[status]))
            item.setBackground(1, QColor(self.PRIORITY_INFO[status]))
            item.setText(0, name)
            item.setText(1, level)
            self.listWindow.scrollToItem(item)
    #sort

    def create_menu(self):
        self.listWindow.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWindow.customContextMenuRequested.connect(lambda pos: self.show_menu(self.listWindow, pos))
    #create menus

    def show_menu(self, widget, position):
        item = widget.itemAt(position)
        if item:
            menu = QMenu()
            a = QAction(f"编辑{item.text(0)}")
            menu.addAction(a)
            a.triggered.connect(lambda checked, i=item: self.open_edit(i))
            menu.exec(widget.viewport().mapToGlobal(position))
    #show menus

    def open_edit(self,item):
        a = editDialog(item.text(0), item.text(1))
        if a.exec() == QDialog.Accepted:
            b = a.save()
            item.setText(0, b[0])
            item.setText(1, b[1])
            self.sorted_()
    #edit

    def show_help(self):
        QMessageBox.information(
            None,
            '帮助',
            """1. 添加待办事项：输入任务名称并选择优先级后添加，不同优先级以不同颜色区
分。
2. 删除任务：支持单选或多选删除任务。
3. 优先级管理：提供按钮快速设置任务优先级，并在添加时生效。
4. 任务排序：添加或编辑任务后自动按优先级从高到低排序。
5. 右键菜单编辑：右键点击任务可进行重命名和修改优先级。
6. 数据持久化：
    - 自动保存任务到本地 “tasks.json” 文件。
    - 支持手动导出/导入 JSON 文件到任意位置。
7. 界面特点：
    - 使用网格布局，左侧显示任务列表，右侧为操作按钮。
    - 状态栏显示当前选择的优先级。
    - 支持窗口关闭时自动保存。"""
        )
    #show help
    
    def openmusic(self):
        filename, _ = QFileDialog.getOpenFileName(self, '打开音乐', '', "mp3文件 (*.mp3)")
        if filename:
            try:
                self.music_load = filename
            except Exception as e:
                QMessageBox.critical(self,"错误",f'无法导入音乐\n{e}',QMessageBox.StandardButton.Close)
    #import music

    def startmusic(self):
        if self.ispaused:
            music.unpause()
            self.ispaused = False
            self.isplay = True
        else:
            try:
                music.load(self.music_load)
                music.play(loops=-1)
                self.ispaused = False
                self.isplay = True
            except Exception as e:
                QMessageBox.critical(self,"错误",f'无法打开音乐\n{e}',QMessageBox.StandardButton.Close)
    #play
    
    def stopmusic(self):
        music.stop()
        self.ispaused = False
        self.isplay = False
    #close
    
    def pausemusic(self):
        if self.isplay and not self.ispaused:
            music.pause()
            self.ispaused = True
            self.isplay = False
    #pause
    
    def on_value_changed(self,value):
        volume_ = float(value) / 100
        music.set_volume(volume_)
    #change volume

    def closeEvent(self, event):
        self.save()
    #save backup

class editDialog(QDialog):
    def __init__(self, item_name, item_level):
        super().__init__()
        self.setWindowTitle(f'编辑{item_name}')
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.f_gird = QGridLayout()
        self.s_gird = QGridLayout()
        self.t_gird = QGridLayout()
        self.text = QLineEdit(item_name)
        self.label = QLabel('重命名')
        self.radio1 = QRadioButton("高等级")
        self.radio1.clicked.connect(lambda: self.choose("高等级"))
        self.radio2 = QRadioButton("中等级")
        self.radio2.clicked.connect(lambda: self.choose("中等级"))
        self.radio3 = QRadioButton("低等级")
        self.radio3.clicked.connect(lambda: self.choose("低等级"))
        self.turePButton = QPushButton('确定')
        self.turePButton.clicked.connect(self.accept)
        self.falsePButton = QPushButton('取消')
        self.falsePButton.clicked.connect(self.reject)
        self.level = item_level
        if item_level == "高等级":
            self.radio1.setChecked(True)
        elif item_level == "中等级":
            self.radio2.setChecked(True)
        else:
            self.radio3.setChecked(True)
        self.build()
    #define variable
    
    def build(self):
        self.mainLayout.addLayout(self.f_gird, 0, 0)
        self.mainLayout.addLayout(self.s_gird, 1, 0)
        self.mainLayout.addLayout(self.t_gird, 2, 0)
        self.f_gird.addWidget(self.label, 0, 0)
        self.f_gird.addWidget(self.text, 1, 0)
        self.s_gird.addWidget(self.radio1, 0, 0)
        self.s_gird.addWidget(self.radio2, 0, 1)
        self.s_gird.addWidget(self.radio3, 0, 2)
        self.t_gird.addWidget(self.turePButton, 0, 0)
        self.t_gird.addWidget(self.falsePButton, 0, 1)
    #build variable

    def choose(self, name):
        self.level = name
    #choose level

    def save(self):
        a = self.text.text()
        level = self.level
        b = [a, level]
        return b
    #save

class startDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'创建任务')
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.f_gird = QGridLayout()
        self.s_gird = QGridLayout()
        self.t_gird = QGridLayout()
        self.text = QLineEdit()
        self.label = QLabel('名称')
        self.radio1 = QRadioButton("高等级")
        self.radio1.clicked.connect(lambda: self.choose("高等级"))
        self.radio2 = QRadioButton("中等级")
        self.radio2.clicked.connect(lambda: self.choose("中等级"))
        self.radio3 = QRadioButton("低等级")
        self.radio3.clicked.connect(lambda: self.choose("低等级"))
        self.turePButton = QPushButton('确定')
        self.turePButton.clicked.connect(self.accept)
        self.falsePButton = QPushButton('取消')
        self.falsePButton.clicked.connect(self.reject)
        self.level = "中等级"
        if self.level == "高等级":
            self.radio1.setChecked(True)
        elif self.level == "中等级":
            self.radio2.setChecked(True)
        else:
            self.radio3.setChecked(True)
        self.build()
        # define variable

    def build(self):
        self.mainLayout.addLayout(self.f_gird, 0, 0)
        self.mainLayout.addLayout(self.s_gird, 1, 0)
        self.mainLayout.addLayout(self.t_gird, 2, 0)
        self.f_gird.addWidget(self.label, 0, 0)
        self.f_gird.addWidget(self.text, 1, 0)
        self.s_gird.addWidget(self.radio1, 0, 0)
        self.s_gird.addWidget(self.radio2, 0, 1)
        self.s_gird.addWidget(self.radio3, 0, 2)
        self.t_gird.addWidget(self.turePButton, 0, 0)
        self.t_gird.addWidget(self.falsePButton, 0, 1)
        # build variable

    def choose(self, name):
        self.level = name
        # choose level

    def save(self):
        a = self.text.text()
        level = self.level
        b = [a, level]
        return b
    # save