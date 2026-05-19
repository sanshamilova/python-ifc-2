import ifcopenshell 

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Получение этажей
storeys = model.by_type("IfcBuildingStorey")
# walls
# doors
# window

#Вывод схемы IFC
print("Схема IFC:", model.schema)

#Количество этажей
print("Количество этажей:", len(storeys))

#Вывод этажа и высотной отметки
for storey in storeys:
    name = storey.Name if storey.Name else "Без имени"
    elevation = storey.Elevation if storey.Elevation is not None else "None (не задана)"
    print(f"Этаж: {name}, Высотная отметка={elevation}")

#Строка-заголовок
print("TITLE: Информация об этажах IFC-модели")