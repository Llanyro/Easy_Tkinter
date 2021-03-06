from io import BytesIO
from tkinter import TOP, Button, Tk, E, W, N, S, messagebox, Menu, Scrollbar, Text, RIGHT, Y, LEFT, END, DISABLED, \
    NORMAL, Entry, Checkbutton, IntVar, PhotoImage, Label, VERTICAL, HORIZONTAL, Listbox
from tkinter.ttk import Notebook, Frame, Combobox, Progressbar
from PIL import ImageTk, Image
from tkinter import messagebox


class GeneralVentana:
    __name: str
    __object_list: list
    __ventana: Tk
    __menubar = None
    __dict_keys: list = ("type", "item")

    # region Funciones
    def __init__(self, titulo: str):
        self.__name = titulo
        self.__object_list = []
        self.__ventana = Tk()
        self.__ventana.title(titulo)
        self.__ventana.protocol("WM_DELETE_WINDOW", self.closeWindow)

    def start(self):
        self.__ventana.mainloop()

    def closeWindow(self):
        if messagebox.askokcancel("Salir", "Quieres salir?"):
            print("Guardando datos...")
            self.__ventana.destroy()

    def addItem(self, item):
        if type(item) == GeneralNotebook or issubclass(item.__class__, GeneralNotebook):
            self.__object_list.append({self.__dict_keys[0]: "notebook", self.__dict_keys[1]: item})
        elif type(item) == GeneralDivTab or issubclass(item.__class__, GeneralDivTab):
            self.__object_list.append({self.__dict_keys[0]: "div", self.__dict_keys[1]: item})
        else:
            print(item.__class__, "No añadido")

    def get(self, id: str):
        item = None
        for i in self.__object_list:
            if i[self.__dict_keys[1]].name == id:
                item = i[self.__dict_keys[1]]
                break
        return item

    @property
    def nucleo(self) -> Tk:
        return self.__ventana

    def setMenuBar(self, menu):
        if type(menu) == GeneralMenuBar:
            self.__menubar = menu
    # endregion


# region Rama Tabs
class GeneralNotebook:
    __parent = None
    __name: str
    __tab_list: list
    __notebook: Notebook

    # region Funciones
    def __init__(self, name: str, parent, row: int, column: int):
        if type(parent) != GeneralDivTab and issubclass(parent.__class__, GeneralDivTab) is not True and \
                type(parent) != GeneralVentana and issubclass(parent.__class__, GeneralVentana) is not True:
            raise Exception
        self.__parent = parent
        self.__name = name
        self.__tab_list = []
        self.__parent.addItem(self)
        self.__notebook = Notebook(parent.nucleo)
        self.__notebook.grid(row=row, column=column, sticky=E+W+N+S)
        self.__parent.nucleo.bind("<Configure>", self.conf)

    def conf(self, event):
        # print(event)
        alto = self.__parent.nucleo.winfo_height()
        largo = self.__parent.nucleo.winfo_width()
        # self.__notebook.config(height=alto, width=int((largo*8)/10))

    def addItem(self, tab):
        if type(tab) == GeneralTab or issubclass(tab.__class__, GeneralTab):
            self.__tab_list.append(tab)
        else:
            print(tab.__class__, "No añadido")

    def get(self, id: str):
        item = None
        for i in self.__tab_list:
            if i.name == id:
                item = i
                break
        return item

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Notebook:
        return self.__notebook

    @property
    def parent(self) -> any:
        return self.__parent

    # endregion


