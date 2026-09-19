import os
from flask import Flask, render_template, jsonify, request
import psycopg2
from db import get_connection
from status import STATUS_LISTA, CODIGOS_STATUS

app = Flask(__name__)

NOME_ESCOLA = "Escola Pública"   # troque pelo nome da sua escola
TIPOS = ("NOTEBOOK", "TABLET")


@app.route("/")
def index():
    logo = os.path.exists(os.path.join(app.static_folder, "logo.jpeg"))
    return render_template(
        "index.html",
        nome_escola=NOME_ESCOLA,
        status_lista=STATUS_LISTA,
        tem_logo=logo,
    )


@app.route("/equipamentos")
def listar_equipamentos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, tipo, carrinho, numero, serie, equipamento, status, observacao,
               TO_CHAR(atualizado_em, 'DD/MM/YYYY HH24:MI') AS atualizado_em,
               (serie IS NOT NULL
                AND COUNT(*) OVER (PARTITION BY serie) > 1) AS serie_duplicada
        FROM equipamentos
        ORDER BY tipo, carrinho, numero
    """)
    colunas = [col[0] for col in cursor.description]
    equipamentos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(equipamentos)


def _ler_campos(dados):
    """Limpa e valida os campos editaveis. Devolve (campos, erro)."""
    serie = (dados.get("serie") or "").strip().upper()
    if serie in ("", "-"):
        serie = None
    equipamento = (dados.get("equipamento") or "").strip()
    status = (dados.get("status") or "").strip().upper()
    observacao = (dados.get("observacao") or "").strip() or None

    if not equipamento:
        return None, "Informe a marca ou o modelo do equipamento."
    if status not in CODIGOS_STATUS:
        return None, "Status inválido."
    return {"serie": serie, "equipamento": equipamento,
            "status": status, "observacao": observacao}, None


@app.route("/equipamentos", methods=["POST"])
def criar_equipamento():
    dados = request.get_json(silent=True) or {}
    campos, erro = _ler_campos(dados)
    tipo = (dados.get("tipo") or "").strip().upper()
    carrinho = (dados.get("carrinho") or "").strip()
    if not erro and tipo not in TIPOS:
        erro = "Tipo inválido."
    if not erro and not carrinho:
        erro = "Informe o carrinho (local) do equipamento."
    if erro:
        return jsonify({"erro": erro}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # O Nº segue a sequencia do carrinho (maior numero atual + 1)
        cursor.execute("""
            INSERT INTO equipamentos
                (tipo, carrinho, numero, serie, equipamento, status, observacao)
            VALUES (%s, %s,
                    (SELECT COALESCE(MAX(numero), 0) + 1
                     FROM equipamentos WHERE tipo = %s AND carrinho = %s),
                    %s, %s, %s, %s)
            RETURNING id, numero
        """, (tipo, carrinho, tipo, carrinho, campos["serie"],
              campos["equipamento"], campos["status"], campos["observacao"]))
        novo_id, numero = cursor.fetchone()
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({"erro": "Já existe um equipamento com esse número neste carrinho."}), 409
    finally:
        cursor.close()
        conn.close()

    return jsonify({"mensagem": f"Equipamento nº {numero} cadastrado.", "id": novo_id}), 201


@app.route("/equipamentos/<int:equip_id>", methods=["PUT"])
def atualizar_equipamento(equip_id):
    campos, erro = _ler_campos(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE equipamentos
        SET serie         = %s,
            equipamento   = %s,
            status        = %s,
            observacao    = %s,
            atualizado_em = NOW()
        WHERE id = %s
        RETURNING numero
    """, (campos["serie"], campos["equipamento"], campos["status"],
          campos["observacao"], equip_id))
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({"erro": "Equipamento não encontrado."}), 404
    return jsonify({"mensagem": f"Equipamento nº {row[0]} atualizado."})


if __name__ == "__main__":
    app.run(debug=True)
