from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
import json

class GPT:
    DEFAULT_SYSTEM_PROMPT = """\
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\
        """
    LLM = ChatOpenAI(temperature=0.0, openai_api_key="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")        
    
    @classmethod
    def get_sub_questions(cls, query):
        prompt = PromptTemplate.from_template("""{deflt} 
        You are a researcher.
        Your goal is to come up with semantically 
        distinct questions the answers 
        to which will aid in constructing the answers to
        the following question. Make sure the answers
        have no semantic or historical overlap with the following question:{query}.
        Return your answer as a JSON list with the key `sub_questions`.
        Sort these questions in order of relevance to the original question.
        """)
        prediction= cls.LLM.predict(prompt.format(deflt=cls.DEFAULT_SYSTEM_PROMPT, query=query))
        return list(json.loads(prediction)["sub_questions"])[:2]


    @classmethod
    def is_question_atomic(cls, query):
        prompt = PromptTemplate.from_template("""{deflt}
        You are a researcher.
        Your goal is to answer whether the below question
        is an atomic question or not. For added context,
        an atomic question is a question whose total answer
        does not depend on the answering of several sub-questions
        or any additional context. Return your answer 
        only as True or False, returning True if it is an atomic question,
        and false otherwise. Here is the question: {query}
        """)
        prediction = cls.LLM.predict(prompt.format(deflt=cls.DEFAULT_SYSTEM_PROMPT, query=query))
        return prediction.lower() =='true'

    @classmethod
    def answer_question(cls,question, answered_sub_qs):
        prompt = PromptTemplate.from_template("""{deflt}
        You are a researcher. Answer this question, with the given subquestions
        and their respective answers as context.
        {answered_sub_qs}
        This is the question
        {question}
        """)

    
        
        answered_sub_qs_string = ""
        for q in answered_sub_qs:
            answered_sub_qs_string += (q.question + ":" + q.answer + "\n")


        formatted = prompt.format(deflt=cls.DEFAULT_SYSTEM_PROMPT, answered_sub_qs=answered_sub_qs_string, question=question)
        print("\n\n\n"+formatted+"\n\n\n")

        return cls.LLM.predict(formatted)

        
    @classmethod
    def answer_atomic(cls, question):
        prompt = PromptTemplate.from_template("""{deflt}
        You are a researcher. Answer this question.
        This is the question
        {question}
        """)
        return cls.LLM.predict(prompt.format(deflt=cls.DEFAULT_SYSTEM_PROMPT, question=question))

        