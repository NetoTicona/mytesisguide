from tkinter import *
from tkinter import ttk
import cv2
from PIL import ImageTk, Image
import imutils
import pymysql
import numpy as np
import time
import threading
import serial
import os
import datetime
import json
import tkinter.messagebox as messagebox


class Main(object):
    def __init__(self, master):
        self.master = master
        self.cam = None
        # frames
        mainFrame = Frame(self.master)
        mainFrame.pack()
        self.connect = pymysql.connect(
            host="localhost", user="root", passwd="", database="db_image_hsv")
        self.cursor = self.connect.cursor()

        #self.serial_port = serial.Serial('COM13', 9600)
        self.serial_port = serial.Serial('COM14', 9600)

        self.stop_thread_flag = False
        self.arduino_data_var = StringVar()
        self.arduino_data_var.set("Peso: 0 g")
        self.tab_change_enabled = True
        self.weight = 0
        self.initiale_aspect = False
        self.display_frame = True
        # ================================================= top frame =============================
        topFrame = Frame(mainFrame, width=1100, height=110,
                         bg='orange', padx=20, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)
        self.top_image = PhotoImage(file="icon/unsa.png")
        self.top_image = self.top_image.subsample(2, 2)
        self.top_image_label = Label(topFrame, image=self.top_image)
        self.top_image_label.grid(
            row=0, column=0, padx=(0, 10))  # Add padx for spacing
        self.heading = Label(topFrame, text='Universidad nacional de san agustin\n "Diseño e Implementación de un Sistema Clasificador de Mangos\n Usando una Red Neuronal y Visión por Computadora" ',
                             font="arial 18 bold", fg='#003f8a', bg='white')
        # Center align vertically
        self.heading.grid(row=0, column=1, sticky="nsew")
        topFrame.columnconfigure(1, weight=1)
        topFrame.rowconfigure(0, weight=1)
        # =================================================== center frame===========================
        centerFrame = Frame(mainFrame, width=1200,
                            relief=RIDGE, bg="red", height=560)
        centerFrame.pack(side=TOP)
        # =============== center left frame =============
        centerLeftFrame = Frame(
            centerFrame, width=500, height=560, bg="yellow", borderwidth=2, relief="solid")
        centerLeftFrame.pack(side=LEFT)
        centerLeftFrame.pack_propagate(False)
        # ====== Results ===========
        centerLeftFrameResult = Frame(centerLeftFrame, width=400,
                                      height=50, bg="salmon", borderwidth=2, relief="solid")
        centerLeftFrameResult.place(in_=centerLeftFrame,
                                    anchor="center", relx=0.5, rely=0.92)
        centerLeftFrameResult.pack_propagate(False)
        # Create and place the first label with text "Peso: 45Kg"
        self.label_peso = Label(
            centerLeftFrameResult, textvariable=self.arduino_data_var, font="arial 12 bold", bg="salmon")
        self.label_peso.pack(side=LEFT, padx=10)
        # Create and place the second label with text "Resultado: Exportable"
        self.label_resultado = Label(
            centerLeftFrameResult, text="Resultado: Exportable", font="arial 12 bold", bg="salmon")
        self.label_resultado.pack(side=LEFT, padx=10)
        centerLeftFrameResult.columnconfigure(0, weight=1)  #
        # ======= 3 Button =========
        self.btnbook_ign = Button(centerLeftFrame, text='Encendido',
                                  compound=LEFT, font='arial 12 bold', command=self.lets_start, state="normal")
        self.btnbook_ign.place(x=10 + 75, y=10)
        self.btnbook_start = Button(centerLeftFrame, text='Inicio',
                                    compound=LEFT, font='arial 12 bold', command=self. initialize_masks , state="disabled")
        self.btnbook_start.place(x=126 + 75, y=10)

        self.btnbook_shutdown = Button(centerLeftFrame, text='Apagar',
                                       compound=LEFT, font='arial 12 bold', command=self.shut_down, state="disabled")
        self.btnbook_shutdown.place(x=190 + 75, y=10)

        self.btnbook_capture = Button(centerLeftFrame, text='capturar',
                                      compound=LEFT, font='arial 12 bold', command=self.captureTwo, state="disabled")
        self.btnbook_capture.place(x=270 + 75, y=10)

        # ======= innerFrame =======
        innerLeftFrame = Frame(centerLeftFrame, width=400,
                               height=400, bg="salmon", borderwidth=2, relief="solid")
        innerLeftFrame.place(in_=centerLeftFrame,
                             anchor="center", relx=0.5, rely=0.46)
        # Create the buttons
        self.button1 = Button(innerLeftFrame, text="Guardar",
                              font="arial 12 bold", command=self.saveAllValues, state="disabled")
        self.button1.place(relx=0.86, rely=0.98, anchor="s")
        # ============= TABs 1 ============= #
        # padre 345 , tab que sea -30 = 315
        self.tabs = ttk.Notebook(innerLeftFrame, width=400, height=315)
        self.tabs.place(relx=0.5, rely=0.45, anchor="center")
        self.tab1_icon = PhotoImage(file='icon/red.png')
        self.tab2_icon = PhotoImage(file='icon/green.png')
        self.tab3_icon = PhotoImage(file='icon/yellow.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='rojo',
                      image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='verde',
                      image=self.tab2_icon, compound=LEFT)
        self.tabs.add(self.tab3, text='amarillo',
                      image=self.tab3_icon, compound=LEFT)
        # ===== Primera botonera tab 1=========

        def update_label_a1(event):
            self.track1laba1.config(
                text="Hue mínimo: {}".format(self.scalea1.get()))

        def update_label_a2(event):
            self.track1laba2.config(
                text="Hue máximo: {}".format(self.scalea2.get()))

        def update_label_a3(event):
            self.track1laba3.config(
                text="Saturación mínima: {}".format(self.scalea3.get()))

        def update_label_a4(event):
            self.track1laba4.config(
                text="Saturación máxima: {}".format(self.scalea4.get()))

        def update_label_a5(event):
            self.track1laba5.config(
                text="Value mínimo: {}".format(self.scalea5.get()))

        def update_label_a6(event):
            self.track1laba6.config(
                text="Value máximo: {}".format(self.scalea6.get()))
        # ===== Segundo botonera tab 1=========

        def update_label_b1(event):
            self.track1labb1.config(
                text="Hue mínimo: {}".format(self.scaleb1.get()))

        def update_label_b2(event):
            self.track1labb2.config(
                text="Hue máximo: {}".format(self.scaleb2.get()))

        def update_label_b3(event):
            self.track1labb3.config(
                text="Saturación mínima: {}".format(self.scaleb3.get()))

        def update_label_b4(event):
            self.track1labb4.config(
                text="Saturación máxima: {}".format(self.scaleb4.get()))

        def update_label_b5(event):
            self.track1labb5.config(
                text="Value mínimo: {}".format(self.scaleb5.get()))

        def update_label_b6(event):
            self.track1labb6.config(
                text="Value máximo: {}".format(self.scaleb6.get()))
        # ===== Tercera botonera tab 1=========

        def update_label_c1(event):
            self.track1labc1.config(
                text="Hue mínimo: {}".format(self.scalec1.get()))

        def update_label_c2(event):
            self.track1labc2.config(
                text="Hue máximo: {}".format(self.scalec2.get()))

        def update_label_c3(event):
            self.track1labc3.config(
                text="Saturación mínima: {}".format(self.scalec3.get()))

        def update_label_c4(event):
            self.track1labc4.config(
                text="Saturación máxima: {}".format(self.scalec4.get()))

        def update_label_c5(event):
            self.track1labc5.config(
                text="Value mínimo: {}".format(self.scalec5.get()))

        def update_label_c6(event):
            self.track1labc6.config(
                text="Value máximo: {}".format(self.scalec6.get()))
        # ====================== Primer Tab ==================================#
        self.track1laba1 = Label(self.tab1, text="Hue mínimo: 0")
        self.track1laba1.place(x=44, y=100-91)
        self.scalea1 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a1)
        self.scalea1.place(x=140, y=100-91)
        self.track1laba2 = Label(self.tab1, text="Hue máximo: 0")
        self.track1laba2.place(x=41, y=150-91)
        self.scalea2 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a2)
        self.scalea2.place(x=140, y=150-91)
        self.track1laba3 = Label(self.tab1, text="Saturación mínima: 0")
        self.track1laba3.place(x=9, y=200-91)
        self.scalea3 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a3)
        self.scalea3.place(x=140, y=200-91)
        self.track1laba4 = Label(self.tab1, text="Saturación máxima: 0")
        self.track1laba4.place(x=7, y=250-91)
        self.scalea4 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a4)
        self.scalea4.place(x=140, y=250-91)
        self.track1laba5 = Label(self.tab1, text="Value mínimo: 0")
        self.track1laba5.place(x=35, y=300-91)
        self.scalea5 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a5)
        self.scalea5.place(x=140, y=300-91)
        self.track1laba6 = Label(self.tab1, text="Value máximo: 0")
        self.track1laba6.place(x=34, y=350-91)
        self.scalea6 = Scale(self.tab1, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_a6)
        self.scalea6.place(x=140, y=350-91)
        # ====================== Segundo Tab ==================================#
        self.track1labb1 = Label(self.tab2, text="Hue mínimo: 0")
        self.track1labb1.place(x=44, y=100-91)
        self.scaleb1 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b1)
        self.scaleb1.place(x=140, y=100-91)
        self.track1labb2 = Label(self.tab2, text="Hue máximo: 0")
        self.track1labb2.place(x=41, y=150-91)
        self.scaleb2 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b2)
        self.scaleb2.place(x=140, y=150-91)
        self.track1labb3 = Label(self.tab2, text="Saturación mínima: 0")
        self.track1labb3.place(x=9, y=200-91)
        self.scaleb3 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b3)
        self.scaleb3.place(x=140, y=200-91)
        self.track1labb4 = Label(self.tab2, text="Saturación máxima: 0")
        self.track1labb4.place(x=7, y=250-91)
        self.scaleb4 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b4)
        self.scaleb4.place(x=140, y=250-91)
        self.track1labb5 = Label(self.tab2, text="Value mínimo: 0")
        self.track1labb5.place(x=35, y=300-91)
        self.scaleb5 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b5)
        self.scaleb5.place(x=140, y=300-91)
        self.track1labb6 = Label(self.tab2, text="Value máximo: 0")
        self.track1labb6.place(x=34, y=350-91)
        self.scaleb6 = Scale(self.tab2, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_b6)
        self.scaleb6.place(x=140, y=350-91)
        # ====================== Tercer Tab ==================================#
        self.track1labc1 = Label(self.tab3, text="Hue mínimo: 0")
        self.track1labc1.place(x=44, y=100-91)
        self.scalec1 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c1)
        self.scalec1.place(x=140, y=100-91)
        self.track1labc2 = Label(self.tab3, text="Hue máximo: 0")
        self.track1labc2.place(x=41, y=150-91)
        self.scalec2 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c2)
        self.scalec2.place(x=140, y=150-91)
        self.track1labc3 = Label(self.tab3, text="Saturación mínima: 0")
        self.track1labc3.place(x=9, y=200-91)
        self.scalec3 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c3)
        self.scalec3.place(x=140, y=200-91)
        self.track1labc4 = Label(self.tab3, text="Saturación máxima: 0")
        self.track1labc4.place(x=7, y=250-91)
        self.scalec4 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c4)
        self.scalec4.place(x=140, y=250-91)
        self.track1labc5 = Label(self.tab3, text="Value mínimo: 0")
        self.track1labc5.place(x=35, y=300-91)
        self.scalec5 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c5)
        self.scalec5.place(x=140, y=300-91)
        self.track1labc6 = Label(self.tab3, text="Value máximo: 0")
        self.track1labc6.place(x=34, y=350-91)
        self.scalec6 = Scale(self.tab3, from_=0, to=255, orient=HORIZONTAL,
                             length=200, showvalue=0, command=update_label_c6)
        self.scalec6.place(x=140, y=350-91)
        # =============== center right frame ==============
        centerRightFrame = Frame(
            centerFrame, width=700, height=560, bg="blue", borderwidth=2, relief="sunken")
        centerRightFrame.pack(side=RIGHT)
        centerRightFrame.pack_propagate(False)  # previene auto ajuste
        """ self.video_label = Label(centerRightFrame)
        self.video_label.pack() """
        # ================ Tabs para videos ==============
        self.tabs_vid = ttk.Notebook(centerRightFrame, width=600, height=460)
        self.tabs_vid.place(relx=0.5, rely=0.5, anchor="center")
        """ self.tabo_icon_vid = PhotoImage(file='icon/original.png') """
        self.tab1_icon_vid = PhotoImage(file='icon/original.png')
        self.tab2_icon_vid = PhotoImage(file='icon/red.png')
        self.tab3_icon_vid = PhotoImage(file='icon/green.png')
        self.tab4_icon_vid = PhotoImage(file='icon/yellow.png')
        # self.tabo_vid = ttk.Frame(self.tabs_vid  )
        self.tab1_vid = ttk.Frame(self.tabs_vid)
        self.tab2_vid = ttk.Frame(self.tabs_vid)
        self.tab3_vid = ttk.Frame(self.tabs_vid)
        self.tab4_vid = ttk.Frame(self.tabs_vid)
        """ self.tabs_vid.add(self.tabo_vid, text='deff',
                      image=self.tabo_icon_vid, compound=LEFT , state="disabled" ) """
        self.tabs_vid.add(self.tab1_vid, text='original',
                          image=self.tab1_icon_vid, compound=LEFT, state="disabled")
        self.tabs_vid.add(self.tab2_vid, text='red',
                          image=self.tab2_icon_vid, compound=LEFT, state="disabled")
        self.tabs_vid.add(self.tab3_vid, text='green',
                          image=self.tab3_icon_vid, compound=LEFT, state="disabled")
        self.tabs_vid.add(self.tab4_vid, text='yellow',
                          image=self.tab4_icon_vid, compound=LEFT, state="disabled")
        self.tabs_vid.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # ================ Tabs para videos ==============
        """ self.video_label_o = Label(self.tabo_vid)
        self.video_label_o.pack() """
        self.video_label_i = Label(self.tab1_vid)
        self.video_label_i.pack()
        self.video_label_r = Label(self.tab2_vid)
        self.video_label_r.pack()
        self.video_label_g = Label(self.tab3_vid)
        self.video_label_g.pack()
        self.video_label_y = Label(self.tab4_vid)
        self.video_label_y.pack()

    def lets_start(self):
            print("LESt START")
            self.tabs_vid.tab(self.tab1_vid, state="normal")
            self.tab_change_enabled = True
            #self.tabs_vid.tab(self.tab2_vid, state="normal")
            #self.tabs_vid.tab(self.tab3_vid, state="normal")
            #self.tabs_vid.tab(self.tab4_vid, state="normal")

            #self.button1.config(state="normal")
            self.btnbook_ign.config(state="disabled")
            self.btnbook_start.config(state="normal")
            self.btnbook_shutdown.config(state="normal")
            #
            self.initiale_aspect = True
            self.tabs_vid.select(self.tab1_vid)

            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT * from t_hsv")
            rows = self.cursor.fetchall()
            # print("Valores de t_hsv table: ")
            for row in rows:
                if row[0] == 1:
                    # print("111")
                    self.scalea1.set(int(row[2]))
                    self.scalea2.set(int(row[3]))
                    self.scalea3.set(int(row[4]))
                    self.scalea4.set(int(row[5]))
                    self.scalea5.set(int(row[6]))
                    self.scalea6.set(int(row[7]))
                elif row[0] == 3:
                    # print("33")
                    self.scaleb1.set(int(row[2]))
                    self.scaleb2.set(int(row[3]))
                    self.scaleb3.set(int(row[4]))
                    self.scaleb4.set(int(row[5]))
                    self.scaleb5.set(int(row[6]))
                    self.scaleb6.set(int(row[7]))
                elif row[0] == 6:
                    # print("66")
                    self.scalec1.set(int(row[2]))
                    self.scalec2.set(int(row[3]))
                    self.scalec3.set(int(row[4]))
                    self.scalec4.set(int(row[5]))
                    self.scalec5.set(int(row[6]))
                    self.scalec6.set(int(row[7]))
        
         

    def shut_down(self):
        try:
            print("Shut Down")
            self.arduino_data_var.set("Peso: 0 g")
            self.stop_arduino_thread()
            self.tab_change_enabled = False
            #self.initiale_aspect = False
            # self.stop_thread_flag = True
            # self.cam = None
            self.tabs_vid.tab(self.tab1_vid, state="disabled")
            self.tabs_vid.tab(self.tab2_vid, state="disabled")
            self.tabs_vid.tab(self.tab3_vid, state="disabled")
            self.tabs_vid.tab(self.tab4_vid, state="disabled")
            self.button1.config(state="disabled")

            self.btnbook_ign.config(state="normal")
            self.btnbook_start.config(state="disabled")
            self.btnbook_shutdown.config(state="disabled")
            self.btnbook_capture.config(state="disabled")

            self.scalea1.set(int(0))
            self.scalea2.set(int(0))
            self.scalea3.set(int(0))
            self.scalea4.set(int(0))
            self.scalea5.set(int(0))
            self.scalea6.set(int(0))

            self.scaleb1.set(int(0))
            self.scaleb2.set(int(0))
            self.scaleb3.set(int(0))
            self.scaleb4.set(int(0))
            self.scaleb5.set(int(0))
            self.scaleb6.set(int(0))

            self.scalec1.set(int(0))
            self.scalec2.set(int(0))
            self.scalec3.set(int(0))
            self.scalec4.set(int(0))
            self.scalec5.set(int(0))
            self.scalec6.set(int(0))

            if self.cam is not None:
                self.cam = None
                # self.cam.release()
                # cv2.destroyAllWindows()
                print("Se finalizó")
            # self.clean_center_right_frame()
        except Exception as e:
            messagebox.showerror("Error", "Ocurrio error al apagar")
            print("Error al extraer data: ", e)

    def initialize_masks(self):
        self.btnbook_capture.config(state="normal")
        try:
            self.initiale_aspect = False
            self.tab_change_enabled = True
            if not hasattr(self, 'arduino_thread') or not self.arduino_thread.is_alive():
                self.serial_port.write(b'START')
                self.start_arduino_thread()
            """ self.tabs_vid.tab(self.tabo_vid, state="normal")  """
            self.tabs_vid.tab(self.tab1_vid, state="normal")
            self.tabs_vid.tab(self.tab2_vid, state="normal")
            self.tabs_vid.tab(self.tab3_vid, state="normal")
            self.tabs_vid.tab(self.tab4_vid, state="normal")

            self.button1.config(state="normal")
            self.btnbook_ign.config(state="disabled")
            self.btnbook_start.config(state="disabled")
            self.btnbook_shutdown.config(state="normal")
            self.btnbook_capture.config(state="normal")
            
            # ======== cam ========#
            # global cam
            # cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            # self.start_camera_orig()
            # ======== SQL ========#
            # print("Vamos a iniciar")
            # self.cursor.close()
        except Exception as e:
            messagebox.showerror("Error", "Ocurrio error al iniciar")
            print("Error al extraer data: ", e)

    def captureTwo(self):

        #self.tab_change_enabled = False
        print("Boton de capture 2")
        self.display_frame = False
        try:

            if self.cam is not None :
                ret, frame = self.cam.read()
                frame_red = frame.copy()
                frame_green = frame.copy()
                frame_yellow = frame.copy()
                if ret == True:
                    save_dir = "mangoes"
                    #----------- guadar datos de entrenamiento------#
                    os.makedirs(save_dir, exist_ok=True)
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    capture_filename = os.path.join(save_dir, f"frame_{ current_datetime }.jpg")
                    cv2.imwrite(capture_filename, frame)
                    print(f"El peso del mango es: { str( self.weight ) }" )
                    r_hue_min = self.scalea1.get()
                    r_hue_max = self.scalea2.get()
                    r_sat_min = self.scalea3.get()
                    r_sat_max = self.scalea4.get()
                    r_val_min = self.scalea5.get()
                    r_val_max = self.scalea6.get()
                    _frame_red,_weight_red = self.process_frame( frame_red , r_hue_min,r_sat_min,r_val_min,r_hue_max,r_sat_max,r_val_max , frame , (255,0,0) )

                    g_hue_min = self.scaleb1.get()
                    g_hue_max = self.scaleb2.get()
                    g_sat_min = self.scaleb3.get()
                    g_sat_max = self.scaleb4.get()
                    g_val_min = self.scaleb5.get()
                    g_val_max = self.scaleb6.get()
                    _frame_green,_weight_green = self.process_frame( frame_green , g_hue_min,g_sat_min,g_val_min,g_hue_max,g_sat_max,g_val_max , _frame_red , (0,255,0) )

                    y_hue_min = self.scalec1.get()
                    y_hue_max = self.scalec2.get()
                    y_sat_min = self.scalec3.get()
                    y_sat_max = self.scalec4.get()
                    y_val_min = self.scalec5.get()
                    y_val_max = self.scalec6.get()
                    _frame_yellow,_weight_yellow = self.process_frame( frame_yellow , y_hue_min,y_sat_min,y_val_min,y_hue_max,y_sat_max,y_val_max , _frame_green , (0,0,255))

                    obj_g = { "id":1, "weight":_weight_green,"description":"Verde" }
                    obj_r = { "id":2, "weight":_weight_red,"description":"Rojo" }
                    obj_y = { "id":3, "weight":_weight_yellow,"description":"Amarillo" }

                    color_g = json.dumps( obj_g )
                    color_r = json.dumps( obj_r )
                    color_y = json.dumps( obj_y )
                    predominant = self.getBigArea( color_g,color_y,color_r )

                    dataTraining_sql = "insert into mangoe_training (peso , img_url , red_area, green_area , yellow_area , predominant_color) values ( %s , %s ,%s , %s ,%s , %s ) "
                    values = ( str(self.weight ), str( capture_filename ) ,str(_weight_red) , str( _weight_green ) , str( _weight_yellow ) , str( predominant ) )
                    self.cursor.execute( dataTraining_sql , values)
                    self.connect.commit()
                    result = messagebox.showinfo("Success", "Se capturó correctamente")
                    if result == "ok":
                        #self.tab_change_enabled = True
                        print("Boton de capture after ok")
                        self.display_frame = True
                        self.handle_original_tab()
       


        except Exception as e:
            messagebox.showerror( "Error" , "Error al capturar datos" )
            print("Error al extraer data: ", e)

       


    def start_arduino_thread(self):
        # Reset the flag when starting the thread.
        self.stop_thread_flag = False
        self.arduino_thread = threading.Thread(target=self.read_arduino_data)
        self.arduino_thread.daemon = True
        self.arduino_thread.start()

    def stop_arduino_thread(self):
        self.stop_thread_flag = True

    def read_arduino_data(self):
        while not self.stop_thread_flag:
            #print("_flag: " + str(self.stop_thread_flag))
            try:
                # self.serial_port.write(b'START')
                arduino_data = self.serial_port.readline().decode().strip()
                #print("data: " + arduino_data)
                if not self.stop_thread_flag:
                    self.weight = arduino_data
                    self.arduino_data_var.set(f"Peso: {arduino_data} g")
                else:
                    self.arduino_data_var.set("Peso: 0 g")
                # time.sleep(1)
            except serial.SerialException:
                print("Serial port error")
            except Exception as e:
                print("Error reading Arduino data:", e)

    def setTimeout(self, func, timeout):
        def wrapper():
            func()
        timeout_mill = timeout/1000
        timer = threading.Timer(timeout_mill, wrapper)
        timer.start()

    def saveAllValues(self):
        try:
            # Print values from Tab 1
            r_hue_min = self.scalea1.get()
            r_hue_max = self.scalea2.get()
            r_sat_min = self.scalea3.get()
            r_sat_max = self.scalea4.get()
            r_val_min = self.scalea5.get()
            r_val_max = self.scalea6.get()
            self.update_tab_values(1, r_hue_min, r_hue_max,
                                r_sat_min, r_sat_max, r_val_min, r_val_max)
            # Print values from Tab 2
            a_hue_min = self.scaleb1.get()
            a_hue_max = self.scaleb2.get()
            a_sat_min = self.scaleb3.get()
            a_sat_max = self.scaleb4.get()
            a_val_min = self.scaleb5.get()
            a_val_max = self.scaleb6.get()
            self.update_tab_values(3, a_hue_min, a_hue_max,
                                a_sat_min, a_sat_max, a_val_min, a_val_max)
            # Print values from Tab 3
            v_hue_min = self.scalec1.get()
            v_hue_max = self.scalec2.get()
            v_sat_min = self.scalec3.get()
            v_sat_max = self.scalec4.get()
            v_val_min = self.scalec5.get()
            v_val_max = self.scalec6.get()
            self.update_tab_values(6, v_hue_min, v_hue_max,
                                v_sat_min, v_sat_max, v_val_min, v_val_max)
        except Exception as e:
            messagebox.showerror("Error", "Ocurrio error al guardar")
            print("Error al extraer data: ", e)

    def update_tab_values(self, id, hue_min, hue_max, sat_min, sat_max, val_min, val_max):
        r_sql = "update t_hsv set hue_min=%s, hue_max=%s, sat_min=%s, sat_max=%s, val_min=%s, val_max=%s where id=%s"
        values = (str(hue_min), str(hue_max), str(sat_min),
                  str(sat_max), str(val_min), str(val_max), id)
        self.cursor.execute(r_sql, values)
        self.connect.commit()

    def clean_center_right_frame(self):
        for widget in self.centerRightFrame.winfo_children():
            widget.destroy()

    def start_camera_orig(self):



        if self.cam is not None and self.display_frame :

            

            ret, frame = self.cam.read()
            if self.initiale_aspect:

                if ret == True:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    font = cv2.FONT_HERSHEY_COMPLEX
                    weight = 999
                    cv2.putText( frame, "el espo se mide en newtons" , (20,20), font, 0.68 , (255,255,255),1,cv2.LINE_AA  )

                    im = Image.fromarray(frame)
                    img = ImageTk.PhotoImage(image=im)
                    # -------------------  -------------------------#
                    self.video_label_i.configure(image=img)
                    self.video_label_i.image = img
                    self.video_label_i.after(10, self.start_camera_orig)
                else:
                    print("ret no es True")


            else:
                frame_red = frame.copy()
                frame_green = frame.copy()
                frame_yellow = frame.copy()
                if ret == True:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    r_hue_min = self.scalea1.get()
                    r_hue_max = self.scalea2.get()
                    r_sat_min = self.scalea3.get()
                    r_sat_max = self.scalea4.get()
                    r_val_min = self.scalea5.get()
                    r_val_max = self.scalea6.get()
                    _frame_red,_weight_red = self.process_frame( frame_red , r_hue_min,r_sat_min,r_val_min,r_hue_max,r_sat_max,r_val_max , frame , (255,0,0) )

                    g_hue_min = self.scaleb1.get()
                    g_hue_max = self.scaleb2.get()
                    g_sat_min = self.scaleb3.get()
                    g_sat_max = self.scaleb4.get()
                    g_val_min = self.scaleb5.get()
                    g_val_max = self.scaleb6.get()
                    _frame_green,_weight_green = self.process_frame( frame_green , g_hue_min,g_sat_min,g_val_min,g_hue_max,g_sat_max,g_val_max , _frame_red , (0,255,0) )

                    y_hue_min = self.scalec1.get()
                    y_hue_max = self.scalec2.get()
                    y_sat_min = self.scalec3.get()
                    y_sat_max = self.scalec4.get()
                    y_val_min = self.scalec5.get()
                    y_val_max = self.scalec6.get()
                    _frame_yellow,_weight_yellow = self.process_frame( frame_yellow , y_hue_min,y_sat_min,y_val_min,y_hue_max,y_sat_max,y_val_max , _frame_green , (255,147,24))

                    obj_g = { "id":1, "weight":_weight_green,"description":"Verde" }
                    obj_r = { "id":2, "weight":_weight_red,"description":"Rojo" }
                    obj_y = { "id":3, "weight":_weight_yellow,"description":"Amarillo" }

                    color_g = json.dumps( obj_g )
                    color_r = json.dumps( obj_r )
                    color_y = json.dumps( obj_y )
                    predominant = self.getBigArea( color_g,color_y,color_r )

                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText( _frame_yellow, f"El area rojo es: {str(_weight_red)}" , (250, 350), font, 0.68 , (0,0,0),1,cv2.LINE_AA  )
                    cv2.putText( _frame_yellow, f"El area verde es: {str(_weight_green)}" , (250,370), font, 0.68 , (0,0,0),1,cv2.LINE_AA  )
                    cv2.putText( _frame_yellow, f"El area amarillo es: {str(_weight_yellow)}" , (250,390), font, 0.68 , (0,0,0),1,cv2.LINE_AA  )
                    cv2.putText( _frame_yellow, f"El color predominante es: { predominant } " , (120,450), font, 0.68 , (0,0,0),1,cv2.LINE_AA  )


                    im = Image.fromarray(_frame_yellow)
                    img = ImageTk.PhotoImage(image=im)
                    # -------------------  -------------------------#
                    self.video_label_i.configure(image=img)
                    self.video_label_i.image = img
                    self.video_label_i.after(10, self.start_camera_orig)
                else:
                  print("ret no es True")
        else:  
            print("sel cam is nonee")

    def start_camera_red(self):
        if self.cam is not None:
            ret, frame = self.cam.read()
            frame_copy = frame.copy()
            if ret == True:

                r_hue_min = self.scalea1.get()
                r_hue_max = self.scalea2.get()
                r_sat_min = self.scalea3.get()
                r_sat_max = self.scalea4.get()
                r_val_min = self.scalea5.get()
                r_val_max = self.scalea6.get()


                _frame,_weight = self.process_frame( frame_copy , r_hue_min,r_sat_min,r_val_min,r_hue_max,r_sat_max,r_val_max , frame , (0,0,255) )

                #print( f"El área total rojo es: { weight }"  )
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText( _frame, f"El area rojo total es: {_weight}" , (200,450), font, 0.68 , (0,0,255),1,cv2.LINE_AA  )

                frame_rgb = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                im_red = Image.fromarray( frame_rgb )
                img_red = ImageTk.PhotoImage(image=im_red)
                # -------------------  -------------------------#
                self.video_label_r.configure(image=img_red)
                self.video_label_r.image = img_red
                self.video_label_r.after(10, self.start_camera_red)
            else:
                print("ret no es True")

    def start_camera_green(self):
        if self.cam is not None:
            ret, frame = self.cam.read()
            if ret == True:
                g_hue_min = self.scaleb1.get()
                g_hue_max = self.scaleb2.get()
                g_sat_min = self.scaleb3.get()
                g_sat_max = self.scaleb4.get()
                g_val_min = self.scaleb5.get()
                g_val_max = self.scaleb6.get()

                _frame,_weight = self.process_frame( frame , g_hue_min,g_sat_min,g_val_min,g_hue_max,g_sat_max,g_val_max, frame , (0,255,0) )


                #print( f"El área total verde es: { weight }"  )
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText( _frame, f"El area verde total es: {_weight}" , (200,450), font, 0.68 , (0,255,0),1,cv2.LINE_AA  )
             
                frame_rgb = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                im_green = Image.fromarray( frame_rgb )
                img_green = ImageTk.PhotoImage(image=im_green)
                # -------------------  -------------------------#
                self.video_label_g.configure(image=img_green)
                self.video_label_g.image = img_green
                self.video_label_g.after(10, self.start_camera_green)
            else:
                print("ret no es True")

    def start_camera_yellow(self):
        if self.cam is not None:
            ret, frame = self.cam.read()
            if ret == True:
                y_hue_min = self.scalec1.get()
                y_hue_max = self.scalec2.get()
                y_sat_min = self.scalec3.get()
                y_sat_max = self.scalec4.get()
                y_val_min = self.scalec5.get()
                y_val_max = self.scalec6.get()

                _frame,_weight = self.process_frame( frame , y_hue_min,y_sat_min,y_val_min,y_hue_max,y_sat_max,y_val_max, frame , (24,147,255) )

                #print( f"El área total rojo es: { weight }"  )
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText( _frame, f"El area amarilla total es: {_weight}" , (200,450), font, 0.68 , (24,147,255),1,cv2.LINE_AA  )

                #print( f"El área total amarillo es: { _weight }"  )
                frame_rgb = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                im_yellow = Image.fromarray(frame_rgb)
                img_yellow = ImageTk.PhotoImage(image=im_yellow)
                # -------------------  -------------------------#
                self.video_label_y.configure(image=img_yellow)
                self.video_label_y.image = img_yellow
                self.video_label_y.after(10, self.start_camera_yellow)
            else:
                print("ret no es True")

    def update_database(self, tab_name, column_name, new_value):
        self.cursor.execute("select * from t_hsv")
        rows = self.cursor.fetchall()
        """ print("Valores de t_hsv table: ")
        for row in rows:
            print(row) """
        # self.cursor.close()

    def on_tab_change(self, event):
        if self.tab_change_enabled:
            #print("tab cambio")
            selected_tab_index = self.tabs_vid.index(self.tabs_vid.select())
            if selected_tab_index == 0:
                # Action for the 'original' tab
                self.handle_original_tab()
            elif selected_tab_index == 1:
                # Action for the 'red' tab
                self.handle_red_tab()
            elif selected_tab_index == 2:
                # Action for the 'green' tab
                self.handle_green_tab()
            elif selected_tab_index == 3:
                # Action for the 'yellow' tab
                self.handle_yellow_tab()
        else:
            print("tab_change_enabled Dehabilitado")
    # Separate functions for each tab change

    def handle_original_tabo(self):
        # Your code for the 'original' tab action
        print("000 tab selected")
        if self.cam is not None:
            self.cam.release()
            cv2.destroyAllWindows()
            self.cam = None

    def handle_original_tab(self):
        # Your code for the 'original' tab action
        #print("Original tab selected")
        print("original TAB")
        if self.cam is not None:
            self.cam.release()
            cv2.destroyAllWindows()
            self.cam = None
        self.setTimeout(self.my_function_orig, 100)

    def my_function_orig(self):
        print("Mi funcion origg")
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.start_camera_orig()

    def handle_red_tab(self):
        # Your code for the 'red' tab action
        if self.cam is not None:
            self.cam.release()
            cv2.destroyAllWindows()
            self.cam = None
        self.setTimeout(self.my_function_red, 100)

    def my_function_red(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.start_camera_red()

    def handle_green_tab(self):
        if self.cam is not None:
            self.cam.release()
            cv2.destroyAllWindows()
            self.cam = None
        self.setTimeout(self.my_function_green, 100)

    def my_function_green(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.start_camera_green()

    def handle_yellow_tab(self):
        if self.cam is not None:
            self.cam.release()
            cv2.destroyAllWindows()
            self.cam = None
        self.setTimeout(self.my_function_yellow, 100)

    def my_function_yellow(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.start_camera_yellow()

    def getBigArea( self , object_v , object_a , object_r ):
        color = ""
        object_v = json.loads(object_v)
        object_a = json.loads(object_a)
        object_r = json.loads(object_r)

        if( (object_v["weight"] >= object_a["weight"]) and ( object_v["weight"] >= object_r["weight"] )  ):
            color = object_v["description"]
        elif( (object_a["weight"] >= object_v["weight"]) and ( object_a["weight"] >= object_r["weight"] ) ):
            color = object_a["description"]
        else:
            color = object_r["description"]

        return color

    def process_frame( self,frame ,hue_min,sat_min,val_min,hue_max,sat_max,val_max , sumframe , colorval ):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([hue_min, sat_min, val_min])
        upper_red = np.array([hue_max, sat_max, val_max])
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        #(blur)imgBlur = cv2.GaussianBlur( mask_red , (5,5) , 1 )
        kernel = np.ones( (2,2) , np.uint8 )
        #(blur)erosion = cv2.erode( imgBlur , kernel , iterations=2 )
        #(blur)dilatacion = cv2.dilate( erosion , kernel , iterations=3 )
        kernelTomorf = np.ones( (3,3) , np.uint8 )
        erosion = cv2.erode( mask_red , kernelTomorf , iterations=4 )
        dilatacion = cv2.dilate( erosion , kernelTomorf , iterations=4 )
        closing = cv2.morphologyEx( dilatacion , cv2.MORPH_CLOSE , kernel )


        contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_total = 0
        contourTouched = []
        #------------------ Get The Area ------------------------------//
        """ for c in contours:
            area = cv2.contourArea(c)
            if area > 4500:
                #print(f"Contour red{counter + 1}: Area = {area}")
                cv2.drawContours( sumframe , contours,  -1 , colorval, 2, cv2.LINE_AA)
                area_total += area """
        if contours and hierarchy is not None and len(hierarchy[0]) > 0:
            
            for i in range(len(contours)):
                if not(i in contourTouched) :
                    contour = contours[i]
                    hierarchy_info = hierarchy[0][i]
                    print("hierarchy_info: " + str(i))
                    print(hierarchy_info)
                    if hierarchy_info[2] > -1: #tiene hijo
                        area_father = cv2.contourArea( contour )
                        cv2.drawContours( sumframe , [contour],  -1 , (255,0,0), 1, cv2.LINE_AA)
                        #extraer todos los contornos cuyo padre es el anterior
                        brothers_area = 0
                        for j in range(len(contours)):
                            hierarchy_brother = hierarchy[0][j]
                            if hierarchy_brother[3] == i : 
                                brother_contour = contours[j]
                                brothers_area +=  cv2.contourArea( brother_contour )
                                cv2.drawContours( sumframe , [brother_contour],  -1 , (0,255,0), 1, cv2.LINE_AA)
                                contourTouched.append( j )
                        #endForbrother
                        #simple way:
                        """ area_child = cv2.contourArea(  contours[ hierarchy_info[2]  ] )
                        cv2.drawContours( sumframe , [contours[ hierarchy_info[2] ]],  -1 , (0,255,0), 1, cv2.LINE_AA) """
                        #Tiene hermano? next
                        area = area_father - brothers_area
                        area_total += area
                    else:
                        print("No tiene hijo!!!")
                        area_child = cv2.contourArea( contour )
                        cv2.drawContours( sumframe , [contour],  -1 , (255,255,255), 1, cv2.LINE_AA)
                        area_total += area_child
                    print("\n")
                else:
                    print("El contorno tocado {}".format(i)  )
            #fin For
            print( "El area total es: {}".format( area_total )  )

        #--------------------------------------------------------------//

        return sumframe , area_total      





    def on_closing(self):
        print("cerrando ventana")
        self.shut_down()
        self.master.destroy()


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Managment System")
    root.geometry("1200x670")
    root.iconbitmap("icon/my.ico")
    root.resizable( False , False )
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
