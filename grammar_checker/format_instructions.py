from typing import Dict, Any
import json

from langchain_core.pydantic_v1 import BaseModel


JSON_FORMAT_INSTRUCTIONS = """\
The output should be a well-formatted JSON instance that strictly conforms to the JSON schema below:

```
{schema}
```

Return only a pure JSON string surrounded by triple backticks (```).\
"""


def remove_title(schema: Dict[str, Any]) -> Dict[str, Any]:
	# recursively remove excessive field "title"
	if isinstance(schema, dict):
		schema.pop("title", None)
		for subschema in schema.values():
			remove_title(subschema)
	return schema


def get_json_format_instructions(pydantic_object: BaseModel) -> str:
	reduced_schema = remove_title(pydantic_object.schema())	# remove excessive fields "title"
	schema_str = json.dumps(reduced_schema)
	json_format_instructions = JSON_FORMAT_INSTRUCTIONS.format(schema=schema_str)
	return json_format_instructions