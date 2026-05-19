import ifcopenshell
import ifcopenshell.util.element

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Получаем все стены
walls = model.by_type("IfcWallStandardCase")

if not walls:
    print("Стены не найдены!")
    exit()

#Выбираем 1 стену
first_wall = walls[0]

print("Исходные данные стены")
print(f"Name: {first_wall.Name}")
print(f"ObjectType: {first_wall.ObjectType}")

#Изменяем имя стены
old_name = first_wall.Name if first_wall.Name else "Без имени"
first_wall.Name = f"MODIFIED {old_name}"
print(f"\nИзменено имя: '{old_name}' → '{first_wall.Name}'")

#Функция для создания IFC-значений
def create_ifc_value(model, value):
    if isinstance(value, bool):
        return model.create_entity("IFCBOOLEAN", value)
    elif isinstance(value, str):
        return model.create_entity("IFCLABEL", value)
    elif isinstance(value, (int, float)):
        return model.create_entity("IFCREAL", float(value))
    else:
        return value

#Ищем существующий Pset_WallCommon
wall_common_pset = None
for rel in first_wall.IsDefinedBy:
    if rel.is_a("IFCRELDEFINESBYPROPERTIES"):
        pset = rel.RelatingPropertyDefinition
        if pset.is_a("IFCPROPERTYSET") and pset.Name == "Pset_WallCommon":
            wall_common_pset = pset
            break

if wall_common_pset:
    print(f"\nНайден Pset_WallCommon")
    
    #Ищем свойство IsExternal
    is_external_prop = None
    for prop in wall_common_pset.HasProperties:
        if prop.Name == "IsExternal":
            is_external_prop = prop
            break
    
    if is_external_prop:
        #Изменяем существующее свойство
        old_value = is_external_prop.NominalValue
        new_value = create_ifc_value(model, True)
        is_external_prop.NominalValue = new_value
        print(f"Изменено IsExternal: {old_value} → True")
    else:
        #Создаём новое свойство
        new_prop = model.create_entity("IFCPROPERTYSINGLEVALUE")
        new_prop.Name = "IsExternal"
        new_prop.NominalValue = create_ifc_value(model, True)
        
        properties = list(wall_common_pset.HasProperties)
        properties.append(new_prop)
        wall_common_pset.HasProperties = properties
        print("Добавлено новое свойство IsExternal = True")
else:
    print("\nPset_WallCommon не найден, создаём новый...")
    #Создаём новый Pset
    wall_common_pset = model.create_entity("IFCPROPERTYSET")
    wall_common_pset.GlobalId = ifcopenshell.guid.new()
    wall_common_pset.Name = "Pset_WallCommon"
    
    #Создаём свойство
    new_prop = model.create_entity("IFCPROPERTYSINGLEVALUE")
    new_prop.Name = "IsExternal"
    new_prop.NominalValue = create_ifc_value(model, True)
    wall_common_pset.HasProperties = [new_prop]
    
    #Привязываем Pset к стене
    rel_def = model.create_entity("IFCRELDEFINESBYPROPERTIES")
    rel_def.GlobalId = ifcopenshell.guid.new()
    rel_def.RelatingPropertyDefinition = wall_common_pset
    rel_def.RelatedObjects = [first_wall]
    print("Создан новый Pset_WallCommon с IsExternal = True")

#Сохраняем изменённую модель
new_file_path = r"E:\SnakePupi\python_labor\modified.ifc"
model.write(new_file_path)
print(f"\nФайл сохранён: {new_file_path}")

#Проверяем изменения
print("Проверка в новом файле")

new_model = ifcopenshell.open(new_file_path)

#Находим изменённую стену
for wall in new_model.by_type("IfcWallStandardCase"):
    if wall.GlobalId == first_wall.GlobalId:
        print(f"Название стены: {wall.Name}")
        
        # Проверяем Pset
        psets = ifcopenshell.util.element.get_psets(wall)
        if "Pset_WallCommon" in psets:
            print(f"Pset_WallCommon: {psets['Pset_WallCommon']}")
        break