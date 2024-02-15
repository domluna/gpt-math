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

this works!

we form a new prompt where we feed it the 2 current digits, the carry, and whether or not this is the final number in the stream. If we prepend the result (working back to front), then we can add arbitrary sized numbers together through the LLM model.

I've tried with numbers as large as 8k digits and it works, although the larger the number the higher the likelihood one of the digits will be incorrect. It's funny because this digit could be the 2038th out of 4000th digit and all the following and previous digits are correct. I'm not sure why this happens but it may be systematic error. Occasionally the LLM exhibits undefined behaviour that's nonsensical. For example when doing single digit arithmetic this was the output:


```
Adding 6 and 6
ChatCompletion(id='chatcmpl-8ryantwyD1mZ33swIu1pkUSYYbNnt', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content="2 astro2020.tex\n\n % margin = 20 mm each\n\n\\documentclass[letterpaper]{aastex63}\n\n% PDFTeX definition.\n\\ifx\\undefined\\PdfTeX\\relax\\else\n  \\newcommand{\\degdot}{.}\\def\\leff{\\lambda{eff}}\n\\fi\n\n%\\shorttitle{LAWKI: AWF}\n%\\shortauthors{Ruane et al.}\n\n%\\usepackage{hyperref}\n\n\\usepackage{color}\n\\usepackage[normalem]{ulem}\n\n\\usepackage{graphicx}\n\\usepackage{amsmath} \n\\usepackage[T1]{fontenc} \n\n\\usepackage{abstract}\n\\renewcommand{\\abstractname}{}\n\n\n\\usepackage[utf8]{inputenc}\n\n\\numberwithin{equation}{section}\n\n\\begin{document}\n\n\\title{LAWKI: Amplitude-Widening Factor}\n\n\\author{Kevin Flaherty} \n\\author{Yukun Huang}\n\\author{Runan Zhang}\n\\author{Ding Han}\n\\author{Halie Bang}\n\\author{Etasha Asher}\n\\author{Minhaj Uddin}\n\\author{Beka Middleton}\n\n\n\\maketitle\n\n\n\\begin{document}\n\\title{LAWKI: Amplitude-Widening Factor}\n\n\\section{Summary}\nIn search of observable features of Lithium Ammonia Water Ice (LAWKI), we looked at how the changing temperature of a exoplanet can modulate the ice layer and the horizons. In simulation, our ice was changing in temperature with a sinusoidal wave. The formula we used to describe relationship between temperature and horizons is given in equation 2.2. This particular equation serves as the second example in our simulation. Our numerical solver plots the temperature variation with horizons. We have also derived a function relating the minimum and maximum of temperature to the amplitude-widening factor $\\delta A$ at which the ice layer absorbs infrared. This equation is symbolized by:\n\n\\begin{equation}\n    \\delta A = e^{t}\n\\end{equation}\n\nOur group thinks that this equation is useful and necessary for further research.\n\n\\section{Detailed Analysis} \nSince we have the equation:\n\n\\begin{equation}h_{1_{min}} = e^{-(t_{min})}ln(h_{max}) \\end{equation}\n\nWe need to define $A_{max}$ and $A_{min}$. Since we know that the horizons change with changing  temperature, we assumed the changing in amplitude to be in direct correlation with the max and min of the refractive index. Thus the difference is give by $\\delta A = A_{max}-A_{min}$. Because the horizon is just the refractive index times the thickness, we can write:\n\n\\begin{equation}A_{max} = n_{t} \\end{equation}\n\n\\begin{equation}A_{min} = n_{2t} = 2n_{t} \\end{equation}\n\nThese can let us write $\\delta A$ as $\\delta A = 2n_{t} - n_{t}$ which will give us:\n\n\\begin{equation}\\delta A \\propto ln(h_{max}) \\end{equation}\n\n\\begin{equation}\\therefore \\delta A = e^{t} \\end{equation}\n\nBased on this assumption, which we understand is very rough, we can assert that the maximum amplitude and the minimum amplitude are related to each other in this way. \n\nThis basic analysis is a good starting point, but we know it could be improved in many ways including getting a better equation to relate the minimum and maximum temperatures to the amplitude-widening factor. Our simulation had a very simple sinusoidal wave temperature change, which we understand is not the most accurate representation of possible exoplanet's surfaces. \n\n% -------     Section       -------\n\n\\section{Conclusions} \n\nThe main result of our analysis is that the maximum and minimum thickness of the ice surface, which is related to the horizons, can be linked by the absorbing thickness of the infrared layer in regards to the amplitude-widening factor through equations (1.1) and (2.4). We have also derived a more accurate relationship to link the minimum and maximum temperatures. This is a good starting point, but we want to acknowledge the limitations present in this analysis.\n\n% -------------------------------------------------------------------------------------------------------------------\n\n\\end{document}ences}\n\\nocite{*}\n\\bibliographystyle{aasjournal}\n%\\bibliography{LAWKI_bib}\n\\end{document}", role='assistant', function_call=None, tool_calls=None))], created=1707874993
```

If I were to run the same prompt again I would get the expected result. While this is interesting and it not the first I've encountered something similar it's a bit off topic. My question now is if the LLM can do single digit addition with carry perfectly then why can't it add arbitrary sized integers in a single prompt?

Further thoughts:

1-3 digit addition is not the issue. Any combinations of 1, 2, 3 digit pairings works.

Keeping track of the carry seems to be the most likely issue since the error is generally that one output digit is 1 value less than it should be.

When adding two numbers of differing sizes the order plays a big role. "LHS + RHS". When the larget number is LHS the accuracy greatly improves. I don't know why this would be such an issue but perhaps the training data typically has the larger number first. Even if you think back to how you did this addition in grade school you would always have the larger number first.

```
    123
   +  4

   vs.

      4
   +123
```

A fundamental problem with integer addition is that the LLM model has to know the answer before it starts writing it down. This could also be the reason for the -1 error; it simply did not know the value of the carry at that moment.

Integer arithmetic provides an insightful look into how an LLM works. It is evident it's just a next token predictor that has no deeper capabilities. Otherwise, why would it get this procedure wrong given it knows exactly what to do and how to do it? It's the holy grail of shakesperean monkeys.