class GeneralTab:
    __parent: GeneralNotebook
    __name: str
    __div_list: list
    __tab: Frame
    __dict_keys: list = ("type", "item")

    # region Funciones
    def __init__(self, name: str, parent: GeneralNotebook):
        self.__parent = parent
        self.__name = name
        self.__div_list = []
        self.__parent.addItem(self)
        self.__tab = Frame(parent.nucleo)
        self.__parent.nucleo.add(self.__tab, text=self.__name, compound=TOP, sticky=N+S+E+W)

    def addItem(self, item):
        if type(item) == GeneralDivTab or issubclass(item.__class__, GeneralDivTab):
            self.__div_list.append(item)
        else:
            print(item.__class__, "No añadido")

    def get(self, id: str):
        item = None
        for i in self.__div_list:
            if i.name == id:
                item = i
                break
        return item

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Frame:
        return self.__tab

    @property
    def parent(self) -> GeneralNotebook:
        return self.__parent
    # endregion


class GeneralDivTab:
    __parent = None
    __name: str
    __row: int
    __col: int
    __object_list: list
    __div: Frame
    __dict_keys: list = ("type", "item")

    # region Funciones
    def __init__(self, name: str, parent, row: int = 0, col: int = 0, columnspan: int = 1, rowspan: int = 1):
        if type(parent) != GeneralTab and issubclass(parent.__class__, GeneralTab) is not True and \
                type(parent) != GeneralVentana and issubclass(parent.__class__, GeneralVentana) is not True:
            raise Exception

        self.__parent = parent
        self.__name = name
        self.__row = row
        self.__col = col
        self.__object_list = []
        self.__parent.addItem(self)
        self.__div = Frame(parent.nucleo)
        self.__div.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    def get(self, id: str):
        item = None
        for i in self.__object_list:
            if i[self.__dict_keys[1]].name == id:
                item = i[self.__dict_keys[1]]
                break
        return item

    def addItem(self, item) -> bool:
        result = True
        if type(item) == GeneralButton or issubclass(item.__class__, GeneralButton):
            self.__object_list.append({self.__dict_keys[0]: "button", self.__dict_keys[1]: item})
        elif type(item) == GeneralTextAreaScrollTab or issubclass(item.__class__, GeneralTextAreaScrollTab):
            self.__object_list.append({self.__dict_keys[0]: "text", self.__dict_keys[1]: item})
        elif type(item) == GeneralEntradaTexto or issubclass(item.__class__, GeneralEntradaTexto):
            self.__object_list.append({self.__dict_keys[0]: "text_insert", self.__dict_keys[1]: item})
        elif type(item) == GeneralCombox or issubclass(item.__class__, GeneralCombox):
            self.__object_list.append({self.__dict_keys[0]: "box", self.__dict_keys[1]: item})
        elif type(item) == GeneralCheckBox or issubclass(item.__class__, GeneralCheckBox):
            self.__object_list.append({self.__dict_keys[0]: "check_box", self.__dict_keys[1]: item})
        elif type(item) == GeneralNotebook or issubclass(item.__class__, GeneralNotebook):
            self.__object_list.append({self.__dict_keys[0]: "notebook", self.__dict_keys[1]: item})
        elif type(item) == GeneralLabel or issubclass(item.__class__, GeneralLabel):
            self.__object_list.append({self.__dict_keys[0]: "label", self.__dict_keys[1]: item})
        elif type(item) == GeneralPhoto or issubclass(item.__class__, GeneralPhoto):
            self.__object_list.append({self.__dict_keys[0]: "photo", self.__dict_keys[1]: item})
        elif type(item) == GeneralProgressBar or issubclass(item.__class__, GeneralProgressBar):
            self.__object_list.append({self.__dict_keys[0]: "progressbar", self.__dict_keys[1]: item})
        elif type(item) == GeneralListBox or issubclass(item.__class__, GeneralListBox):
            self.__object_list.append({self.__dict_keys[0]: "listbox", self.__dict_keys[1]: item})
        else:
            print(item.__class__)
            result = False
        return result

    def deleteItem(self, id: str) -> bool:
        result = False
        # Search Item
        for i in self.__object_list:
            if i[self.__dict_keys[1]].name == id:
                # Delete item
                del i
                result = True
                break
        return result

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Frame:
        return self.__div

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col

    @row.setter
    def row(self, value: int):
        self.__row = value

    @col.setter
    def col(self, value: int):
        self.__col = value

    @property
    def parent(self):
        return self.__parent

    # endregion


