# GPT Math

the purpose of these experiments is to determine how well gpt4 can add two integers of arbitrary length.

## Output token size

- difficult to return single tokens, i.e. "1", "1", "5" instead of "115". Even with a large bias towards the single tokens it doesn't work. My hypothesis as you why this is the case is that GPT learns to use 2 or 3 digit tokens for almost everything numerical and then only uses single tokens when they will be followed by a non-digit token.
- single tokens are used for the final portion
