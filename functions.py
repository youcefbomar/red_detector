import cv2 as cv
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog



def starter(path,save_path):
    frames_path=path_maker(path)
    frames_list = video_to_frames(path)


    for i in range(0,len(frames_list),2) :

        cv.imwrite(os.path.join(frames_path,f'frames{i}.jpg'), red_detector(frames_list[i]))

    frames_path = os.path.join(os.path.dirname(path),'frames')
    images_to_video(frames_path,save_path)
    deleter(path)





def deleter(path):
    path=os.path.dirname(path)
    frames_path = os.path.join(path, 'frames')
    os.chmod(frames_path, 0o777)  # Sets full permissions
    shutil.rmtree(frames_path)

def path_maker(path) :
    path=os.path.dirname(path)
    frames_path = os.path.join(path, 'frames')
    if os.path.isdir(frames_path) == False:
        os.makedirs(frames_path)
    else :
        os.chmod(frames_path, 0o777)  # Sets full permissions
        shutil.rmtree(frames_path)
        os.makedirs(frames_path)
    return frames_path



def red_detector(img) :
    
    new_img = img
    img_size=len(img)
    for x in range(img_size):
        j=0

        for i in img[x]:
            if i[2]>i[1]+80 and i[2]>i[0] :

                new_img[x][j] = i
                
            else :

                new_img[x][j] = [255,255,255]
                
            j+=1
    return new_img



def images_to_video(directory, output_path, fps=15):
    output_path = os.path.join(output_path,'video.mp4')
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No image files found in the directory.")
        return

    # Sort the files numerically based on the frame number in the file name
    image_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()))

    # Read the first image to get dimensions (height and width)
    first_frame = cv.imread(os.path.join(directory, image_files[0]))
    if first_frame is None:
        print(f"Error reading the first image {image_files[0]}")
        return

    height, width, _ = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 'mp4v' codec for mp4 output
    video_writer = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    # Loop through the image files and add each one as a frame in the video
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        frame = cv.imread(image_path)

        if frame is None:
            print(f"Error reading {image_file}, skipping...")
            continue

        # Resize the frame to match the size of the first frame (if necessary)
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv.resize(frame, (width, height))

        # Write the frame to the video
        video_writer.write(frame)

    # Release the video writer and finish
    video_writer.release()
    print(f"Video saved to {output_path}")


def video_to_frames(video_path):
    # Open the video file
    video_capture = cv.VideoCapture(video_path)
    frames = []

    # Loop through the frames of the video
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        # If a frame was successfully read
        if ret:
            frames.append(cv.resize(frame,(len(frame[0])//4,len(frame)//4)))
        else:
            break

    # Release the video capture object
    video_capture.release()
    return frames


def video_directory():

    root = tk.Tk()
    root.withdraw()  

    video_path = filedialog.askopenfilename(title="Select Your Video")
    return video_path


def save_directory():

    root = tk.Tk()
    root.withdraw()  

    save_path = filedialog.askdirectory(title="Where To Save it")
    return save_path
    