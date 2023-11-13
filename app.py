from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFilter, ImageOps,ImageFont
import textwrap
from io import BytesIO
from webcolors import rgb_to_name, hex_to_rgb, CSS3_HEX_TO_NAMES
from flask import Flask, request, send_file
from PIL import Image
import os
import torch
from webcolors import rgb_to_name, hex_to_rgb, CSS3_HEX_TO_NAMES
import base64
import requests
import json
import uuid

app = Flask(__name__, static_folder='static')

# stable-diffusion model pipline
 

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def rgb_to_color_name(rgb):
    try:
        color_name = rgb_to_name(rgb)
        return color_name
    except ValueError:
        closest_match = min(
            CSS3_HEX_TO_NAMES.items(),
            key=lambda item: sum((a - b) ** 2 for a, b in zip(hex_to_rgb(item[0]), rgb)))[1]
        return closest_match



def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))



def rgb_to_rgba(rgb, alpha):
    rgb = [max(0, min(255, val)) for val in rgb]
    rgba = tuple(rgb + [alpha])
    return rgba

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgba = rgb + (255,)
    
    return rgba

def process_image(input_path,input_path_logo,text_input,button_text,hex_code):
        input_image_path = input_path
        hex_color_code = hex_code
        logo_path = input_path_logo
        text=text_input
        button_text=button_text
        corner_radius = 20
        path_ttf="timr45w.ttf"
        size_val=300
        #input format is changed by check_ai,check_ai==True if stable-diffusion model is used
        response = requests.get(input_image_path)
    
    # İsteğin başarılı olup olmadığını kontrol et
        if response.status_code == 200:
        # BytesIO nesnesine dönüştür
         img = Image.open(BytesIO(response.content)).convert("RGBA")
        
        rgb_values = hex_to_rgb(hex_color_code)
        color_name = rgb_to_color_name(rgb_values)
        text_color=color_name
        text0="ok "+text_color

        #changing shape of image 
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], corner_radius, fill=255)
        image_result_original = Image.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, 0)), img)
        image_result_original.putalpha(mask)
        ratio=image_result_original.width/image_result_original.height

        #adding background
        image_result=image_result_original.resize((int(size_val*ratio),size_val), Image.LANCZOS)
        background_size=(int(size_val*2.5),int(size_val*2.5))
        new_image = Image.new("RGB", background_size, "white") 
        width_bg, height_bg = new_image.size
        width_overlay, height_overlay = image_result.size
        x_position = (width_bg - width_overlay) // 2
        y_position = int(size_val*0.55)+20
        combined = Image.new("RGBA", new_image.size)
        combined.paste(new_image, (0, 0))
        combined.paste(image_result, (x_position, y_position), image_result)

        #adding logo
        logo_first = Image.open(logo_path).convert("RGBA")
        ratio_logo=logo_first.width/logo_first.height
        size_logo_val=int(size_val/2)
        logo=logo_first.resize((int(size_logo_val*ratio_logo),size_logo_val), Image.BICUBIC)
        width_overlay_logo, height_overlay_logo = logo.size
        x_position = (width_bg - width_overlay_logo) // 2
        y_position = 20

        combined_logo = Image.new("RGBA", combined.size)
        combined_logo.paste(combined, (0, 0))
        combined_logo.paste(logo, (x_position, y_position), logo)


        #adding top bar and bottom bar 
        rectangle_width = int(size_val*2.25)
        rectangle_height = 10
        radius = 50
        x_position = (combined_logo.width - rectangle_width) // 2
        y_position =int((-1400/size_val)) 
        rgb_code=hex_to_rgb(hex_color_code)
        rgba_values_0 = rgb_to_rgba(rgb_code,0)
        rgba_values_255 = rgb_to_rgba(hex_to_rgb(hex_color_code),255)
        rounded_rectangle = Image.new('RGBA', (rectangle_width, rectangle_height), rgba_values_0)
        draw = ImageDraw.Draw(rounded_rectangle)
        draw.rounded_rectangle([(0, 0), (rectangle_width, rectangle_height)], radius, fill=hex_to_rgba(hex_color_code))
        combined_logo.paste(rounded_rectangle, (x_position, y_position), rounded_rectangle)

        y_position_bottom = int(2.48*size_val)
        rounded_rectangle_bottom = Image.new('RGBA', (rectangle_width, rectangle_height), rgb_to_rgba(hex_to_rgb(hex_color_code),0))
        draw = ImageDraw.Draw(rounded_rectangle)
        draw.rounded_rectangle([(0, 0), (rectangle_width, rectangle_height)], radius, fill=hex_to_rgba(hex_color_code))
        combined_logo.paste(rounded_rectangle, (x_position, y_position_bottom), rounded_rectangle)

        #adding frame
        border_size = 2
        border_color = (0, 0, 0) 
        image_with_frame = ImageOps.expand(combined_logo, border=border_size, fill=border_color)
        image_width, image_height = image_with_frame.size
        draw = ImageDraw.Draw(image_with_frame)

        #adding punchline text
        font_size = 45
        font = ImageFont.truetype(path_ttf, font_size)
        max_text_width = image_width - 40 
        wrapped_text = textwrap.fill(text, width=30) 
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((image_width - text_width) // 2, (image_height - text_height) // 2 + image_height // 4)
        text_color = rgb_code 
        draw.multiline_text(text_position, wrapped_text, font=font, fill=text_color, align="center")
        #adding button
        button_color = rgb_code 
        button_font_size = 30
        button_font = ImageFont.truetype(path_ttf, button_font_size)
        button_width = 300
        button_height = 45
        button_position = ((image_width - button_width) // 2, text_position[1] + text_height + 30)  # Yüksekliği ayarlandı

        draw.rounded_rectangle([button_position, (button_position[0] + button_width, button_position[1] + button_height)],
                            fill=button_color, outline=None, width=0, radius=10)

        button_text_position = ((image_width - button_width) // 2 + (button_width - draw.textlength(button_text, font=button_font)) // 2,
                            button_position[1] + 5)  
        button_text_color = (255, 255, 255)  


        draw.text(button_text_position, button_text, font=button_font, fill=button_text_color)

  
        image_with_frame

        output_buffer = BytesIO()

      
        image_with_frame.save(output_buffer, format="PNG")

       
        output_buffer.seek(0)

        return output_buffer

def process_sd_image_procedure(file_input, prompt_input,hex_input):
    try:
        
        user_name = "iamsmblc"
        repo_name = "images"
        github_token = ""
        hex_color_code = hex_input
        rgb_values = hex_to_rgb(hex_color_code)
        color_name = rgb_to_color_name(rgb_values)
        text_color = color_name
        #prompt text with hex color input
        prompt_text = prompt_text = prompt_input + ", " + text_color 
        uploaded_file = file_input
        file_name = str(uuid.uuid4())[:8] + ".png"
        
        file_data = base64.b64encode(uploaded_file.read()).decode('utf-8')

        #upload to Github
        response = requests.put(
                f"https://api.github.com/repos/{user_name}/{repo_name}/contents/{file_name}",
                headers={"Authorization": f"Bearer {github_token}"},
                json={
                    "message": "New file uploaded",
                    "content": file_data,
                },
            )
        response.raise_for_status()

        input_file = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/main/{file_name}"
        
        url = "https://stablediffusionapi.com/api/v3/img2img"

        payload = json.dumps({
            "key": "R7ZvSv1UVlKrQKvwZPlWasyl252mWJh9W4pFIh2JbkvMCo4zSV3qfCYUjhNd",
            "prompt": prompt_text,
            "negative_prompt": None,
            "init_image": input_file,
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "30",
            "safety_checker": "no",
            "enhance_prompt": "yes",
            "guidance_scale": 7.5,
            "strength": 0.7,
            "seed": None,
            "webhook": None,
            "track_id": None
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  

        data = json.loads(response.text)
        output_value = data["output"]

        image_url = output_value[0]
       

        return image_url

    except :
     return "Please re-upload the images and try again."
    

#banner without stable-diffusion model image
@app.route('/get-without-diff', methods=['POST'])
def upload_file_without_diff():
   try:
    if 'file' not in request.files or 'file_logo' not in request.files:
        return 'Both files are required', 400

    file = request.files['file']
    file_logo = request.files['file_logo']
    hex_code = request.form.get('hex_input')  
    text_input = request.form.get('text_input')  
    button_text = request.form.get('button_text_input')  

    if file.filename == '' or file_logo.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename) and file_logo and allowed_file(file_logo.filename):
        
        output_buffer = process_image(file, file_logo, text_input,button_text, hex_code)

       
        return send_file(output_buffer, as_attachment=True, download_name='banner.png', mimetype='image/png'), 200
    else:
        return 'Invalid file type. Please upload files of type png', 400
   except:
       return "Please re-upload the images and try again."
 # stable-diffusion model image
@app.route('/get-diff', methods=['POST'])
def process_sd_image():
    try:
        if 'file_diff' not in request.files:
         return 'File is are required', 400     
        hex_color_code = request.form.get('hex_diff')
        prompt_text = request.form.get('prompt') 
        uploaded_file = request.files['file_diff']
        image_url=process_sd_image_procedure(uploaded_file, prompt_text,hex_color_code)
        
        
        response = requests.get(image_url)
        response.raise_for_status() 
        image = Image.open(BytesIO(response.content))
        img_byte_array = BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        return send_file(img_byte_array, mimetype='image/png')
    except:  
       return "Please re-upload the images and try again." 

 #banner with stable-diffusion model image- 
@app.route('/get-result', methods=['POST'])
def upload_file():
    try:
        if 'file_diff' not in request.files or 'file_logo' not in request.files:
            return 'Both files are required', 400
        uploaded_file = request.files['file_diff']
        hex_color_code = request.form.get('hex_diff')
        rgb_values = hex_to_rgb(hex_color_code)
        color_name = rgb_to_color_name(rgb_values)
        text_color = color_name
        file_logo = request.files['file_logo']
        hex_code = request.form.get('hex_input')  
        text_input = request.form.get('text_input')  
        button_text = request.form.get('button_text_input')  

        prompt_text = request.form.get('prompt')    
        processed_image=process_sd_image_procedure(uploaded_file, prompt_text,hex_color_code)

        

        if uploaded_file.filename == '' or file_logo.filename == '':
            return 'No selected file', 400

        if processed_image and allowed_file(uploaded_file.filename) and file_logo and allowed_file(file_logo.filename):
            
            output_buffer = process_image(processed_image, file_logo, text_input,button_text, hex_code)

        
            return send_file(output_buffer, as_attachment=True, download_name='banner.png', mimetype='image/png'), 200
        else:
            return 'Invalid file type. Please uplad files of type png', 400
    except:  
       return "Please re-upload the images and try again." 

@app.route('/', methods=['GET'])
def get_app():
    return "App works."
if __name__ == '__main__':
    app.run(debug=True)
