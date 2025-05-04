from vllm import LLM, SamplingParams

model = LLM(model="/path-to-model/Qwen3-30B-A3B", tensor_parallel_size=4)
sampling_params = SamplingParams(temperature=0.7, max_tokens=2000)

def build_prompt(history):
    prompt = ""
    for msg in history:
        if msg["role"] == "user":
            prompt += f"<s>[INST] {msg['content']} [/INST]"
        elif msg["role"] == "assistant":
            prompt += f" {msg['content']} </s>"
    return prompt

history = []

while True:
    user_input = input("请输入提示词: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    history.append({"role": "user", "content": user_input})
    prompt = build_prompt(history)
    outputs = model.generate(prompt, sampling_params)
    #print(outputs)
    #response = outputs[0].text.strip()
    response = outputs[0].outputs[0].text
    #print(response)
    print("Assistant:", response)
    history.append({"role": "assistant", "content": response})
