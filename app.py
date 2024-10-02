from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            descricao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/transacao', methods=['POST'])
def add_transaction():
    data = request.json
    tipo = data.get('tipo')
    valor = data.get('valor')
    descricao = data.get('descricao')
    
    if not tipo or not valor or not descricao:
        return jsonify({'error': 'Dados incompletos!'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO transacoes (tipo, valor, descricao) VALUES (?, ?, ?)',
                 (tipo, valor, descricao))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Transação adicionada com sucesso!'}), 201

@app.route('/transacoes', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    transacoes = conn.execute('SELECT * FROM transacoes').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in transacoes])

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)
