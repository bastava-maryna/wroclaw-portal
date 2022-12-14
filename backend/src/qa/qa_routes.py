
from flask import Blueprint, request, jsonify
import time
from .model.retriever import Retriever
from .model.reader import Reader

qa_routes = Blueprint("qa_routes", __name__)


@qa_routes.route("/qa", methods=["POST"])
def qa():
    
    st = time.time()
    reader = Reader()
    retriever = Retriever()
    if request.method == "POST":
        query = request.json["question"]     
        # retriever.create_embeddings()
        answers = {}
        results,links = retriever.retrieve_docs(query)

        for num, i in enumerate(results):
            answers[num] = reader.answer_question(query, i)
        
        final_results=[]
        for answer,result,link in zip(answers,results,links):
            answ=answers[answer]['answer']
            score=answers[answer]['score']
            context=result
            ln=link
            elem_dict={ "answer" : answ,
                            "score":score,
                            "context":context,
                            "link":ln}
            final_results.append(elem_dict)

        highest=0
        for elem in final_results:
            if elem["score"]>highest:
                 best=elem
                 highest=elem["score"]
        final_results.pop(final_results.index(best))  
        highest=0
        for elem in final_results:
            if elem["score"]>highest:
                 second=elem
                 highest=elem["score"]
        final_results.pop(final_results.index(second))  
        sorted_final=[best,second,final_results[0]]

        et = time.time()
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')
      
        return jsonify(sorted_final)


