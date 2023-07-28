# import torch
# from transformers import AutoModel, AutoTokenizer

# def run_language_model(model_path, input_text):
#     # Load the model and tokenizer from a local path
#     model = AutoModel.from_pretrained(model_path, local_files_only=True)
#     tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

#     # Preprocess the input text
#     inputs = tokenizer(input_text, return_tensors="pt")

#     # Run inference
#     with torch.no_grad():
#         outputs = model(**inputs)

#     return outputs

# model_path = '/Users/sudomoniker/Projects/llama/llama-2-7b-chat/consolidated.00.pth'
# input_text = '''Hi, what are you?'''

# outputs = run_language_model(model_path, input_text)
# print(outputs)

import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")