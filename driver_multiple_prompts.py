# ---
# this driver iterates through a few selected checkpoints (from multiple volumes), on multiple prompts
# i used this to nail down the best checkpoint across trainings with different hyperparameters
# ---


import os
import subprocess
import time
import re


# ---
# prompts i want to test, store outputs in respective folders
# ---

prompt_list=["A Baroque-style painting of Dumpling the little black cat with golden eyes, lounging regally on a velvet cushion in an ornate, gold-framed room", "Dumpling the little black cat with golden eyes, in a cyberpunk cityscape, perched on a neon-lit rooftop, with glowing holographic billboards in the background", "A whimsical cartoon of Dumpling the little black cat with golden eyes, chasing colorful butterflies in a vibrant meadow, drawn in the style of Studio Ghibli", "A steampunk scene of Dumpling the little black cat with golden eyes, sitting next to intricate, brass gears and machinery, with smoke and warm light filling the workshop", "Dumpling the little black cat with golden eyes, as a character in a magical realism painting, floating through an enchanted forest surrounded by glowing orbs and mystical creatures"]


output_folder_list=["output_images/baroque", "output_images/cyberpunk", "output_images/ghibli", "output_images/steampunk", "output_images/magical"]

for output_folder in output_folder_list:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


# ---
# shortlisted checkpoints and their corresponding volumes
# ---

checkpoint_list = ["/model/checkpoint-270/pytorch_lora_weights.safetensors","/model/checkpoint-170/pytorch_lora_weights.safetensors","/model/checkpoint-180/pytorch_lora_weights.safetensors","/model/checkpoint-190/pytorch_lora_weights.safetensors","/model/checkpoint-120/pytorch_lora_weights.safetensors","/model/checkpoint-130/pytorch_lora_weights.safetensors"]

volume_list = ["v7","v8","v8","v8","v9","v9"]



# ---
# for my personal reference, this is my "control"
# ---
# checkpoint_list=["/model/pytorch_lora_weights.safetensors"]
# volume_list=["v2"]


# ---
# inference URL served by Modal
# ---

base_url="https://dumplingisabeast--dumpling-dreambooth-app-model-web--5c92db-dev.modal.run/"




# ---
# helper functions
# ---

def ckpt_index(checkpoint_dir):
    match=re.search(r'checkpoint-(\d+)',checkpoint_dir)
    if match:
        ckpt_index=match.group(1)
    else:
        ckpt_index="missing_index"
    return ckpt_index




# update file path if need, this is pointing to my old file
def replace_dir(new_dir,new_vol):
    with open("06_gpu_and_ml/dreambooth/dreambooth_app_sdxl.py","r") as file:
        lines=file.readlines()
    with open("06_gpu_and_ml/dreambooth/dreambooth_app_sdxl_new.py","w") as file:
        for line in lines:
            if line.startswith("    checkpoint_dir: str"):
                file.write(f'    checkpoint_dir: str="{new_dir}"\n')
            elif line.startswith('    "dreambooth-finetuning-volume-'):
                base_str='    "dreambooth-finetuning-volume-'
                new_line=f'{base_str}{new_vol}",\n'
                print(new_line)
                file.write(new_line)
            else:
                file.write(line)



def send_request_and_save(input_text,output_path):
        curl_command=f"curl -X GET '{base_url}?text={input_text.replace(' ', '%20')}&num_inference_steps=25&guidance_scale=7.5' --output {output_path}"
        subprocess.run(curl_command,shell=True)
        print(f"image saved to {output_path}")




# ---
# main loop function
# ---


for checkpoint, volume in zip(checkpoint_list,volume_list):

    replace_dir(checkpoint, volume)
    command=["modal","serve","06_gpu_and_ml/dreambooth/dreambooth_app_sdxl_new.py"] # update file path if need, this is pointing to my old file
    process=subprocess.Popen(command)
    time.sleep(10)

    for prompt, output_folder in zip(prompt_list,output_folder_list):
        output_file=f"{output_folder}/{checkpoint_index}.png"
        #output_file=f"{output_folder}/control.png"
        send_request_and_save(input_text=prompt,output_path=output_file)
        time.sleep(10)
    print(f"terminating FastAPI app for {checkpoint}, volume {volume}")
    process.terminate()

    