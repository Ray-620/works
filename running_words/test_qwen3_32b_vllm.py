from openai import OpenAI

# Configure client to use local vLLM server
client = OpenAI(
    base_url="http://localhost:8090/v1",
    api_key="sk-tu293*****91" # Remove if no auth is required
)

# Define messages
messages = [
    #{"role": "system", "content": "请写一篇关于[主题]的[文章/报告/演讲稿]，要求[字数/结构/风格]。"},
    {"role": "user", "content": "以[角色]为主角，写一个[类型]故事，包含[情节要素]"},
    #{"role": "user", "content": "中国古代皇帝有哪些？"},
    #{"role": "system", "content": "你是一个擅长逻辑推理的助手，请逐步思考并给出详细分析。"},
    #{"role": "user", "content": "请分析以下问题：为什么量子计算机比经典计算机更快？"},
    #{"role": "user", "content": "请逐步解释量子计算的原理，分步骤说明其与经典计算的区别。"}
]

# Make request
try:
    response = client.chat.completions.create(
        model="Qwen3-32B",  # Matches the model name served by vLLM
        messages=messages,
        max_tokens=32768
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
