from typing import List, Optional

import nltk
nltk.download('punkt_tab')
nltk.download('punkt')


def split_text(
	text: str,
	language: Optional[str] = "english"
) -> List[str]:
	# a separate function for scalability if we'll want to add some preprocessing
	sent_text = nltk.sent_tokenize(text, language=language)
	return sent_text