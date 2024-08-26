from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from grammar_checker.format_instructions import get_json_format_instructions


class SentenceAnalysis(BaseModel):
	original_sentence: str = Field(..., description="Original sentence")
	corrected_sentence: str = Field(..., description="Corrected sentence")
	error_type: str = Field(..., description="The type of the error")
	reasoning: str = Field(..., description="Reasoning of why it is an error")

analysis_json_parser = JsonOutputParser(pydantic_object=SentenceAnalysis)


CORRECTION_INSTRUCTIONS = """\
Check if the original sentence below has grammatical errors and correct the sentence if necessary.\
Correct only grammatical errors and ignore the others. Describe the error type in few words.\
If there are multiple errors, list errors in the order of their appearance.
Provide a short one-sentence reasoning of why you think it is a mistake.

{format_instructions}


Example
=====
Original sentence: "I have two dog"
Analysis:
```
{{
	"original_sentence": "I have two dog.",
	"corrected_sentence": "I have two dogs.",
	"error_type": "Number agreement",
	"reasoning": "The word 'two' requires the dependant noun to be plural."
}}
```

Your actual task
=====
Original sentence: "{original_sentence}"
Analysis:
"""


# since the task does not presuppose chatting (and thus message history),
# a simple prompt will suffice
CORRECTION_PROMPT = PromptTemplate.from_template(
	CORRECTION_INSTRUCTIONS,
	partial_variables={"format_instructions": get_json_format_instructions(SentenceAnalysis)}
)