from typing import NamedTuple


# configurado para funcionar com Anchor="mm"
class FieldDimensions(NamedTuple):
    maxWidth: int
    maxHeight: int
    x: int
    y: int


simplesDimensions = {
    "TENISTA_1": FieldDimensions(440, 69, 616, 190),
    "TENISTA_2": FieldDimensions(440, 69, 616, 315),
    "CAT_1": FieldDimensions(86, 77, 951, 192),
    "CAT_2": FieldDimensions(86, 77, 951, 315),
    "PLACAR_1": FieldDimensions(245, 130, 594, 603),
    "PLACAR_2": FieldDimensions(245, 130, 594, 837),
    "TIEBREAK_1": FieldDimensions(140, 130, 888, 603),
    "TIEBREAK_2": FieldDimensions(140, 130, 888, 837),
    "LOCAL": FieldDimensions(530, 68, 674, 994)
}

duplasDimensions = {
    "DUPLA_1": FieldDimensions(384, 47, 357, 123),
    "DUPLA_2": FieldDimensions(384, 47, 357, 205),
    "CAT_1": FieldDimensions(57, 50, 604, 126),
    "CAT_2": FieldDimensions(57, 50, 685, 126),
    "CAT_3": FieldDimensions(57, 50, 604, 200),
    "CAT_4": FieldDimensions(57, 50, 685, 200),
    "PLACAR_1": FieldDimensions(98, 94, 388, 395),
    "PLACAR_2": FieldDimensions(98, 94, 391, 548),
    "TIEBREAK_1": FieldDimensions(98, 94, 582, 395),
    "TIEBREAK_2": FieldDimensions(98, 94, 584, 548),
    "LOCAL": FieldDimensions(355, 50, 441, 650)  # 196
}

torneioSimplesDimensions = {
    "TORNEIO": FieldDimensions(67, 66, 490, 51),
    "TENISTA_1": FieldDimensions(385, 45, 438, 124),
    "TENISTA_2": FieldDimensions(385, 45, 438, 206),
    "CAT_1": FieldDimensions(53, 53, 685, 130),
    "CAT_2": FieldDimensions(53, 53, 685, 203),
    "PLACAR_SET1_TEN1": FieldDimensions(98, 95, 389, 395),
    "PLACAR_SET1_TEN2": FieldDimensions(98, 95, 392, 548),
    "PLACAR_SET2_TEN1": FieldDimensions(98, 95, 584, 395),
    "PLACAR_SET2_TEN2": FieldDimensions(98, 95, 584, 548),
    "TIEBREAK_1": FieldDimensions(98, 95, 783, 396),
    "TIEBREAK_2": FieldDimensions(98, 95, 783, 549),
    "LOCAL": FieldDimensions(420, 48, 474, 650)
}
