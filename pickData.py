from tkinter import *
from tkinter import ttk
import math
import pandas as pd
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt


class Main(object):
    def __init__(self, master):
        self.master = master
        self.exportable_mode = False
        self.non_exportable_mode = False
        self.normal_mode = True
        self.show_coords = StringVar()
        self.show_coords.set("ola")
        self.exportable_points = []  # Array to store exported points
        mainFrame = Frame(self.master)
        mainFrame.pack()

        topFrame = Frame(mainFrame, width=1200, height=50,
                         bg="orange", padx=20, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)

         # Add the first button with background color blue
        exportable_button = Button(topFrame, text="Exportable", bg="blue", fg="white" , command=self.toggle_exportable_mode )
        exportable_button.grid(row=0, column=0, padx=10, pady=5)

        # Add the second button with background color red
        no_exportable_button = Button(topFrame, text="No Exportable", bg="red", fg="white" , command=self.toggle_no_exportable_mode )
        no_exportable_button.grid(row=0, column=1, padx=10, pady=5)

        no_exportable_button = Button(topFrame, text="No selection", bg="gray", fg="white" , command=self.toggle_normal_mode )
        no_exportable_button.grid(row=0, column=2, padx=10, pady=5)

        self.label_coords = Label( topFrame , textvariable=self.show_coords ,font="arial 12 bold" )
        self.label_coords.grid( row=0 , column=3, padx=10, pady=5 )

        # =========== center ===================//
        centerFrame = Frame(mainFrame, width=1200,
                            relief=RIDGE, bg="blue",  borderwidth=0, height=600)
        centerFrame.pack(side=TOP)

        # ===============  left frame  ===========================//
         # Add a frame with width 600
        frame1 = Frame(centerFrame, width=1100, height=600, bg="green")
        frame1.pack(side=LEFT)
        # ----------------- verticals inside left ---------------------//
          # Add two vertical frames inside frame1 with height 250 each
        subframe1 = Frame(frame1, width=1100, height=530, bg="yellow")
        subframe1.pack(side=TOP)

       # Implementing interactive grid
        grid_canvas = Canvas(subframe1, width=1000, height=520, bg="white")
        grid_canvas.pack()

        # Define grid range and step sizes
        x_start, x_end, x_step = 300, 1000, 5
        y_start, y_end, y_step = -0.1, 1.1, 0.1

        # Create grid points
        grid_points = []
        for x in range(x_start, x_end + x_step, x_step):
            for y in range(int(y_start * 10), int((y_end + y_step) * 10), int(y_step * 10)):
                grid_points.append((x, y / 10))

        # Create circles for each grid point with reduced size
        point_radius = 2  # Adjust the radius as needed

        def on_point_click(event):
            item = grid_canvas.find_closest(event.x, event.y)
            x_pixel = grid_canvas.coords(item)[0] + point_radius
            y_pixel = grid_canvas.coords(item)[1] + point_radius
            x_value = x_pixel / 1000 * (x_end - x_start) + x_start
            y_value = y_pixel / 520 * (y_end - y_start) + y_start
            self.show_coords.set( str(x_value) + " , " + str(  round(1-y_value , 1 ))   )


            if self.exportable_mode:
                grid_canvas.itemconfig(item, fill="blue")
                grid_canvas.itemconfig(item, tags=("exported_point",))
                point_value = 1
                self.exportable_points.append((( x_value, round(1-y_value , 1 )), point_value))

            elif self.non_exportable_mode:
                grid_canvas.itemconfig(item, fill="red")
                grid_canvas.itemconfig(item, tags=("exported_point",))
                point_value = 0
                self.exportable_points.append((( x_value, round(1-y_value , 1 )), point_value))
            else:
                grid_canvas.itemconfig(item, fill="gray")
                grid_canvas.itemconfig(item, tags=("exported_point",))
                self.show_coords.set( str(x_value) + " , " + str(  round(1-y_value , 1 ))   )
                print("array para exportar")
                print( self.exportable_points )

                updated_points_list = [point for point in self.exportable_points if point[0] != ( x_value, round(1-y_value , 1 )) ]
                self.exportable_points = updated_points_list
                print( "borrado: ", updated_points_list  )






        for x, y in grid_points:
            if x == x_end:
                continue

            # Skip creating ovals for the first column and last row
            x_pixel = (x - x_start) / (x_end - x_start) * 1000
            y_pixel = (y - y_start) / (y_end - y_start) * 520
            point = grid_canvas.create_oval(
                x_pixel - point_radius, y_pixel - point_radius,
                x_pixel + point_radius, y_pixel + point_radius,
                fill="gray", outline=""
            )
            grid_canvas.tag_bind(point, "<Button-1>", on_point_click)


        for y_label in range(int(y_start * 10), int((y_end + y_step) * 10), int(y_step * 10)):
            y_pixel_label = ((y_label / 10 - y_start) / (y_end - y_start) * 520)
            grid_canvas.create_text(1000, y_pixel_label, text=f"{(y_label / 10)-1:.1f}", anchor=E, font=("Helvetica", 8), fill="purple" )


        #----------------- fin verticals inside left ---------------//
        subframe2 = Frame(frame1, width=1100, height=70, bg="purple")
        subframe2.pack(side=BOTTOM)

        save_button = Button( subframe2 , text="Guardar" , command=self.save_array  )
        save_button.grid( row=0, column=3 , padx=10 , pady=10 )

        draw_button = Button(  subframe2 , text="Dibujar" , command=self.draw_excel  )
        draw_button.grid( row=0, column=5 , padx=10 , pady=10 )


        #============= right frame ==============================//
        # Add a frame with width 300
        frame2 = Frame(centerFrame, width=100, height=600, bg="red")
        frame2.pack(side=LEFT)


    def toggle_exportable_mode(self):
        self.exportable_mode = True
        self.non_exportable_mode = False

    def toggle_no_exportable_mode(self):
        self.exportable_mode = False
        self.non_exportable_mode = True

    def toggle_normal_mode(self):
        self.exportable_mode = False
        self.non_exportable_mode = False

    def save_array( self  ):
        print( "Guardar" )
        print( self.exportable_points )
        columns = {'a': [], 'b': [], 'z': []}
        for entry in self.exportable_points:
            columns['a'].append(entry[0][0])
            columns['b'].append(entry[0][1])
            columns['z'].append(entry[1])

        # Create a DataFrame
        df = pd.DataFrame(columns)

        # Save the DataFrame to an Excel file
        df.to_excel('output.xlsx', index=False)

    def draw_excel(self):
        print( "Dibujar es un excel" )
        file_path = self.select_file()
        if file_path:
            a_values, b_values, z_values = self.read_excel_and_convert(file_path)
            coordinates = list(zip(a_values, b_values))

            self.draw_coordinates(coordinates, z_values)


    def select_file(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])
        root.destroy()
        return file_path

    def read_excel_and_convert(self,file_path):
    # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Extract values for 'a', 'b', and 'z' columns
        a_values = df['a'].tolist()
        b_values = df['b'].tolist()
        z_values = df['z'].tolist()

        return a_values, b_values, z_values

    def draw_coordinates(self,coordinates, z_values):
        x = [point[0] for point in coordinates]
        y = [point[1] for point in coordinates]

        colors = []

        for z in z_values:
            if z == 1:
                colors.append('blue')
            elif z == 0:
                colors.append('red')

        plt.scatter(x, y, marker='o', c=colors)
        plt.title('')
        plt.xlabel('Peso')  # Rename the x-axis
        plt.ylabel('Color')  # Rename the y-axis

        plt.grid(True)
        plt.show()




def main():
    root = Tk()
    app = Main(root)
    root.title("Mi data picker")
    root.geometry("1200x650")
    root.resizable( False , False )
    root.mainloop()


if __name__ == "__main__":
    main()
