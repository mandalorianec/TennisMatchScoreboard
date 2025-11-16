# from src.exceptions.own_exceptions import ValidationException
#
#
# class Validator:
#     pass
#
#     @staticmethod
#     def validate_player_name(player_name: str, min_len=3, max_len=30):
#         if not isinstance(player_name, str):
#             raise ValidationException("Имя должно быть строкой")
#         player_name = player_name.strip()
#         if len(player_name) < min_len or len(player_name) > 30:
#             raise ValidationException(f"Длина имени должна быть минимум {min_len} и не превышать {max_len}")
#         if not player_name.isalpha():
#             raise ValidationException("Строка должна содержать только буквенные символы")
