import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

onStart = True
bot_command_fp = "/home/PunchAdmin/bot/soundboard_command.txt"

#buttons = [
#  {"label": "Button1", "image_url": "url_to_image1"}
#]

buttons = []
img_to_sound_map = {}

# Ensure there's a folder to save the uploads
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_SOUND_EXTENSIONS = {'mp3', 'ogg'}

def build_button_list():
    img_file_list = os.listdir('static/images')
    sound_file_list = os.listdir('sounds')
    print(img_file_list)
    print(sound_file_list)

    if len(img_file_list) != len(sound_file_list):
        print("IMAGE AND SOUND FILE MISMATCH!")

    for i in range(len(img_file_list)):
        for j in range(len(sound_file_list)):
            img_name_and_ext = img_file_list[i]
            sound_name_and_ext = sound_file_list[j]
            img_name = img_name_and_ext.split(".")[0]
            sound_name = sound_name_and_ext.split(".")[0]
            if img_name == sound_name:
                if img_name_and_ext not in img_to_sound_map:
                    img_to_sound_map[img_name_and_ext] = sound_name_and_ext
                    print(url_for("static", filename='images/'+img_name_and_ext))
                    buttons.append({"label": img_name_and_ext, "image_url": url_for('static', filename='images/'+img_name_and_ext)})

@app.route('/')
def index():
    build_button_list()
    #buttons[0]["image_url"] = url_for('static', filename='images/joanas_guiide_error.png')
    return render_template('index.html', buttons=buttons)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/handle_button_click', methods=['POST'])
def handle_button_click():
    img_name = request.form['label']
    f = open(bot_command_fp, "w")
    f.write(img_to_sound_map[img_name])
    return redirect(url_for('index'))

#@app.route('/image_button-clicked', methods=['POST'])
#def image_button_clicked():
#    print("IMAGE BUTTON WAS CLICKED!")
#    f = open(bot_command_fp, "w")
#    f.write("megaman.mp3")
#    f.close()
#    return redirect(url_for('index'))

@app.route('/button-clicked', methods=['POST'])
def button_clicked():
    print("BUTTON WAS CLICKED!")
    return redirect(url_for('upload'))

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'image' not in request.files and 'sound' not in request.files:
        print("No file!")
        return redirect(request.url)
    f_img = request.files['image']
    f_sound = request.files['sound']
    if f_img.filename == '' or f_sound.filename == '':
        print("No selected file!")
        return redirect(request.url)
    if f_img and f_sound:
        img_filename = f_img.filename
        sound_filename = f_sound.filename
        img_ext = img_filename.split(".")[-1]
        sound_ext = sound_filename.split(".")[-1]
        print("IMG EXT: " + str(img_ext))
        print("SOUND EXT: " + str(sound_ext))

        if img_ext not in ALLOWED_IMG_EXTENSIONS or sound_ext not in ALLOWED_SOUND_EXTENSIONS:
            # TODO: Put an error message
            print("Submitted unallowed extension!")
            return redirect(url_for('index'))

        button_id = 1
        if len(buttons) != 0:
            button_id = int(buttons[-1]['label'].split(".")[0]) + 1
        
        f_img.save(os.path.join("static/images", str(button_id) + "." + img_ext))
        f_sound.save(os.path.join("sounds", str(button_id) + "." + sound_ext))
        return redirect(url_for('index'))
    else:
        return redirect(request.url)

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)
