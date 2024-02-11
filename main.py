from openai import OpenAI
import math
import random
import tiktoken

def load_api_key():
    with open('.env') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY'):
                return line.split('=')[1].strip()
    return None

def random_bigint(k: int) -> str:
    return ''.join([str(random.randint(0, 9)) for _ in range(k)])

key = load_api_key()
client = OpenAI(api_key=key)

# tokens are from cl100k_base encoding
# ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
tokens = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
logit_bias = {f"{k}": 10 for k in tokens} # bias for these tokens over tokens that map to 3 digit strings

enc = tiktoken.get_encoding('cl100k_base')
# bad_tokens = []
# bad_tokens = enc.encode_batch(list(map(str, range(10, 1000))))
# for t in bad_tokens:
#     logit_bias[str(t[0])] = -100

# Define your prompt here
prompt = f"70290091967294948856565911246006 + 45618277827721751796872019133876 = "
system_message = "You are an arithmetic assistant that can add arbitrary long integers with ease. You are given an expression of the form 'number1 + number2 = '. Return the answer itself only. Do not add any preamble. Do not use multiple digit tokens."

completion = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt}
  ],
    logit_bias=logit_bias,
    logprobs=True,
    top_logprobs=2,
)
completion.choices[0].message.content


for (i, logprob) in enumerate(completion.choices[0].logprobs.content):
    ret = f"{i}, Chosen Token = '{logprob.token}'"
    s = []
    for t in logprob.top_logprobs:
        s.append(f"'{t.token}' - {round(math.exp(t.logprob)*100,2)}")
    if s:
        ret += " ... lobprobs: [" +  ','.join(s) + "]"
    print(ret)
