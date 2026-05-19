import ifcopenshell 

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Количество стен
walls = model.by_type("IfcWall")
print("Число стен:", len(walls))
