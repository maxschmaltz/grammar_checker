import os
import asyncio
import logging
from dotenv import load_dotenv
from typing import Optional, List, Dict, Awaitable

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.output_parsers import OutputFixingParser

from grammar_checker.prompts import analysis_json_parser, CORRECTION_PROMPT
from grammar_checker.utils import split_text

logger = logging.getLogger(__name__)
load_dotenv()	# load environment variables


class GrammarChecker:

	timeout: Optional[float] = 30.0

	def __init__(self, llm_name: Optional[str] = None) -> None:
		
		if not llm_name:
			llm_name = "meta/llama3-8b-instruct"

		llm = ChatNVIDIA(
			model=llm_name,
			nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
			temperature=0,
			max_tokens=1024
		)

		output_parser = OutputFixingParser.from_llm(
			llm=llm,
			parser=analysis_json_parser,
			max_retries=2
		)

		self._correction_chain = CORRECTION_PROMPT | llm | output_parser

	async def _acheck_sentence(self, sent: str) -> Awaitable[Dict[str, str]]:

		try:
			output = await asyncio.wait_for(
				self._correction_chain.ainvoke({"original_sentence": sent}),
				timeout=self.timeout
			)			
			logger.info("Successfully processed", sent)
			return output
		
		except Exception as e:
			# most often errors are OutputParserException, TimeoutException
			logger.error("Error calling correction chain", e)
			# return error to postprocess
			return {
				"sentence": sent,
				"exec_error": str(e),
				"exec_error_type": str(type(e))
			}
		
	async def _acheck(self, sents: List[str]) -> Awaitable[List[Dict[str, str]]]:
		tasks = [self._acheck_sentence(sent) for sent in sents]
		outputs = await asyncio.gather(*tasks)
		return outputs

	def check(self, text: str) -> List[Dict[str, str]]:
		sents = split_text(text)
		outputs = asyncio.run(self._acheck(sents))
		return outputs