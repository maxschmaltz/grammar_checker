import datetime
from flask import Flask, request

from grammar_checker.grammar_checker import GrammarChecker

app = Flask(__name__)
checker = GrammarChecker()


@app.route("/check", methods=['GET'])
def check():

	text = request.args.get('text')

	if not text.strip():
		return {
			"status": 400,
			"content": {
				"exec_error": "Empty text"
			},
			"timecode": datetime.datetime.now()
		}
	
	outputs = checker.check(text)
	return {
			"status": 200,
			"content": outputs,
			"timecode": datetime.datetime.now()
		}