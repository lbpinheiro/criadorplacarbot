from modules import constants, functions

initialHandler = [
    "Selecione a categoria do jogo (simples, duplas ou torneio simples)",
    constants.TIPO_INVALIDO,
    functions.validate_tipo,
    "tipo",
    constants.tipoMarkup
]

stateHandler = [
    (
        "Insira o nome do jogador vencedor",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player1",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do jogador vencedor (C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat1",
        constants.catMarkup
    ),
    (
        "Insira o nome do jogador derrotado",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player2",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do jogador derrotado (C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat2",
        constants.catMarkup
    ),
    (
        "Insira o placar do jogo, sempre em referência ao vencedor e apenas "
        "números. Exemplos: 60, 63, 75. Em caso de tiebreak, informe os "
        "pontos do perdedor entre parênteses, exemplos: 76(4), 76(9)",
        "Placar inválido",
        functions.validate_score,
        "score",
        constants.defaultMarkup
    ),
    (
        "Insira o nome do local onde ocorreu o jogo",
        constants.LOCAL_INVALIDO,
        functions.validate_local,
        "local",
        constants.localMarkup
    )
]

stateHandlerDuplas = [
    (
        "Insira o nome do Tenista 1 da dupla vencedora",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player1",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do Tenista 1 da dupla vencedora "
        "(C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat1",
        constants.catMarkup
    ),
    (
        "Insira o nome do Tenista 2 da dupla vencedora",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player2",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do Tenista 2 da dupla vencedora "
        "(C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat2",
        constants.catMarkup
    ),
    (
        "Insira o nome do Tenista 1 da dupla derrotada",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player3",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do Tenista 1 da dupla derrotada "
        "(C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat3",
        constants.catMarkup
    ),
    (
        "Insira o nome do Tenista 2 da dupla derrotada",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player4",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do Tenista 2 da dupla derrotada "
        "(C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat4",
        constants.catMarkup
    ),
    (
        "Insira o placar do jogo, sempre em referência à dupla "
        "vencedora e apenas números. Exemplos: 60, 63, 75. "
        "Em caso de tiebreak, informe os "
        "pontos do perdedor entre parênteses, exemplos: 76(4), 76(9)",
        "Placar inválido",
        functions.validate_score,
        "score",
        constants.defaultMarkup
    ),
    (
        "Insira o nome do local onde ocorreu o jogo",
        constants.LOCAL_INVALIDO,
        functions.validate_local,
        "local",
        constants.localMarkup
    )
]

stateHandlerTorneio = [
    (
        "Insira a categoria do torneio",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "torneio",
        constants.catMarkup
    ),
    (
        "Insira o nome do jogador vencedor",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player1",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do jogador vencedor (C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat1",
        constants.catMarkup
    ),
    (
        "Insira o nome do jogador derrotado",
        constants.JOGADOR_INVALIDO,
        functions.validate_name,
        "player2",
        constants.defaultMarkup
    ),
    (
        "Insira a categoria do jogador derrotado (C, B, A, S ou SS)",
        "Categoria Inválida. As categorias válidas são C, B, A, S ou SS",
        functions.validate_cat,
        "cat2",
        constants.catMarkup
    ),
    (
        "Insira o placar do jogo, sempre em referência ao vencedor e "
        "apenas números, sets divididos por espaço. Se houver terceiro "
        "set (tiebreak de 7 pontos) insira apenas a pontuação do jogador "
        "derrotado. Exemplos: '60 61', '46 75 3', '26 63 4', '76 76', "
        "'75 61', '64 67 2'",
        "Placar inválido",
        functions.validate_score_torneio,
        "score",
        constants.defaultMarkup
    ),
    (
        "Insira o nome do local onde ocorreu o jogo",
        constants.LOCAL_INVALIDO,
        functions.validate_local,
        "local",
        constants.localMarkup
    )
]


def getStateHandler(chat_id, user_info):
    if ("tipo" in user_info[chat_id] and
            user_info[chat_id]["tipo"].upper() == "DUPLAS"):
        return stateHandlerDuplas
    elif ("tipo" in user_info[chat_id] and
            user_info[chat_id]["tipo"].upper() == "TORNEIO SIMPLES"):
        return stateHandlerTorneio
    else:
        return stateHandler
