import unicodedata

# ============================================================
# Status possiveis do equipamento (fonte unica para app e importador)
# O campo "codigo" e o valor gravado no banco (CHECK do schema.sql).
# ============================================================
STATUS_LISTA = [
    {"codigo": "COMPLETO",      "rotulo": "Completo",      "disponivel": True,
     "descricao": "À disposição para uso."},
    {"codigo": "FUNCIONAL",     "rotulo": "Funcional",     "disponivel": True,
     "descricao": "À disposição para uso."},
    {"codigo": "EM_ANALISE",    "rotulo": "Em análise",    "disponivel": False,
     "descricao": "Fica com o responsável técnico; havendo peças e ferramentas, o reparo é feito na própria escola."},
    {"codigo": "REPARO",        "rotulo": "Reparo",        "disponivel": False,
     "descricao": "Aparelho enviado para conserto fora do ambiente escolar."},
    {"codigo": "NAO_FUNCIONAL", "rotulo": "Não funcional", "disponivel": False,
     "descricao": "Fora da garantia e sem conserto."},
    {"codigo": "DESAPARECIDO",  "rotulo": "Desaparecido",  "disponivel": False,
     "descricao": "Equipamento furtado."},
]

CODIGOS_STATUS = [s["codigo"] for s in STATUS_LISTA]


def _so_letras(texto):
    """'Em análise' -> 'EMANALISE' (sem acento, espaco ou pontuacao)."""
    sem_acento = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in sem_acento if c.isalpha() and ord(c) < 128).upper()


# 'EM ANÁLISE', 'em analise', 'Não Funcional'... -> codigo do banco
_MAPA = {_so_letras(s["rotulo"]): s["codigo"] for s in STATUS_LISTA}
_MAPA.update({_so_letras(s["codigo"]): s["codigo"] for s in STATUS_LISTA})


def normalizar_status(texto):
    """Devolve o codigo do status ou None se o texto nao for reconhecido."""
    return _MAPA.get(_so_letras(texto))
