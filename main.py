import functions  
import tkinter as tk

def video_button() :
    global video_path
    video_path=functions.video_directory()
def save_button() :
    global save_path
    save_path=functions.save_directory()

def start_button() :
    global save_path,video_path
    functions.starter(video_path,save_path)



root = tk.Tk()
root.title("Red Detector")


button = tk.Button(root, text="Where Is Your Video", command=video_button)
button.pack()

button = tk.Button(root, text="Where YouWant To Save The Final Result", command=save_button)
button.pack()


button = tk.Button(root, text="Start", command=start_button)
button.pack()

root.mainloop()



print(functions.video_path)
functions.starter(functions.video_path,functions.save_path)





