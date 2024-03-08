# Тут будут вспомогательные функции

from PIL import Image

def split_image():
    # Открываем изображение
    image_path = "images/slime/slime-animations.png"
    image = Image.open(image_path)

    # Размеры кадра анимации
    frame_width = 32
    frame_height = 32

    # Количество кадров в анимации
    frames_count = 4

    # Итерируемся по кадрам анимации и сохраняем их
    for frame_index in range(frames_count):
        # Вырезаем кадр из изображения
        left = frame_index * frame_width
        top = 0
        right = left + frame_width
        bottom = top + frame_height
        frame = image.crop((left, top, right, bottom))

        # Сохраняем кадр в файл
        frame.save(f"images/slime/test/stand_{frame_index}.png")


def remove_background(input_image_path, output_image_path):
    # Открываем изображение
    image = Image.open(input_image_path)

    # Получаем размеры изображения
    width, height = image.size

    # Создаем новое изображение с прозрачным фоном
    transparent_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Проходим по каждому пикселю и копируем его в новое изображение, если он не является белым
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel != image.getpixel((1, 1)):  # Если пиксель не белый, копируем его
                transparent_image.putpixel((x, y), pixel)

    # Сохраняем результат
    transparent_image.save(output_image_path)


split_image()