
# ---
# this driver script iterates through checkpoints on the same text prompt
# all outputs saved to the same folder
# i first checked every 50 checkpoints, then shorten the range and checked every 10 or 20 checkpoints
# ---

import os
import subprocess
import time
import re


# text prompt

prompt="dumpling the little black cat with golden eyes"


# define the checkpoints you want to iterate through

base_path = "/model/checkpoint-"
file_name = "pytorch_lora_weights.safetensors"
checkpoint_list = [f"{base_path}{i}/{file_name}" for i in range(100,300,10)] # update what's in the range()


# set output folder

output_folder = "output_images/dumpling" # update this

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# web_endpoint served by Modal

base_url="https://dumplingisabeast--dumpling-dreambooth-app-model-web--5c92db-dev.modal.run/"




# ---
# helper functions
# ---

## update file path accordingly if need
def replace_dir(new_dir):
    with open("06_gpu_and_ml/dreambooth/dumpling_lora_sdxl.py","r") as file:
        lines=file.readlines()
    with open("06_gpu_and_ml/dreambooth/dumpling_lora_sdxl_new.py","w") as file:
        for line in lines:
            if line.startswith("    checkpoint_dir: str"):
                file.write(f'    checkpoint_dir: str="{new_dir}"\n')
            else:
                file.write(line)



def send_request_and_save(input_text,output_path):
        curl_command=f"curl -X GET '{base_url}?text={input_text.replace(' ', '%20')}&num_inference_steps=25&guidance_scale=7.5' --output {output_path}"
        subprocess.run(curl_command,shell=True)
        print(f"image saved to {output_path}")



def ckpt_index(checkpoint_dir):
    match=re.search(r'checkpoint-(\d+)',checkpoint_dir)
    if match:
        ckpt_index=match.group(1)
    else:
        ckpt_index="missing_index"
    return ckpt_index




# ---
# main, loop through all checkpoints
# ---

for checkpoint in checkpoint_list:

    checkpoint_index=ckpt_index(checkpoint)
    print(f"checkpoint set to {checkpoint_index}")
    replace_dir(checkpoint)
    command=["modal","serve","06_gpu_and_ml/dreambooth/dumpling_lora_sdxl_new.py"] #update the .py file name accordingly if need
    process=subprocess.Popen(command)
    time.sleep(10)
    
    output_file=f"{output_folder}/{checkpoint_index}.png"
    send_request_and_save(input_text=prompt,output_path=output_file)
    time.sleep(10)
    print(f"terminating FastAPI app for {checkpoint}")
    process.terminate()

    