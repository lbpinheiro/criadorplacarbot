from PIL import Image, ImageDraw, ImageFont
from modules import dimensions, constants
import copy
import io
import re


def max_font(text, width, height):
    font_size = 10
    past_font = ImageFont.truetype(constants.FONT_FILE_NAME, font_size)
    past_bbox = past_font.getbbox(text)

    while True:
        font = ImageFont.truetype(constants.FONT_FILE_NAME, font_size + 1)
        bbox = font.getbbox(text)
        if bbox[2] - bbox[0] > width or bbox[3] - bbox[1] > height:
            break
        font_size += 1
        past_font = copy.deepcopy(font)
        past_bbox = copy.deepcopy(bbox)

    return past_font, past_bbox


def draw_text(field, text, draw):
    font, bbox = max_font(text, field.maxWidth, field.maxHeight)

    x = field.x
    y = field.y + constants.OFFSET  # + (field.maxHeight - bbox[3])/2
    draw.text((x, y), text, font=font, fill=(0, 0, 0), anchor="mm")


def merge_photos(img, user_photo):
    img_user = Image.open(io.BytesIO(user_photo))

    # Tamanho máximo permitido para a imagem
    max_width = img.height if img.height > img.width else img.width
    max_height = img.width if img.width < img.height else img.height
    if img_user.width > img_user.height:  # Imagem do usuário na horizontal
        if img_user.width > max_height:
            img_user.thumbnail((max_height, max_height), Image.ANTIALIAS)
    else:  # Imagem do usuário na vertical
        if img_user.height > max_width:
            img_user.thumbnail((max_width, max_width), Image.ANTIALIAS)

    # Verificar as dimensões das imagens
    width_placar, height_placar = img.size
    width_user, height_user = img_user.size

    # Verificar se a altura da imagem do usuário é maior que a largura
    if img_user.height > img_user.width:
        # Redimensionar a imagem do usuário para a altura máxima do placar
        img_user.thumbnail((img.width, img.height), Image.ANTIALIAS)

    # Verificar as dimensões das imagens
    width_placar, height_placar = img.size
    width_user, height_user = img_user.size

    # Verificar se a altura da imagem do usuário é maior que a largura
    if height_user > width_user:
        # Criar uma nova imagem com as dimensões combinadas
        new_width = width_placar + width_user
        new_height = max(height_placar, height_user)
        new_image = Image.new('RGB', (new_width, new_height))

        # Colar a imagem do placar no lado esquerdo
        new_image.paste(img, (0, 0))

        # Colar a imagem do usuário no lado direito
        new_image.paste(img_user, (width_placar, 0))
    else:
        # Criar uma nova imagem com as dimensões combinadas
        new_width = max(width_placar, width_user)
        new_height = height_placar + height_user
        new_image = Image.new('RGB', (new_width, new_height))

        # Colar a imagem do placar acima da imagem do usuário
        new_image.paste(img, ((new_width - width_placar) // 2, 0))
        new_image.paste(img_user,
                        ((new_width - width_user) // 2, height_placar))

    # Salvar a nova imagem
    img_byte_arr = io.BytesIO()
    new_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr


def create_image(chat_id, user_info, bot, user_photo=None):
    img = Image.open("ranking.jpg")
    draw = ImageDraw.Draw(img)

    text = user_info[chat_id]["player1"].title()
    draw_text(dimensions.simplesDimensions["TENISTA_1"], text, draw)

    text = user_info[chat_id]["player2"].title()
    draw_text(dimensions.simplesDimensions["TENISTA_2"], text, draw)

    text = user_info[chat_id]["cat1"].upper()
    draw_text(dimensions.simplesDimensions["CAT_1"], text, draw)

    text = user_info[chat_id]["cat2"].upper()
    draw_text(dimensions.simplesDimensions["CAT_2"], text, draw)

    score = user_info[chat_id]["score"]

    text = score[:1]
    draw_text(dimensions.simplesDimensions["PLACAR_1"], text, draw)

    text = score[1:2]
    draw_text(dimensions.simplesDimensions["PLACAR_2"], text, draw)

    if len(score) > 2:
        match = re.search(r"\((\d+)\)", score)
        tie2 = int(match.group(1))
        tie1 = 7

        if tie2 > 5:
            tie1 = tie2 + 2

        # tiebreak 1
        text = str(tie1)
        draw_text(dimensions.simplesDimensions["TIEBREAK_1"], text, draw)

        # tiebreak 2
        text = str(tie2)
        draw_text(dimensions.simplesDimensions["TIEBREAK_2"], text, draw)

    # local
    text = user_info[chat_id]["local"].upper()
    draw_text(dimensions.simplesDimensions["LOCAL"], text, draw)

    img_byte_arr = None
    if user_photo is not None:
        img_byte_arr = merge_photos(img, user_photo)
    else:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')

    img_byte_arr.seek(0)
    bot.send_photo(chat_id=chat_id, photo=img_byte_arr)


def create_image_duplas(chat_id, user_info, bot, user_photo=None):
    img = Image.open("ranking-duplas.jpg")
    draw = ImageDraw.Draw(img)

    text = user_info[chat_id]["player1"].title() + \
        "/" + user_info[chat_id]["player2"].title()

    draw_text(dimensions.duplasDimensions["DUPLA_1"], text, draw)

    text = user_info[chat_id]["player3"].title() + \
        "/" + user_info[chat_id]["player4"].title()

    draw_text(dimensions.duplasDimensions["DUPLA_2"], text, draw)

    text = user_info[chat_id]["cat1"].upper()
    draw_text(dimensions.duplasDimensions["CAT_1"], text, draw)

    text = user_info[chat_id]["cat2"].upper()
    draw_text(dimensions.duplasDimensions["CAT_2"], text, draw)

    text = user_info[chat_id]["cat3"].upper()
    draw_text(dimensions.duplasDimensions["CAT_3"], text, draw)

    text = user_info[chat_id]["cat4"].upper()
    draw_text(dimensions.duplasDimensions["CAT_4"], text, draw)

    score = user_info[chat_id]["score"]

    text = score[:1]
    draw_text(dimensions.duplasDimensions["PLACAR_1"], text, draw)

    text = score[1:2]
    draw_text(dimensions.duplasDimensions["PLACAR_2"], text, draw)

    if len(score) > 2:
        match = re.search(r"\((\d+)\)", score)
        tie2 = int(match.group(1))
        tie1 = 7

        if tie2 > 5:
            tie1 = tie2 + 2

        # tiebreak 1
        text = str(tie1)
        draw_text(dimensions.duplasDimensions["TIEBREAK_1"], text, draw)

        # tiebreak 2
        text = str(tie2)
        draw_text(dimensions.duplasDimensions["TIEBREAK_2"], text, draw)

    # local
    text = user_info[chat_id]["local"].upper()
    draw_text(dimensions.duplasDimensions["LOCAL"], text, draw)

    img_byte_arr = None
    if user_photo is not None:
        img_byte_arr = merge_photos(img, user_photo)
    else:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')

    img_byte_arr.seek(0)
    bot.send_photo(chat_id=chat_id, photo=img_byte_arr)


def create_image_torneio(chat_id, user_info, bot, user_photo=None):
    img = Image.open("torneio-simples.jpg")
    draw = ImageDraw.Draw(img)

    text = user_info[chat_id]["torneio"].upper()
    draw_text(dimensions.torneioSimplesDimensions["TORNEIO"], text, draw)

    text = user_info[chat_id]["player1"].title()
    draw_text(dimensions.torneioSimplesDimensions["TENISTA_1"], text, draw)

    text = user_info[chat_id]["player2"].title()
    draw_text(dimensions.torneioSimplesDimensions["TENISTA_2"], text, draw)

    text = user_info[chat_id]["cat1"].upper()
    draw_text(dimensions.torneioSimplesDimensions["CAT_1"], text, draw)

    text = user_info[chat_id]["cat2"].upper()
    draw_text(dimensions.torneioSimplesDimensions["CAT_2"], text, draw)

    score = user_info[chat_id]["score"].strip().split()

    text = score[0][:1]
    draw_text(
        dimensions.torneioSimplesDimensions["PLACAR_SET1_TEN1"],
        text,
        draw
    )

    text = score[0][1:2]
    draw_text(
        dimensions.torneioSimplesDimensions["PLACAR_SET1_TEN2"],
        text,
        draw
    )

    text = score[1][:1]
    draw_text(
        dimensions.torneioSimplesDimensions["PLACAR_SET2_TEN1"],
        text,
        draw
    )

    text = score[1][1:2]
    draw_text(
        dimensions.torneioSimplesDimensions["PLACAR_SET2_TEN2"],
        text,
        draw
    )

    if len(score) > 2:
        tie2 = int(score[2])
        tie1 = 7

        if tie2 > 5:
            tie1 = tie2 + 2

        # tiebreak 1
        text = str(tie1)
        draw_text(
            dimensions.torneioSimplesDimensions["TIEBREAK_1"],
            text,
            draw
        )

        # tiebreak 2
        text = str(tie2)
        draw_text(
            dimensions.torneioSimplesDimensions["TIEBREAK_2"],
            text,
            draw
        )

    # local
    text = user_info[chat_id]["local"].upper()
    draw_text(
        dimensions.torneioSimplesDimensions["LOCAL"],
        text,
        draw
    )

    img_byte_arr = None
    if user_photo is not None:
        img_byte_arr = merge_photos(img, user_photo)
    else:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')

    img_byte_arr.seek(0)
    bot.send_photo(chat_id=chat_id, photo=img_byte_arr)
