from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, status_code = None, detail: str = None):
        super().__init__(status_code=status_code or self.status_code, detail=detail or self.detail)

class UserNotEnoughPrivileges(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У пользователя недостаточно прав"
    
    
class UserPasswordsDoNotMatch(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Введенные пароли не совпадают"


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    
    
class UserIsNotActive(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Ваш аккаунт заблокирован администратором"


class RoomFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"
