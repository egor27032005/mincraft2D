from PIL import Image, ImageDraw

def create_stretched_image(input_image_path, output_image_path):
    # Открываем входное изображение
    original_image = Image.open(input_image_path)
    
    # Получаем размеры оригинального изображения
    width, height = original_image.size
    
    # Создаем новое изображение с шириной в три раза больше оригинала
    new_image = Image.new('RGB', (width * 3, height))
    
    # Копируем оригинальное изображение три раза в новое изображение
    new_image.paste(original_image, (0, 0))          # Первое изображение
    new_image.paste(original_image, (width, 0))     # Второе изображение
    new_image.paste(original_image, (width * 2, 0)) # Третье изображение
    
    # Сохраняем новое изображение
    new_image.save(output_image_path)

# Пример использования
# input_image_path = 'assets/Water/water_1.png'  # Путь к входному изображению
# output_image_path = 'assets/Water/water2.png' # Путь для сохранения выходного изображения
# create_stretched_image(input_image_path, output_image_path)


def crop_diagonal(input_image_path, output_image_path):
    original_image = Image.open(input_image_path).convert("RGBA")

    # Получаем размеры оригинального изображения
    width, height = original_image.size

    # Создаем маску с теми же размерами, что и оригинальное изображение
    mask = Image.new('L', (width, height), 0)  # 'L' - режим для градаций серого
    draw = ImageDraw.Draw(mask)

    # Рисуем белый треугольник на маске для создания прозрачной области
    draw.polygon([(0, height), (width, height), (width, 0)], fill=255)

    # Создаем новое изображение с прозрачным фоном
    transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # Применяем маску к оригинальному изображению
    transparent_image.paste(original_image, mask=mask)

    # Сохраняем обрезанное изображение
    transparent_image.save(output_image_path)


# input_image_path = 'assets/Water/water2.png'  # Путь к входному изображению
# output_image_path = 'assets/Water/water3.png'  # Путь для сохранения выходного изображения
# crop_diagonal(input_image_path, output_image_path)


def split_image_into_three(input_image_path, output_image_prefix):
    # Открываем входное изображение
    original_image = Image.open(input_image_path)

    # Получаем размеры оригинального изображения
    width, height = original_image.size

    # Вычисляем ширину каждой части
    part_width = width // 3

    # Создаем три части изображения
    for i in range(3):
        # Определяем координаты для обрезки
        left = i * part_width
        right = left + part_width if i < 2 else width  # Последняя часть захватывает остаток
        box = (left, 0, right, height)

        # Обрезаем изображение
        part_image = original_image.crop(box)

        # Сохраняем обрезанную часть
        part_image.save(f"{output_image_prefix}_part_{i + 1}.png")


input_image_path = 'assets/Water/water4.png'  # Путь к входному изображению
output_image_prefix = 'assets/Water/waters.png'  # Префикс для сохранения выходных изображений
split_image_into_three(input_image_path, output_image_prefix)


def crop_diagonal_to_transparent(input_image_path, output_image_path):
    original_image = Image.open(input_image_path).convert("RGBA")

    # Получаем размеры оригинального изображения
    width, height = original_image.size

    # Создаем маску с теми же размерами, что и оригинальное изображение
    mask = Image.new('L', (width, height), 0)  # 'L' - режим для градаций серого
    draw = ImageDraw.Draw(mask)

    # Рисуем белый треугольник на маске для создания прозрачной области
    draw.polygon([(0, 0), (width, 0), (width, height)], fill=255)

    # Создаем новое изображение с прозрачным фоном
    transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # Применяем маску к оригинальному изображению
    transparent_image.paste(original_image, mask=mask)

    # Обрезаем изображение, оставляя только нижнюю часть
    cropped_image = transparent_image.crop((0, height // 2, width, height))

    # Сохраняем обрезанное изображение
    cropped_image.save(output_image_path)


# Пример использования
# input_image_path = 'assets/Water/water2.png'  # Путь к входному изображению
# output_image_path = 'assets/Water/water4.png'  # Путь для сохранения выходного изображения
# crop_diagonal_to_transparent(input_image_path, output_image_path)