# Generating AI Pictures of My Cat
This is an adaptation from the [DreamBooth example on Modal](https://modal.com/docs/examples/dreambooth_app).

I also have a [Substack writeup](https://soundsofsusurrus.substack.com/p/generating-ai-pictures-of-my-cat) on the process and outputs.

## To run
* Set up a Modal account to run training and inference remotely. And optionally Weights & Biases
* Clone this repository. Navigate to the directory and set up your virtual environment
* Run `pip install modal` to install its python packages, then `modal setup` to authenticate
* Update links in instance_example_urls.txt to point to your training pictures
* Update parts of dumpling_lora_sdxl.py accordingly to train your specific subject
* Run `modal run dumpling_lora_sdxl.py` to start training
* When done, run `modal serve dumpling_lora_sdxl.py` to serve the model on a web endpoint. Copy the web_endpoint URL, add a "\docs" to the end, you should be able to test out different prompts from there
* If you've saved multiple checkpoints during training and want to compare their outputs. Run `python driver.py`
* If you have multiple checkpoints and want to compare them across multiple text prompts, run `python driver_multiple_prompts.py`
