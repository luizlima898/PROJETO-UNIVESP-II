from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Configuração da conexão com o MySQL
db_config = {
    'user': 'root',
    'password': 'mavinga898',
    'host': 'localhost',
    'database': 'estoque',
}

# Função para estabelecer a conexão com o banco de dados
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Rota para a página inicial (exibição de produtos)
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', produtos=produtos)
    
# Rota para inserir os dados na tabela MySQL
@app.route('/inserir', methods=['POST'])
def inserir():
    data = request.get_json()
    nome = data.get("nome")
    estoque = data.get("estoque")
    local = data.get("local")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO estoque (nome, estoque, local) VALUES (%s, %s, %s)"
        val = (nome, estoque, local)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "sucesso", "mensagem": "Produto inserido com sucesso!"}), 201
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# Rota para pesquisar produtos

@app.route('/pesquisar', methods=['GET'])
def pesquisar_produto():
    termo = request.args.get('termo')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # <- assim cada linha vira dict {coluna: valor}
    sql = "SELECT * FROM estoque WHERE nome LIKE %s"
    val = (f'%{termo}%',)
    cursor.execute(sql, val)
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(produtos=produtos, termo=termo)
    

    
# Rota para buscar os dados da tabela no MySQL
@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT codigo, nome, estoque, local FROM estoque"
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)  # Retorna os dados no formato JSON
    except Exception as e:
        return jsonify({'error': str(e)})
        cursor.close()
        conn.close()
               
@app.route('/atualizar', methods=['POST'])
def atualizar():
    db_config = {
        'user': 'root',
        'password': 'mavinga898',
        'host': 'localhost',
        'database': 'estoque',
}
    try:
        # Dados recebidos do HTML (via fetch ou formulário)
        dados = request.get_json()
        id_registro = dados.get("codigo")
        novo_nome = dados.get("nome")
        novo_estoque = dados.get("estoque")
        novo_local = dados.get("local")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "UPDATE estoque SET nome = %s, estoque = %s, local = %s WHERE codigo = %s"
        cursor.execute(sql, (id_registro, novo_nome, novo_estoque, novo_local))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "mensagem": "Registro atualizado com sucesso!"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})
        
        
if __name__ == '__main__':
    app.run(debug=True)
        






