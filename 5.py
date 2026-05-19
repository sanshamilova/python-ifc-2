import ifcopenshell 

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Получение всех дверей
doors = model.by_type("IfcDoor")

#Порог минимальной ширины
min_width = 800  # 800 мм

#Список для узких дверей
narrow_doors = []

for door in doors:
    name = door.Name if door.Name else "Без имени"
    width = getattr(door, "OverallWidth", None)
    height = getattr(door, "OverallHeight", None)
    
    #Проверка, что размеры есть
    if width is not None and height is not None:
        #Округление размеров
        width_mm = round(width, 1)
        height_mm = round(height, 1)
        
        #Проверка, узкая ли дверь
        if width_mm < min_width:
            narrow_doors.append((name, width_mm, height_mm))
    else:
        #Если размеров нет, вывод предупреждения
        print(f"У двери '{name}' отсутствуют размеры")

#Вывод результата
print("Результат анализа дверей:")
if narrow_doors:
    print(f"\nНайдено узких дверей: {len(narrow_doors)}")
    print(f"Порог минимальной ширины: {min_width} мм\n")
    print("Список узких дверей:")
    for name, width, height in narrow_doors:
        print(f"{name}: ширина = {width} мм, высота = {height} мм")
else:
    print(f"\nУзких дверей не обнаружено (все двери шире {min_width} мм)")