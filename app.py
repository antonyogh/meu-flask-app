from flask import Flask, request, jsonify

app = Flask(__name__)

servicos = [{'id':1,'servico':'Troca de óleo'},
            {'id':2,'servico':'Troca de pastihas'},
            {'id':3,'servico':'Troca de correia dentada'}]

@app.route("/")
def home():
    return jsonify({'status':'Api inicializada','versão':'1.0'})

@app.route('/servicos',methods=['GET'])
def servicos():
    return jsonify({'servicos':servicos})

@app.route('/add',methods=['POST'])
def add():
    if not request.json or not 'id' in request.json or not 'servico' in request.json:
        return jsonify({'message':'Dados inválidos!'}),400
    
    s = {'id': request.json['id'],'servico':request.json['servico']}
    servicos.append(s)
    return jsonify({'message':'Servico inserirdo!','servico':s}),201

if __name__ == "__main__":
    app.run()
    