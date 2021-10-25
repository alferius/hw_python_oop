from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: int

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {format(self.duration, ".3f")} ч.; '
                f'Дистанция: {format(self.distance, ".3f")} км; '
                f'Ср. скорость: {format(self.speed, ".3f")} км/ч; '
                f'Потрачено ккал: {format(self.calories, ".3f")}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, 
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_COEFF_1: int = 18
    MEAN_SPEED_COEFF_2: int = 20
    LEN_STEP = 0.65

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий."""
        return ((self.MEAN_SPEED_COEFF_1 * super().get_mean_speed()
                - self.MEAN_SPEED_COEFF_2) * self.weight / self.M_IN_KM
                * (self.duration * 60))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_COEFF_1: float = 0.035
    IS_SQUARE: int = 2
    WEIGHT_COEFF_2: float = 0.029
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий."""
        return ((self.WEIGHT_COEFF_1 * self.weight + (super().get_mean_speed()
                 ** self.IS_SQUARE // self.height) * self.WEIGHT_COEFF_2
                 * self.weight) * (self.duration * self.MIN_IN_HOUR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    LEN_STEP: float = 1.38
    MEAN_SPEED_COEFF: float = 1.1
    WEIGHT_COEFF: int = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.MEAN_SPEED_COEFF) 
                * self.WEIGHT_COEFF * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        check_workout = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
        return check_workout[workout_type](*data)
    except KeyError:
        raise Exception('Unknow input sensor')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