class GeneralTextAreaScrollTab:
    __parent: GeneralDivTab
    __name: str
    __text: Text = None
    __scroll: Scrollbar = None

    # region Funciones
    # def __init__(self, name: str, parent: GeneralDivTab, fill=Y, height=4, width=50):
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, columnspan: int = 1, rowspan: int = 1):
        self.__name = name
        self.__parent = parent
        self.__scroll = Scrollbar(self.__parent.nucleo)
        self.__text = Text(self.__parent.nucleo)

        # self.__scroll.pack(side=RIGHT, fill=fill)
        # self.__text.pack(side=LEFT, fill=fill)
        # self.__text.rowconfigure(self.__parent.nucleo, 0, weight=1)
        # self.__text.columnconfigure(self.__parent.nucleo, 0, weight=1)

        self.__text.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)
        self.__scroll.grid(row=row, column=col + columnspan + 1, rowspan=rowspan, sticky=N+S)

        self.__scroll.config(command=self.__text.yview)
        self.__text.config(yscrollcommand=self.__scroll.set)

        self.__parent.addItem(self)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    def appendText(self, contenido: str, readonly: bool = False):
        if self.__text is not None:
            self.__text.insert(END, contenido)
            self.setReadOnly(readonly=readonly)

    def clearText(self):
        if self.__text is not None:
            self.__text.delete('1.0', END)

    def setText(self, contenido: str, readonly: bool = False):
        self.clearText()
        self.appendText(contenido, readonly=readonly)

    def setReadOnly(self, readonly: bool):
        if readonly:
            self.__text.config(state=DISABLED)
        else:
            self.__text.config(state=NORMAL)

    @property
    def name(self) -> str:
        return self.__name

    # endregion


class GeneralEntradaTexto:
    __parent: GeneralDivTab
    __name: str
    __text: Entry

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int,
                 height=4, width=50, columnspan: int = 1, rowspan: int = 1):
        self.__name = name
        self.__parent = parent
        self.__text = Entry(self.__parent.nucleo)
        self.__text.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)
        self.__parent.addItem(self)

    def getText(self) -> str:
        return self.__text.get()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    def clearText(self):
        if self.__text is not None:
            self.__text.delete(0, END)

    def setText(self, contenido: str):
        self.clearText()
        self.__text.insert(0, contenido)

    # endregion


class GeneralButton:
    __parent: GeneralDivTab
    __name: str
    __button: Button

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int,
                 command=None, columnspan: int = 1, rowspan: int = 1):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__button = Button(parent.nucleo, text=self.__name, command=command)
        self.__button.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Button:
        return self.__button

    # endregion


class GeneralCombox:
    __parent: GeneralDivTab
    __name: str
    __box: Combobox

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, values: list,
                 columnspan: int = 1, rowspan: int = 1):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__box = Combobox(self.parent.nucleo, values=values)
        self.__box.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)
        self.__box.current(0)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Combobox:
        return self.__box

    def getCurrent(self):
        return self.__box.current()

    def getCurrentText(self) -> str:
        return self.__box.get()

    # endregion


class GeneralCheckBox:
    __parent: GeneralDivTab
    __name: str
    __box: Checkbutton
    __variable: IntVar

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int,
                 columnspan: int = 1, rowspan: int = 1):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__variable = IntVar()
        self.__box = Checkbutton(self.__parent.nucleo, text=name, variable=self.__variable, onvalue=1, offvalue=0)
        self.__box.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Checkbutton:
        return self.__box

    def var(self) -> IntVar:
        return self.__variable

    # endregion


