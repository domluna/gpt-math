# GPT Math

the purpose of these experiments is to determine how well gpt4 can add two integers of arbitrary size. GPT4 is used because it's the most capable model.

## Notes

Difficult to return single tokens, i.e. "1", "1", "5" instead of "115", even with a large logit bias towards single tokens. ~15 a shift begins to occur, but prior to that 3 digit tokens are still selected. My hypothesis why this is the case is that GPT learns to use 2 or 3 digit tokens for almost everything numerical and then only uses single tokens when they will be followed by a non-digit token.

This plays a bit when the logit bias for the eot token is increased as well. However, the eot token itself is not important, we could use any token as the eot token, for example 'X', and then inform the model through the system prompt this is the new eot token. The results are the same.

If the logit bias for the eot token is not increased then single digit tokens are returned until the max token limit is reached. So we need to increase the logit bias for the eot token as well. The problem then becomes the model favors creating 1-2 total digits and then returning the eot token, even for a large number where that's clearly nowhere near the correct answer.

It could be that because GPT is thinking in a much larger space ~990 possible outcomes (all 3 digit and 2 digit tokens) that the quality degrades.

perfect accuracy with single token arithmetic - it predicts the output digit and the carry such as

9 + 3 - digit: 2, carry: 1

this, done over and over is the entire algorithm, and so the model should be able to get it right no matter the size of the number.
