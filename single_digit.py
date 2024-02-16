from openai import OpenAI
import math
import openai
import fire
import pandas as pd
from time import time
import tqdm
import pathlib
import itertools
from prompts import SYSTEM_MESSAGE


def load_api_key():
    with open(".env") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY"):
                return line.split("=")[1].strip()
    return None


def send_message(client: openai.OpenAI, num1: int, num2: int, top_logprobs=0):
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
    return int(out)


def addition_experiment(top_logprobs=0, repeats=10):
    """
    n: int - the number of random addition problems to generate
    k: int - the number of digits in the random numbers to add
    """
    key = load_api_key()
    client = OpenAI(api_key=key)

    nums = list(itertools.product(range(1, 10), repeat=2))
    outs = []

    start_time = time()
    for _ in range(repeats):
        for a, b in tqdm.tqdm(nums):
            print(f"Adding {a} and {b}")
            out = send_message(client, a, b, top_logprobs)
            print(f"Got: {out}, {a+b==out}")
            outs.append((a, b, out))

    elapsed_time = time() - start_time
    print(f"Total elapsed time: {elapsed_time} seconds")

    # Write outputs to a CSV file with Pandas
    columns = ["input_a", "input_b", "output"]
    df = pd.DataFrame(outs, columns=columns)
    filename = "single_digit.csv"
    output_file = pathlib.Path(__file__).parent / "data" / filename
    print("Writing to", output_file)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    fire.Fire(addition_experiment)