class GeneralLabel:
    __parent: GeneralDivTab
    __name: str
    __label: Label

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, text: str, row: int, col: int,
                 columnspan: int = 1, rowspan: int = 1):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__label = Label(self.__parent.nucleo, text=text)
        self.__label.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Label:
        return self.__label

    # endregion


class GeneralPhoto:
    __parent: GeneralDivTab
    __name: str
    __image = None
    __label: Label

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, content: bytes, row: int, col: int,
                 columnspan: int = 1, rowspan: int = 1, width: int = 300, height: int = 300):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__image = ImageTk.PhotoImage(Image.open(BytesIO(content)).resize((height, width), Image.ANTIALIAS))
        self.__label = Label(self.__parent.nucleo, image=self.__image, height=height, width=width)
        self.__label.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Label:
        return self.__label

    # endregion


class GeneralProgressBar:
    __parent: GeneralDivTab
    __name: str
    __bar: Progressbar

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int,
                 columnspan: int = 1, rowspan: int = 1):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__bar = Progressbar(self.__parent.nucleo, orient=HORIZONTAL, maximum=100)
        self.__bar.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Progressbar:
        return self.__bar

    def setProgress(self, prog: float) -> None:
        self.__bar["value"] = prog

    def addProgress(self, prog: float) -> None:
        self.__bar.step(prog)

    def getProgress(self) -> float:
        return self.__bar["value"]

    # endregion


class GeneralListBox:
    __parent: GeneralDivTab
    __name: str
    __list: Listbox
    #__elements: int

    # region Funciones
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int,
                 columnspan: int = 1, rowspan: int = 1, command=None):
        #self.__elements = 0
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__list = Listbox(self.__parent.nucleo)
        self.__list.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, sticky=N+S+E+W)
        if command is not None:
            self.__list.bind("<<ListboxSelect>>", command)

    @property
    def parent(self) -> GeneralDivTab:
        return self.__parent

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nucleo(self) -> Listbox:
        return self.__list

    def addElement(self, value: str):
        self.__list.insert(self.__list.size(), value)
        #self.__elements += 1

    def insertElement(self, value: str, pos: int):
        self.__list.insert(pos, value)
        #self.__elements += 1

    def removeElement(self, pos: int):
        self.__list.delete(pos)
        #self.__elements += 1

    # endregion


# endregion
# region Menu
class GeneralMenuBar:
    __parent: GeneralVentana
    __name: str
    __menu_list: list
    __menubar: Menu

    # region Funciones
    def __init__(self, name: str, parent: GeneralVentana):
        self.__parent = parent
        self.__name = name
        self.__menu_list = []
        self.__parent.setMenuBar(self)
        self.__menubar = Menu(self.__parent.nucleo)
        self.__parent.nucleo.config(menu=self.__menubar)

    def addMenu(self, menu):
        if type(menu) == GeneralMenu:
            self.__menu_list.append(menu)

    @property
    def nucleo(self) -> Menu:
        return self.__menubar

    # endregion


class GeneralMenu:
    __parent: GeneralMenuBar
    __name: str
    __menu: Menu

    # region Funciones
    def __init__(self, name: str, parent: GeneralMenuBar):
        self.__parent = parent
        self.__name = name
        self.__parent.addMenu(self)
        self.__menu = Menu(self.__parent.nucleo, tearoff=0)
        self.__parent.nucleo.add_cascade(label=self.__name, menu=self.__menu)

    @property
    def nucleo(self) -> Menu:
        return self.__menu

    # endregion

# endregion

"""v = GeneralVentana("Ventana1")
v.ventana.geometry("800x400")
g = GeneralNotebook("Notebook", v)
t = GeneralTab("Tab1", g)
t2 = GeneralTab("Tab1", g)
b = GeneralButtonTab("Butt", t)
b2 = GeneralButtonTab("Butt2", t)
b3 = GeneralButtonTab("Butt", t2)
b4 = GeneralButtonTab("Butt2", t2)

v.ventana.mainloop()"""
