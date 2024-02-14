from openai import OpenAI
import random
import math
import openai
import fire
import pandas as pd
from time import time
import tqdm
import pathlib
from prompts import SYSTEM_MESSAGE


def load_api_key():
    with open(".env") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY"):
                return line.split("=")[1].strip()
    return None


def random_bigint(k: int) -> int:
    i = 0
    ret = ""
    while i < k:
        rand = random.randint(0, 9)
        if rand == 0 and i == 0:
            continue
        ret += str(rand)
        i += 1
    return int(ret)


def send_message(
    client: openai.OpenAI, num1: int, num2: int, top_logprobs=0, logit_bias=None
) -> int:
    prompt = f"{num1} + {num2} = "

    kwargs = dict(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    if top_logprobs > 0:
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = top_logprobs

    if logit_bias:
        kwargs["logit_bias"] = logit_bias

    completion = client.chat.completions.create(**kwargs)
    print(completion)
    out = completion.choices[0].message.content

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

    return int(out)


def addition_experiment(n: int, k1: int, k2: int, top_logprobs=0, use_logit_bias=False):
    """
    n: int - the number of random addition problems to generate
    k: int - the number of digits in the random numbers to add
    """
    key = load_api_key()
    client = OpenAI(api_key=key)

    # you need a large bias for the single tokens to outweigh the 3 and 2 digit tokens.
    bias = 20
    logit_bias = {
        "15": bias,  # 0
        "16": bias,  # 1
        "17": bias,  # 2
        "18": bias,  # 3
        "19": bias,  # 4
        "20": bias,  # 5
        "21": bias,  # 6
        "22": bias,  # 7
        "23": bias,  # 8
        "24": bias,  # 9
    }
    logit_bias["100257"] = int(15)  # eot token

    nums = [(random_bigint(k1), random_bigint(k2)) for _ in range(n)]
    results = []

    start_time = time()
    for a, b in tqdm.tqdm(nums):
        print(f"Adding {a} and {b}")
        if use_logit_bias:
            out = send_message(client, a, b, top_logprobs, logit_bias)
        out = send_message(client, a, b, top_logprobs)
        print(f"Got: {out}, {a+b==out}")
        results.append((a, b, out))

    elapsed_time = time() - start_time
    print(f"Total elapsed time: {elapsed_time} seconds")

    # Write outputs to a CSV file with Pandas
    columns = ["input_a", "input_b", "output"]
    df = pd.DataFrame(results, columns=columns)
    output_file = (
        pathlib.Path(__file__).parent
        / "data"
        / f"addition_experiment_{n}_{k1}_{k2}.csv"
    )
    print("Writing to", output_file)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    fire.Fire(addition_experiment)
