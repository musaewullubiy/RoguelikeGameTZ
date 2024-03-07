# Тут будут вспомогательные функции

from PIL import Image

# Открываем изображение
image_path = "images/fox.png"
image = Image.open(image_path)

# Размеры кадра анимации
frame_width = 24
frame_height = 16

# Количество кадров в анимации
frames_count = image.width // frame_width

# Итерируемся по кадрам анимации и сохраняем их
for frame_index in range(frames_count):
    # Вырезаем кадр из изображения
    left = frame_index * frame_width
    top = 32
    right = left + frame_width
    bottom = top + frame_height
    frame = image.crop((left, top, right, bottom))

    # Сохраняем кадр в файл
    frame.save(f"images/fox/test/move_{frame_index}.png")