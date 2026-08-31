from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


print("Chargement du tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Chargement du modèle...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)

print("Modèle chargé !")


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    },
    {
        "role": "user",
        "content": "Explique-moi simplement ce qu'est Docker.",
    },
]


text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

model_inputs = tokenizer(
    [text],
    return_tensors="pt",
).to(model.device)


generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=200,
)


generated_ids = [
    output_ids[len(input_ids):]
    for input_ids, output_ids in zip(
        model_inputs.input_ids,
        generated_ids,
    )
]


response = tokenizer.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)[0]


print("\n========== QWEN ==========\n")
print(response)
