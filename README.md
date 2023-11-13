# bannerapp
Banner App

Flask API with Stable Diffusion Image Generation
This Flask API implementation utilizes the stable diffusion model from the img2img model to generate banners based on user input. Follow the steps below to set up and run the application.

Requirements
You can install them by running:

pip install -r requirements.txt

Run the Flask application:

python app.py

Access the API with your preferred platform using the following base URL:

http://localhost:xxx

Check if the API works:

Send a GET request to the following endpoint:
[GET] http://localhost:xxx/
Generate a Stable Diffusion Image:

Send a POST request to the following endpoint:
[POST] http://localhost:xxx/get-diff
Include the required input key and any additional requirements as specified by the API.

key                           type             value
file_diff                    file              The image you want to transform into stable diffusion

hex_diff                     text              hex code of the color to be used in the image
prompt                       text              prompt text

Send a POST request to the following endpoint:
[[POST] http://localhost:xxx/get-diff](http://localhost:xxx:/get-result)

key                           type             value
file_diff                    file              The image you want to transform into stable diffusion
file_logo                    file              logo
text_input                   text              Punchline text
hex_input                    text              color for banner
button_text_input            text              button text
hex_diff                     text              hex code of the color to be used in the image
prompt                       text              prompt text

sample inputs and output
inputs

file_diff
![cup_input](https://github.com/iamsmblc/bannerapp/assets/70532406/440680ac-022f-4dc5-b907-bed172c7f5a9)

file_logo
![logo](https://github.com/iamsmblc/bannerapp/assets/70532406/0ab7fce2-beb9-48f9-adb6-4a5f27bea89d)

text_input
this is a test

hex_input
#f5ef42

button_text_input
buton text

hex_diff
#f5ef42

prompt
flowers on cup

output

![image](https://github.com/iamsmblc/bannerapp/assets/70532406/6ad3aba3-92be-4e53-9124-f38b5a8bf836)

