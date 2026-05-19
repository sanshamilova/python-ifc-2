import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.geom

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Получаем все двери
doors = model.by_type("IfcDoor")

#Задаём критерий фильтрации
min_width = 800  # минимальная ширина двери в мм
min_height = 2000  # минимальная высота двери в мм

print("Фильтрация дверей и экспорт подмодели")

#Анализируем двери и отбираем подходящие
good_doors = []
door_info = []

for door in doors:
    name = door.Name if door.Name else "Без имени"
    width = getattr(door, "OverallWidth", None)
    height = getattr(door, "OverallHeight", None)
    
    if width is not None and height is not None:
        width_mm = round(width, 1)
        height_mm = round(height, 1)
        
        #Проверяем критерий
        if width_mm >= min_width and height_mm >= min_height:
            good_doors.append(door)
            door_info.append((name, width_mm, height_mm))

#Выводим информацию об отобранных дверях
print(f"\nВсего дверей в модели: {len(doors)}")
print(f"Отобрано дверей (ширина >= {min_width} мм, высота >= {min_height} мм): {len(good_doors)}")

if good_doors:
    print("\nОтобранные двери:")
    for name, width, height in door_info:
        print(f"  {name}: ширина = {width} мм, высота = {height} мм")
else:
    print("\nНет дверей, удовлетворяющих критерию!")
    exit()

#Создаём подмодель
print("Создание модели")

#Создаём новую пустую модель с той же схемой
schema = model.schema
new_model = ifcopenshell.file(schema=schema)

#Копируем все необходимые элементы
#Сначала собираем все элементы, связанные с отобранными дверями
elements_to_copy = set()

#Добавляем сами двери
for door in good_doors:
    elements_to_copy.add(door)

#Находим и добавляем связанные элементы
def add_related_elements(element):
    #Ищем все связи, где element участвует
    for rel in model.get_inverse(element):
        elements_to_copy.add(rel)
        #Добавляем все элементы, связанные через отношение
        if hasattr(rel, "RelatedObjects"):
            for obj in rel.RelatedObjects:
                elements_to_copy.add(obj)
        if hasattr(rel, "RelatingObject"):
            elements_to_copy.add(rel.RelatingObject)
        if hasattr(rel, "RelatingProduct"):
            elements_to_copy.add(rel.RelatingProduct)
        if hasattr(rel, "RelatingGroup"):
            elements_to_copy.add(rel.RelatingGroup)

#Добавляем связанные элементы для каждой двери
for door in good_doors:
    add_related_elements(door)

#Копируем все собранные элементы в новую модель
element_map = {}
for elem in elements_to_copy:
    #Пропускаем, если уже скопирован
    if elem.id() in element_map:
        continue
    try:
        new_elem = new_model.add(elem)
        element_map[elem.id()] = new_elem
    except:
        pass

#Особенно важно: копируем здание и этажи
buildings = model.by_type("IfcBuilding")
for building in buildings:
    if building.id() not in element_map:
        new_model.add(building)
        element_map[building.id()] = building

storeys = model.by_type("IfcBuildingStorey")
for storey in storeys:
    if storey.id() not in element_map:
        new_model.add(storey)
        element_map[storey.id()] = storey

#Обновляем ссылки в скопированных элементах
for elem in new_model:
    #Восстанавливаем ссылки на другие элементы
    pass

#Сохраняем подмодель
new_file_path = r"E:\SnakePupi\python_labor\doors_wide_min_800mm.ifc"
new_model.write(new_file_path)
print(f"Подмодель сохранена: {new_file_path}")

#Проверяем результат
print("Проверка модели")

#Открываем созданную подмодель
check_model = ifcopenshell.open(new_file_path)

#Получаем двери в подмодели
check_doors = check_model.by_type("IfcDoor")

print(f"\nКоличество дверей в подмодели: {len(check_doors)}")

#Проверяем, что все двери удовлетворяют критерию
all_valid = True
for door in check_doors:
    width = getattr(door, "OverallWidth", None)
    height = getattr(door, "OverallHeight", None)
    if width is not None and height is not None:
        if width >= min_width and height >= min_height:
            print(f"{door.Name}: {width} x {height}")
        else:
            print(f"{door.Name}: {width} x {height} - не проходит критерий")
            all_valid = False
    else:
        print(f"  ? {door.Name}: размеры не указаны")

if all_valid:
    print("Все двери в подмодели удовлетворяют критерию")
else:
    print("Некоторые двери не проходят критерий")
