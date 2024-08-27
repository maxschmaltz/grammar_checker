## LLM-Based Grammar Checker

### Quickstart

The app exposes a local API endpoint under `http://127.0.0.1:5000` and receives a single argument: text. The text gets checked for grammatical errors sentence-wise and for each sentence, returns a four-place dictionary with the original sentence, corrected sentence (if necessary), the type of the error, and a reasoning of why it is an error. The output is formatted as a JSON string. The corresponding functionality is available under `/check`.

**Example**

Run the query with `curl` in bash or directly in the browser: 

```bash
curl 'http://127.0.0.1:5000/check?text=Hello%20World'
```

Output (formatted here for readability):

```json
{
	"content":[
		{
			"corrected_sentence": "Hello, World!",
			"error_type": "Punctuation",
			"original_sentence": "Hello World",
			"reasoning":"The sentence lacks a comma and an exclamation mark to make it a complete sentence."
		}
	],
	"status": 200,
	"timecode": "Tue, 27 Aug 2024 12:21:35 GMT"
}
```


### Tech Stack

* LLM. As the baseline model, Llama3.1 8B Instruct was chosen. This model gives a great balance between computational costs and the quality of output. It is lightweight and (should be) optimized for efficiency on one hand, but is simultaneously quite powerful in language understanding and following instructions. The model is hosted on NVIDIA servers and is inferenced via API calls.

* Orchestration. I chose LangChain as one of the most popular and powerful frameworks for LLM-based stuff, which provides seamless creation of the pipeline.

* Backend framework. The project is a simple I/O pipeline which has just one purpose: receive a text and output the result. Therefore, backend must pretty much serve this purpose and can thus be super lightweight. I chose Flask because it allows for providing all the required backend functionality in a couple of string of code. It is nevertheless functional enough to be scalable, so there won't be a need to move to another framework in the scenario where the project evolves and need to be run in prod. As a bonus, it helps maintain clean and simple docu with Swagger.

* Last but not least, the whole processing runs asynchronously which 1) simplifies the (hypothetical) streaming functionality, and 2) doesn't block the server if something goes wrong with a single sentence.


### Challenges

* Research. I spent some time researching and picking right model and backend framework based on the requirements of the assignment.

* LLM inference. To ensure sufficient quality from the start, I needed a more or less powerful model that would be fine-tuned to follow instructions and could generate a valid JSON. Moreover, in the scenario of rapid development (in only a couple of hours) I needed to be familiar with the model because different models react differently to different prompts and some models require a certain format; in other words I couldn't risk experimenting so I laid off the idea with Zephyr 7B right away. So did I with OpenAI models because they are costly. Luckily, I found out recently that as a member of NVIDIA Developer Program, I have an access to NVIDIA-hosted LLMs, among which are Llamas which satisfy both quality and cost constrains. The solution is also scalable because one can request an enterprise license.

* The most challenging part for me was the async workflow. It was trivially rusty with me :) But some research and AI did their job and I got that part alright.


### Future Improvements

My implementation is a baseline so I left many things only on paper.

* Caching.

* Streaming. In the current implementation, even though it runs asynchronously, the output is still waited for and then sent as a whole. So from the point of view of a user, it is still pretty much synchronous. This baseline though allows for a pretty quick switch that will stream the sentences as they are ready to be sent.

* Demo-app. I usually wrap small showcases into simple Streamlit apps, kind of MVPs, but I'd need another 1-2h for that.

* Parameters: users like to play around with different models, temperatures, parameters etc. even though they might not always understand what this is :)

* Adjusting the language.

* Evaluation. Unlike abstract generation, grammatical error detection is (almost fully) deterministic so it can use strict metrics that can be calculated based only on the outputs, given some gold standard. In English, the model can be run over the [FCE dataset](https://paperswithcode.com/dataset/fce) so we can calculate accuracy and such. A wrong sentence can indeed be corrected in multiple ways but (intuitively) it is still deterministic enough to not need to use LLM-based evaluation approaches (like Ragas and analogues).

* Load testing (?)