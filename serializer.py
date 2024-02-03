import json
class QuestionJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                "question": obj.question,
                "answer": obj.answer,
                "sub_questions": [self.default(sub_question) for sub_question in obj.get_sub_questions()]
            }
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def serialize_question(question):
    return json.dumps(question, cls=QuestionJSONEncoder, indent=2)
