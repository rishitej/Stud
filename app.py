import openai
from gpt import GPT
from gpt import Example
from flask import Flask,request, jsonify

openai.api_key='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'

gpt = GPT(engine="davinci", temperature=0.5, max_tokens=100)

gpt.add_example(Example('Fetch unique values of DEPARTMENT from Worker table.',
                        'Select distinct DEPARTMENT from Worker;'))
gpt.add_example(Example('Print the first three characters of FIRST_NAME from Worker table.',
                        'Select substring(FIRST_NAME,1,3) from Worker;'))
gpt.add_example(Example("Find the position of the alphabet ('a') in the first name column 'Amitabh' from Worker table.",
                        "Select INSTR(FIRST_NAME, BINARY'a') from Worker where FIRST_NAME = 'Amitabh';"))
gpt.add_example(Example("Print the FIRST_NAME from Worker table after replacing 'a' with 'A'.",
                        "Select CONCAT(FIRST_NAME, ' ', LAST_NAME) AS 'COMPLETE_NAME' from Worker;"))
gpt.add_example(Example("Display the second highest salary from the Worker table.",
                        "Select max(Salary) from Worker where Salary not in (Select max(Salary) from Worker);"))
gpt.add_example(Example("Display the highest salary from the Worker table.",
                        "Select max(Salary) from Worker;"))
gpt.add_example(Example("Fetch the count of employees working in the department Admin.",
                        "SELECT COUNT(*) FROM worker WHERE DEPARTMENT = 'Admin';"))
gpt.add_example(Example("Get all details of the Workers whose SALARY lies between 100000 and 500000.",
                        "Select * from Worker where SALARY between 100000 and 500000;"))
gpt.add_example(Example("Get Salary details of the Workers",
                        "Select Salary from Worker"))

app = Flask(__name__)

@app.route('/get_code', methods=['POST'])
def find_answer():
    prompt = request.files['prompt'].read().decode("utf-8")
    print(prompt)
    response = gpt.get_top_reply(prompt)
    ans=response.split('output:')[1].strip()
    resp = jsonify({'code':ans})
    resp.status_code = 400
    return resp

if __name__=='__main__':
    app.run(debug=True)
