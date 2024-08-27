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

		# NVIDIA-hosted models of choice have pretty much the same interface as ChatOpenAI
		llm = ChatNVIDIA(
			model=llm_name,
			nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
			temperature=0,	# ensure reproducibility
			max_tokens=1024
		)

		# this fixing parser with first try to parse the output with the
		# underlying parser (JSON parser over `SentenceAnalysis` in our case)
		# and will retry to fix invalid JSON with an LLM in case the first
		# parsing(s) fail(s)
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
		
	async def acheck(self, sents: List[str]) -> Awaitable[List[Dict[str, str]]]:
		# in this implementation, the text is processed sentence-wise for a couple of reasons:
		#	1. convenience of asynchronous processing
		#	2. if something fails with one sentence, other still get processed
		tasks = [self._acheck_sentence(sent) for sent in sents]
		outputs = await asyncio.gather(*tasks)	# async loop
		return outputs

	def check(self, text: str) -> List[Dict[str, str]]:
		sents = split_text(text)
		outputs = asyncio.run(self.acheck(sents))
		return outputs