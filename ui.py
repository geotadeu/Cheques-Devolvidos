from imp import create_dynamic
from config import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from idlelib.tooltip import Hovertip

class UI():
    def __init__(self, root):
        self.root = root

    def start(self, onSubmit):
        self.onSubmit = onSubmit
        self.root.title("Tratamento de Cheques Devolvidos")
        self.root.configure(background='#003641')
        self.root.geometry("700x450")
        self.root.resizable(False, False)
        self.root.maxsize(width=900, height=600)
        self.root.minsize(width=500, height=200)
        self.root.iconbitmap('config\icon_square.ico')
        self.img_help = PhotoImage(file='icons\help.png').subsample(2, 2)
        self.img_csv = PhotoImage(file='icons\csv.png').subsample(2, 2)
        self.img_txt = PhotoImage(file='icons\\txt.png').subsample(2, 2)
        self.img_save = PhotoImage(file='icons\seta.png').subsample(3, 3)
        self.relatorios = ["Compensação geral", "PA selecionado", "Todos PAs"]
        self.create_frames()
        self.render_frame1()
        self.render_frame2()
        self.root.mainloop()

    def create_frames(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#00AE9D', highlightbackground='#ffffff', highlightthickness=3, highlightcolor='#ffffff', relief=FLAT)
        self.frame_1.place(relx=0.01, rely=0.02, relwidth=0.48, relheight=0.96)

        self.frame_2 = Frame(self.root, bd=4, bg='#00AE9D', highlightbackground='#ffffff', highlightthickness=3, highlightcolor='#ffffff', relief=FLAT)
        self.frame_2.place(relx=0.5, rely=0.02, relwidth=0.49, relheight=0.96)

        self.frame_2_1 = Frame(self.frame_2, bd=4, bg='#00AE9D', highlightbackground='#00AE9D', highlightthickness=3, highlightcolor='#00AE9D', relief=FLAT)
        self.frame_2_1.place(relx=0.02, rely=0.00, relwidth=0.96, relheight=0.15)

        self.frame_2_2 = Frame(self.frame_2, bd=4, bg='#00AE9D', highlightbackground='#00AE9D', highlightthickness=3, highlightcolor='#00AE9D', relief=FLAT)
        self.frame_2_2.place(relx=0.02, rely=0.13, relwidth=0.96, relheight=0.33)

        self.frame_2_3 = Frame(self.frame_2, bd=4, bg='#00AE9D', highlightbackground='#00AE9D', highlightthickness=3, highlightcolor='#00AE9D', relief=FLAT)
        self.frame_2_3.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.45)
    
    def get_coop(self):
        if hasattr(self, 'coop_cb'):
            return self.coop_cb.get()
        return -1

    def get_pa(self):
        if hasattr(self, 'pa_cb'):
            return self.pa_cb.get()
        return -1

    def toggle_fields(self, event):
        self.lb_coop.place_forget()
        self.coop_cb.place_forget()
        self.lb_pa.place_forget()
        self.pa_cb.place_forget()

        if(self.rel_cb.get() == "Compensação geral" or self.rel_cb.get() == "PA selecionado"):
            self.lb_coop.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.2)
            self.coop_cb.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.2)
            self.lb_pa.place(relx=0.25, rely=0.50, relwidth=0.5, relheight=0.2)
            self.pa_cb.place(relx=0.25, rely=0.70, relwidth=0.5, relheight=0.2)
        elif(self.rel_cb.get() == "Todos PAs"):
            self.lb_coop.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.2)
            self.coop_cb.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.2)

    def render_frame1(self):
        # [LABEL] Caminho de relatórios
        self.lb_info = Label(self.frame_1, text="Caminho dos Relatórios:", bg='#00AE9D', font=('Asap SemiBold', 13))
        self.lb_info.place(relx=0.12, rely=0.02, relwidth=0.8, relheight=0.06)

        # [LABEL] Relatório C/C
        self.lb_info = Label(self.frame_1, text="Relatório de Dev. de CHs C/C - CCO 083:", bg='#00AE9D', font=('Asap SemiBold', 10))
        self.lb_info.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.06)
        self.lb_info = Label(self.frame_1, text="Conta-Corrente → Relatório → Corporativo \n→ CompeSuaRemessa → Cheques devolvidos \n→ Todos/Todos\n* Retirar relatório em formato CSV", bg='#00AE9D', font=('Asap Regular', 9))
        self.lb_info.place(relx=0.05, rely=0.16, relwidth=0.9, relheight=0.15)

        # [LABEL] Relatório Intercredis
        self.lb_info = Label(self.frame_1, text="Relatório de Dev. de CHs Intercredis - CCO 148:", bg='#00AE9D', font=('Asap SemiBold', 10))
        self.lb_info.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.06)
        self.lb_info = Label(self.frame_1, text="Conta-Corrente → Relatório de Fechamento \n→ CCO 148\n* Retirar relatório em formato TXT Formatado", bg='#00AE9D', font=('Asap Regular', 9))
        self.lb_info.place(relx=0.05, rely=0.39, relwidth=0.9, relheight=0.15)

        # [LABEL] Relatório C/P
        self.lb_info = Label(self.frame_1, text="Relatório de Dev. de CHs C/P:", bg='#00AE9D', font=('Asap SemiBold', 10))
        self.lb_info.place(relx=0.05, rely=0.57, relwidth=0.9, relheight=0.06)
        self.lb_info = Label(self.frame_1, text="Conta-Poupança → Relatório de Cheques Devolvidos\n* Retirar relatório em formato CSV", bg='#00AE9D', font=('Asap Regular', 9))
        self.lb_info.place(relx=0.05, rely=0.62, relwidth=0.9, relheight=0.1)

        # [LABEL] Dúvidas
        self.lb_info = Label(self.frame_1, text="Em caso de dúvidas, entrar em contato\ncom o setor de Compensação\nAnábio ou Geovane\n(37) 3216-8700", bg='#00AE9D', font=('Asap Regular', 9))
        self.lb_info.place(relx=0.05, rely=0.82, relwidth=0.9, relheight=0.13)

    def render_frame2(self):
        # [BUTTON] Ajuda
        self.bt_help = Button(self.frame_2, image=self.img_help, command=self.help_click, bd=0, bg='#00AE9D', font=('Asap Regular', 10), activebackground="#00AE9D", activeforeground="#00AE9D")
        self.bt_help.place(relx=0.9, rely=0.001, relwidth=0.1, relheight=0.07)
        self.myTip = Hovertip(self.bt_help, 'Em caso de dúvidas, entrar em contato\n        com o setor de Compensação\n                Anábio ou Geovane\n                     (37) 3216-8700')

        # [COMBOBOX] Tipo de relatório
        self.lb_rel = Label(self.frame_2_1, text='Tipo de relatório:', bg='#00AE9D', font=('Asap SemiBold', 13))
        self.lb_rel.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.5)
        self.rel_cb = ttk.Combobox(self.frame_2_1, values=self.relatorios, font=('Asap Regular', 10), state='readonly')
        self.rel_cb.bind('<<ComboboxSelected>>', lambda e: self.toggle_fields(e))
        self.rel_cb.place(relx=0.25, rely=0.50, relwidth=0.5, relheight=0.5)
        self.rel_cb.set(self.relatorios[0])
        self.myTip = Hovertip(self.rel_cb, 'Informe o tipo de relatório\nque deseja exportar')

        # [COMBOBOX] Cooperativa
        self.lb_coop = Label(self.frame_2_2, text='Selecione a COOP:', bg='#00AE9D', font=('Asap SemiBold', 13))
        self.lb_coop.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.2)
        self.coop_cb = ttk.Combobox(self.frame_2_2, values=Config.ListaCoop, font=('Asap Regular', 10), state='readonly')
        self.coop_cb.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.2)
        self.coop_cb.set(Config.CoopAtual)
        self.myTip = Hovertip(self.coop_cb, 'Informe o número da\nsua cooperativa')

        # [COMBOBOX] PA
        self.lb_pa = Label(self.frame_2_2, text='Selecione o PA:', bg='#00AE9D', font=('Asap SemiBold', 13))
        self.lb_pa.place(relx=0.25, rely=0.50, relwidth=0.5, relheight=0.2)
        self.pa_cb = ttk.Combobox(self.frame_2_2, values=Config.ListaPA, font=('Asap Regular', 10), state='readonly')
        self.pa_cb.place(relx=0.25, rely=0.70, relwidth=0.5, relheight=0.2)
        self.pa_cb.set('PA0000')
        self.myTip = Hovertip(self.pa_cb, 'Informe o número do\nseu PA')

        # [BUTTON] Abrir arquivo Dev Cheques C/C - Formato CSV
        self.bt_openFile01 = Button(self.frame_2_3, text="    Abrir arquivo CSV - Devolução CCO 083", command=self.open_file1, image=self.img_csv, compound=LEFT, bd=3, bg='#C9D200', font=('Asap Regular', 10))
        self.bt_openFile01.place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.20)
        self.myTip = Hovertip(self.bt_openFile01, 'Conta-Corrente → Relatório → Corporativo \n→ CompeSuaRemessa → Cheques devolvidos \n→ Todos/Todos\n\n* Retirar relatório em formato CSV')

        # [BUTTON] Abrir arquivo Dev Cheques Intercredis - Relatório CCO 148 - Formato TXT
        self.bt_openFile02 = Button(self.frame_2_3, text="    Abrir arquivo TXT Formatado - CCO 148", command=self.open_file2, bd=3, bg='#C9D200', image=self.img_txt, compound=LEFT, font=('Asap Regular', 10))
        self.bt_openFile02.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.20)
        self.myTip = Hovertip(self.bt_openFile02, 'Conta-Corrente → Relatório de Fechamento \n→ CCO 148\n\n* Retirar relatório em formato TXT Formatado')

        # [BUTTON] Abrir arquivo Dev Cheques C/P - Formato CSV
        self.bt_openFile03 = Button(self.frame_2_3, text="    Abrir arquivo CSV     -      Devolução C/P", command=self.open_file3, bd=3, bg='#C9D200', image=self.img_csv, compound=LEFT, font=('Asap Regular', 10))
        self.bt_openFile03.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.20)
        self.myTip = Hovertip(self.bt_openFile03, 'Conta-Poupança → Relatório de Cheques Devolvidos\n\n* Retirar relatório em formato CSV')

        # [BUTTON] Enviar
        self.bt_enviar = Button(self.frame_2_3, text="ENVIAR ", command=self.onSubmit, image=self.img_save, compound=RIGHT, bd=3, bg='#49479D', fg='#ffffff', font=('Asap SemiBold', 11))
        self.bt_enviar.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.20)

    def open_file1(self):
        self.path1 = filedialog.askopenfilename(initialdir="", title="", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    def open_file2(self):
        self.path2 = filedialog.askopenfilename(initialdir="", title="", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

    def open_file3(self):
        self.path3 = filedialog.askopenfilename(initialdir="", title="", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    def help_click(self):
        messagebox.showinfo('Sobre', 'Este software foi desenvolvido por Geovane Tadeu\nEmail: geovanetadeu97@hotmail.com\nwww.github.com/geotadeu')



####### Cores Sicoob ######
# Branco            #ffffff
# Turquesa          #00AE9D
# Verde Escuro      #003641
# Roxo              #49479D
# Verde Medio       #7DB61C
# Verde Claro       #C9D200