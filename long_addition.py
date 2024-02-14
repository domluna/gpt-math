from openai import OpenAI
import math
import openai
import fire
from time import time
from prompts import LONG_ADDITION_SYSTEM_MESSAGE
import random


def load_api_key():
    with open(".env") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY"):
                return line.split("=")[1].strip()
    return None


def random_bigint(k: int) -> str:
    i = 0
    ret = ""
    while i < k:
        rand = random.randint(0, 9)
        if rand == 0 and i == 0:
            continue
        ret += str(rand)
        i += 1
    return ret


def send_message(
    client: openai.OpenAI, num1: int, num2: int, carry: int, end: bool, top_logprobs=0
):
    prompt = f"{num1} {num2} {carry} {str(end).lower()}"

    kwargs = dict(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": LONG_ADDITION_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    if top_logprobs > 0:
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = top_logprobs

    completion = client.chat.completions.create(**kwargs)
    print(completion)

    if top_logprobs > 0:
        print("Top Logprobs")
        for i, logprob in enumerate(completion.choices[0].logprobs.content):
            ret = f"{i}, Chosen Token = '{logprob.token}'"
            s = []
            for t in logprob.top_logprobs:
                s.append(f"'{t.token}' - {round(math.exp(t.logprob)*100,2)}")
            if s:
                ret += " ... lobprobs: [" + ",".join(s) + "]"
            print(ret)

    out = completion.choices[0].message.content

    # parse "2 1" into 2 and 1
    ret = out.split()
    if len(ret) == 1:
        return {"result": int(ret[0]), "carry": 0}
    return {"result": int(ret[0]), "carry": int(ret[1])}


def addition_experiment(k: int, top_logprobs=0):
    """
    n: int - the number of random addition problems to generate
    k: int - the number of digits in the random numbers to add
    """
    key = load_api_key()
    client = OpenAI(api_key=key)

    num1 = random_bigint(k)
    num2 = random_bigint(k)

    start_time = time()
    carry = 0
    ret = ""
    for i, (a, b) in enumerate(zip(reversed(num1), reversed(num2))):
        end = i == len(num1) - 1
        print(f"Adding digit {i+1} - {a} and {b} with carry {carry}, end={end}")
        out = send_message(client, int(a), int(b), carry, end, top_logprobs)
        result = out["result"]
        carry = out["carry"]
        print(f"Got: {result}, {result} and carry {carry}")
        ret = str(result) + ret

    elapsed_time = time() - start_time
    print(f"Total elapsed time: {elapsed_time} seconds")
    print(f"Num1: {num1}")
    print(f"Num2: {num2}")
    print(f"Output: {ret}")
    print(
        f"Expected: {int(num1) + int(num2)}, Correct: {ret == str(int(num1) + int(num2))}"
    )


if __name__ == "__main__":
    fire.Fire(addition_experiment)
