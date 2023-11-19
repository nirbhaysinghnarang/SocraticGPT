import logging
from colorama import Fore, Style
from gpt import GPT

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Question:
    history = set()

    def __init__(self, question):
        self.question = question
        self.answer = None
        logging.info(f"{Fore.MAGENTA}Initialized Question: '{self.question}'{Style.RESET_ALL}")

    def is_atomic(self):
        atomic = GPT.is_question_atomic(self.question)
        logging.info(f"{Fore.CYAN}Checking if question '{self.question}' is atomic: {atomic}{Style.RESET_ALL}")
        return atomic

    def get_sub_questions(self):
        sub_questions = GPT.get_sub_questions(self.question)
        logging.info(f"{Fore.CYAN}Retrieved sub-questions for '{self.question}': {sub_questions}{Style.RESET_ALL}")
        return sub_questions

    def get_answer(self, depth=0, max_depth=5):
        logging.info(f"{Fore.BLUE}Answering question: '{self.question}' at depth {depth}{Style.RESET_ALL}")
        if depth >= max_depth:
            logging.warning(f"{Fore.RED}Max depth {max_depth} reached. Forcing direct answer for question '{self.question}'.{Style.RESET_ALL}")
            self.answer = GPT.answer_atomic(self.question)
            return self.answer
        if self.question in Question.history:
            logging.warning(f"{Fore.RED}Cycle detected for question '{self.question}'. Forcing direct answer.{Style.RESET_ALL}")
            self.answer = GPT.answer_atomic(self.question)
            return self.answer
        Question.history.add(self.question)
        if self.is_atomic():
            logging.info(f"{Fore.GREEN}Question '{self.question}' is atomic. Obtaining base answer.{Style.RESET_ALL}")
            self.answer = GPT.answer_atomic(self.question)
        else:
            subquestions = self.get_sub_questions()
            logging.info(f"{Fore.YELLOW}Question '{self.question}' is not atomic. Subquestions: {subquestions}{Style.RESET_ALL}")
            context_answers = []
            for question in subquestions:
                logging.info(f"{Fore.BLUE}Answering sub-question: '{question}' at depth {depth + 1}{Style.RESET_ALL}")
                subquestion = Question(question)
                subquestion.get_answer(depth + 1, max_depth)
                context_answers.append(subquestion)
                logging.info(f"{Fore.BLUE}Answered sub-question: '{question}' with answer: '{subquestion.answer}' at depth {depth + 1}{Style.RESET_ALL}")
            self.answer = GPT.answer_question(self.question, context_answers)
        logging.info(f"{Fore.GREEN}Answered main question: '{self.question}' with answer: '{self.answer}' at depth {depth}{Style.RESET_ALL}")
        return self.answer
