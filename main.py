import datetime
from flask import Flask, request
from flasgger import Swagger

from grammar_checker.grammar_checker import GrammarChecker

app = Flask(__name__)
checker = GrammarChecker()


@app.route("/check", methods=['GET'])
def check():

	"""
	---
	description: Check the input text for grammatical errors.
	parameters:
        - in: query
          name: text
          schema:
            type: string
          description: input text to check
	responses:
		200:
			description: success
			schema:
				type: object
				properties:
					status:
						type: integer
						description: The HTTP status code of the request.
						example: 200
					content:
						type: array
						description: JSON string with the main content of the response; it is list of four-place dictionaries with the original sentence, it's corrected (if necessary) version, type of grammatical error, and the reasoning
						items:
							type: object
							properties:
							original_sentence:
								type: string
								description: The original sentence provided in the request.
								example: "Hello World"
							corrected_sentence:
								type: string
								description: The corrected version of the original sentence.
								example: "Hello, World!"
							error_type:
								type: string
								description: The type of grammatical error detected.
								example: "Punctuation"
							reasoning:
								type: string
								description: The reasoning behind the correction.
						example: '[{"corrected_sentence": "Hello, World!", "error_type": "Punctuation", "original_sentence": "Hello World", "reasoning": "The sentence lacks a comma and an exclamation mark to make it a complete sentence."}]'
					timecode:
						type: string
						description: The time at which the response was generated.
						example: "Mon, 26 Aug 2024 18:12:32 GMT"
		400:
			description: bad request
			schema:
				type: object
				properties:
					status:
						type: integer
						description: The HTTP status code indicating the type of error.
						example: 400
					content:
						type: string
						description: error description
						example: '"exec_error": "Empty text"'
	"""

	text = request.args.get("text")

	if not text or not text.strip():
		return {
			"status": 400,
			"content": {
				"exec_error": "Empty text"
			},
			"timecode": datetime.datetime.now()
		}
	
	outputs = checker.check(text)
	# here, we can postprocess content depending on errors
	# ...
	return {
			"status": 200,
			"content": outputs,
			"timecode": datetime.datetime.now()
		}


docs = Swagger(app)