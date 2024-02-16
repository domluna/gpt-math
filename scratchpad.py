from openai import OpenAI
import random
import openai
import fire
import pandas as pd
from time import time
import tqdm
import pathlib
from prompts import SCRATCHPAD_MESSAGE


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


def send_message(client: openai.OpenAI, num1: int, num2: int) -> int:
    prompt = f"{num1} + {num2} = "

    kwargs = dict(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": SCRATCHPAD_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=4096,
    )

    completion = client.chat.completions.create(**kwargs)
    print(completion.usage)
    out = completion.choices[0].message.content
    print("Scratchpad output:")
    print(out)

    # find the part of the message that is
    # Final result: <final result>
    out = out.split("Final result: ")[1].strip()
    print("Got:", out)
    print("Expected:", num1 + num2)

    return int(out)


def addition_experiment(n: int, k1: int, k2: int):
    """
    n: int - the number of random addition problems to generate
    k: int - the number of digits in the random numbers to add
    """
    key = load_api_key()
    client = OpenAI(api_key=key)

    nums = [(random_bigint(k1), random_bigint(k2)) for _ in range(n)]
    results = []

    start_time = time()
    for a, b in tqdm.tqdm(nums):
        print(f"Adding {a} and {b}")
        out = send_message(client, a, b)
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
        / f"scratchpad_addition_experiment_{n}_{k1}_{k2}.csv"
    )
    print("Writing to", output_file)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    fire.Fire(addition_experiment)
