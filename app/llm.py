from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)

print("Model loaded!")


def generate_response(message: str) -> tuple[str, int, int]:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        [text],
        return_tensors="pt",
    ).to(model.device)

    input_tokens = inputs.input_ids.shape[1]

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
    )

    generated_ids = outputs[:, inputs.input_ids.shape[1]:]

    output_tokens = generated_ids.shape[1]

    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0]

    return response, input_tokens, output_tokens
