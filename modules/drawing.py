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
    img_byte_arr = io.BytesIO()

    img_user = Image.open(io.BytesIO(user_photo))

    # Redimensiona a imagem do placar para ter a mesma
    # largura da imagem do usuário

    # TODO seria possível aqui forçar um achatamento da
    # imagem do usuário para deixar nos moldes da boleta
    width, _ = img_user.size
    img = img.resize((width, img.height))

    # Junta as imagens
    new_image = Image.new('RGB', (width, img.height + img_user.height))
    new_image.paste(img, (0, 0))
    new_image.paste(img_user, (0, img.height))

    # Save the image
    new_image.save(img_byte_arr, format='PNG')

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
