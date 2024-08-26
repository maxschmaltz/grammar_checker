Congratulations you have made it this far! This already shows that you are among the top candidates applying for this role. To better understand how you work and think, here is a coding challenge.

You shouldn't spend much more than 2 hours working on it. In case you have any questions, feel free to reach out to us similar to how you would reach out to a teammate.


# Signavio NEXT Challenge: Grammar Checker Backend

## Overview

Your task is to build a backend for a grammar checker using a Language Model (LLM). The backend should be able to receive a text input, process it using the LLM, and return a list of errors found in the text along with their corrections and the type of error.

Use Python and a backend framework of your choice. The backend should expose an API endpoint where text can be uploaded. It returns a list of triplets: wrong sentence, corrected sentence, and type of error.

You can use any LLM of your choice. For instance, [Zephyr 7B](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha) can be run on your own device. It is not particularly important that your approach is highly accurate. A conceptual approach is okay. You can also use OpenAI models but you will have to provide your own API keys.

Make sure to think about the following things

- How will the API be documented?
- How will you test the API? 
- What happens if processing takes long? Can you run the process in the background without blocking the frontend?
- How will you handle errors when the LLM generation fails or is not syntactically correct?
- How do you evaluate your approach? Provide a draft of how your system could be evaluated.
- ... and anything you deem important but is not mentioned here. 

## What's important for us 

- Code Quality: Your code should be clean, easy to understand, and well-documented.
- Error Handling: Your application should be able to handle different types of grammatical errors effectively.
- Performance: Your application should be able to handle long-running requests without blocking the client.
- Choice of Backend Framework and LLM: Your choice of backend framework and LLM should be justified based on the requirements of the task.

## Submission

Please submit your code along with a README file. The README should include:

- Instructions on how to run your code.
- A brief explanation of your design choices and why you made them.
- Any challenges you faced and how you overcame them.
- Any future improvements or additions you would make if you had more time.

🤗 Good luck!