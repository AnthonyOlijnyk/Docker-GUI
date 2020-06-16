from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import threading
import shutil
from nilearn import plotting

# Global variable that creates an instance of a tkinter window object.
root = Tk()

class GUI(Frame):
    
    # Initializing what is seen on the appication when it starts up.
    def __init__(self, master):

        # Creating a label with a specific text, font, foreground color, and background color.
        self.lab = Label(master, text="Test Images", font=("Disos", 28), fg="#f4f4f4", bg="#333333")
        # Specifying where on the application I want to attach the label. The sticky
        # parameter indicates that I want this widget to be slid over to the left side
        # (or west side) of the application. The pady and padx parameters indicate
        # how much space between widgets I would like using an x-y grid.
        self.lab.grid(row=0, column=0, sticky=W, pady=4, padx=5)

        # Same as lab, but this label shows "Hello!" instead.
        self.t1 = Label(master, text="Hello!", font=("Disos", 28), fg="#f4f4f4", bg="#333333")
        # I attach this label to column 3 because I wanted it on the right side of the application.
        self.t1.grid(row=0, column=3, pady=4, padx=10)

        # This function creates a listbox object on the application. A listbox is a drop down menu
        # where select one element from it and that element is then highlighted. This is like the 
        # file saving window on windows machnies. Here is specify the background color, foreground
        # color, font, and the mode I want this listbox to operate in, here it is single. Single mode
        # ensures that you can only select one single item from the list.
        self.lbx = Listbox(master, bg="#555555", fg="#f4f4f4", font=("Disos", 16), selectmode=SINGLE)
        # Adding the test image to the listbox as the first element in the list.
        self.lbx.insert(1, "tantupdated:test")
        # Attaching the listbox at certain x,y locations. here, I use columnspan and rowspan
        # to allow the listbox to take up 4 columns worth of space horizontally and 4 rows worth
        # of space vertically. I also use sticky to allow the listbox to expand in all directions
        # to fill up space.
        self.lbx.grid(row=1, column=0, columnspan=4, rowspan=4, padx=5, pady=1, sticky=E+W+S+N)

        # Creating and addinig a button to the application. I specify text to be shown on the button,
        # a background color, an active background color (ie. when the button is pressed, what color
        # does it change to), a font, and a command. The command determines which function the button
        # should activate upon pressing.
        self.obtn1 = Button(master, text="Run", bg="#99fadc", activebackground="#7ecfd4", font=("Disos", 28), command=self.startThread)
        # Similar to the other objects, I specify a certain x,y position I want the button to appear on
        # the application and allow it to stretch out both east and west 4 columns worth of space using
        # a combination of columnspan and sticky.
        self.obtn1.grid(row=5, column=0, columnspan=4, padx=2, pady=2, sticky=E+W)

        # This button is the same as the previous, only a different function is activated upon press.
        self.obtn2 = Button(master, text="Show", bg="#99fadc", activebackground="#7ecfd4", font=("Disos", 28), command=self.showImage)
        self.obtn2.grid(row=6, column=0, columnspan=4, padx=2, pady=2, sticky=E+W)

        # This button is once again similar to the previous one but a different function will activate
        # when it is pressed.
        self.obtn3 = Button(master, text="Delete", bg="#99fadc", activebackground="#7ecfd4", font=("Disos", 28), command=self.startThreadDeleteImage)
        self.obtn3.grid(row=7, column=0, columnspan=4, padx=2, pady=2, sticky=E+W)

        # This command is telling the 0th column to fill up any horizontal space that it can with 
        # respect to the geometrical size of the window. Previously, we had used sticky to fill up
        # space, but sticky only fills up the space that a specific column takes up. This will allow
        # the 0th column to fill up any space that is left over regardless of the allocated column 
        # space. Weight being one indicates that it should take up space while a weight of zero would
        # mean that it shouldn't take up space. This command is used in junction with the listbox and
        # buttons in order to get them to fill up the desired amount of space horizontally.
        master.grid_columnconfigure(0, weight=1)
        # This is the same as column configure but with row one this time. This row will expand to fill
        # up space in the vertical direction. This specific command is used in junction with the listbox
        # in order to get the listbox to fill up the desired amount of space vertically.
        master.grid_rowconfigure(1, weight=1)
        # This command configures the background color of the main window.
        master.config(bg="#333333")

    # This function tries to delete an image that is saved on the docker server as well as
    # any temporary files that have been copied from the docker server onto the host machine.
    # If an error occurs, a message box pops up indicating what went wrong.
    def deleteImage(self):
            try:
                # lbx.get(lbx.curselection()) is a function that will get the text that is
                # currently being selected in the listbox. 
                imageName = "anthonyolijnyk/" + self.lbx.get(self.lbx.curselection())
                # Running a command in terminal.
                os.system("docker rmi " + imageName)
                # Changing what the text of a certain label says.
                self.t1.config(text="Image Deleted")
                # Removing the temporary files from the out directory.
                shutil.rmtree(os.path.join(os.getcwd(), "out", "app"))
                # Changing what the text of a certain label says.
                self.t1.config(text="Files Deleted")
            except FileNotFoundError:
                # Showing the error message.
                messagebox.showerror("Note", "Temporary files already deleted.")

    # This function shows the volume that was used to make the prediction as well as the predicted
    # segmentation volume in two separate windows. If there are no images found, an error message
    # will pop up.
    def showImage(self):
            try:
                # Determining the path to the original volume.
                original_volume = (os.path.join(os.getcwd(), "out", "app", "prediction", "h17_FLAIR_01.nii.gz"))
                # Determining the path to the segmented volume.
                segmented_volume = (os.path.join(os.getcwd(), "out", "app", "data", "h17_FLAIR_01.nii.gz"))
                # Plotting both of the volumes.
                plotting.plot_img(original_volume, title="h17_FLAIR_01 (Original)")
                plotting.plot_img(segmented_volume, title="h17_FLAIR_01 (Predicted)")
                # Showing the plot.
                plotting.show()
            except ValueError:
                # Error message.
                messagebox.showerror("Error", "Files not found, try running the image first so that the temporary files appear in the out folder.")
            
    # This function will attempt to run the specified image in a containerized environment. Once the
    # container is running, the message of "Check Terminal!" will appear in the top right of the window
    # indicating that the command line interface is ready for use. After exiting the command line interface,
    # the process cleans up after itself by removing the unneeded container from memory.
    def runImage(self):
            # Getting the proper command text from the listbox selection.
            imageName = "anthonyolijnyk/" + self.lbx.get(self.lbx.curselection())
            # Changing label text.
            self.t1.config(text="Pulling...")
            # Creating a progress bar that indicates that the process is working correctly.
            # Here I specify it to load horizontally, have a length of 300, and operate in the
            # indeterminate mode meaning that it will show a box bouncing back and forth instead
            # of a bar loading to 100%.
            pbar = ttk.Progressbar(self, orient=HORIZONTAL, length=300, mode="indeterminate")
            # Attaching the progress bar to the application.
            pbar.grid(row=0, column=2, pady=4, padx=10)
            # Setting a reocurring timer for the progress bar to follow.
            pbar.start(10)
            # Updating the main tkinter loop so that we can see the changes we made to the application
            # without needing to wait to get out of the function.
            self.update()
            # Issuing terminal command. This command will pull the docker image from the docker hub
            # page and save it to the server.
            os.system("docker pull " + imageName)
            # Updating main loop.
            self.update()
            # Once the pulling process is complete, the progress bar is no longer needed so it can be
            # removed. 
            pbar.destroy()
            # Changing label text.
            self.t1.config(text="Check Terminal!")
            # Updating main loop.
            self.update()
            # This terminal command will run the docker image and start the command line interface.
            os.system("docker run -it --name temp " + imageName)
            # This terminal command will copy temporary files made from the docker image into the
            # specified out folder in the ui directory.
            os.system("docker cp temp:/app ./out")
            # This terminal command removes the containerized environment after the process is complete.
            os.system("docker rm temp")
            # Changing label text.
            self.t1.config(text="Execution Complete")
    
    # Starting an asynchronous process for running a docker image. This function solves the previous
    # problem of having the application not respond when the docker image was being pulled.
    def startThread(self):
            threading.Thread(target=self.runImage).start()
    # Similar to the previous function, but the asynchronous process being run this time is different.
    def startThreadDeleteImage(self):
            threading.Thread(target=self.deleteImage).start()

# A function that, when the application is x'd out, will destroy the temporary files that are
# saved in the out directory.
def onClosing():
    # Finding the temporary files.
    directory = os.path.join(os.getcwd(), "out", "app")
    # Checking if the directory exists.
    if os.path.isdir(directory):
        # Deleting the directory.
        shutil.rmtree(os.path.join(os.getcwd(), "out", "app"))
    # Killing the application.
    root.destroy()

def main():
    # Setting the size of the application window on startup.
    root.geometry("950x800")
    # Setting the title of the application window.
    root.title("Container Testing")
    # Creating an instance of the GUI object passing the global object root as the parameter.
    play = GUI(root)
    # Issuing a command that when the application is x'd out, run the onClosing function.
    root.protocol("WM_DELETE_WINDOW", onClosing)
    # Main loop that continuously runs the program.
    root.mainloop()


if __name__ == '__main__':
    main()
