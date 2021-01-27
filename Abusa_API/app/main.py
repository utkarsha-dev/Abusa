from flask import Flask, request, jsonify
from flask_cors import CORS
from Model.tflite_inference import Processor
from Model.load_abuse import abuse
import _thread

files = {}
file_num = 0

app = Flask(__name__)
path = "/app/Model/"
p = Processor(model_path=path + "model.tflite", tokenizer_path=path + "tokenizer.pickle")
CORS(app)

def thread_process(data, file_name):
    global files
    print ("Thread Started")
    r = p.get_prediction(data)
    print ("Thread Completed")
    files[file_name][0] = 1
    files[file_name].append(r)

@app.route('/')
def infer():
    return "Tested", 200
 
@app.route('/getAbusiveData')
def bad_words():
    return abuse, 200

@app.route('/modelData', methods = ['POST'])
def data_recieve():
    global files, file_num
    data = request.get_json(force=True)
    files["file" + str(file_num)] = 0
    _thread.start_new_thread(thread_process, (data, 'file' + str(file_num)))
    files['file' + str(file_num)] = [0]
    file_num += 1
    
    return {"threadnum": 'file' + str(file_num - 1)}, 200

@app.route('/getModelOutput')
def get_data():
    global files
    data = request.args.get("threadnum", None)
    if data == None:
        return {"response": "Bad Request"}, 200
    elif files.get(data, None) == None:
        return {"response": "Bad Request"}, 200
    elif files[data][0] == 0:
        return {"response": "Unfinished"}, 200
    else:
        sendData = files[data][1]
        del files[data]
        return {"response": "success", "data": sendData}

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)