import ifcopenshell 
import ifcopenshell.util.element

#Путь к файлу
file_path = r"E:\SnakePupi\python_labor\Example_1.ifc"

model = ifcopenshell.open(file_path)

#Количество стен
walls = model.by_type("IfcWall")
print("Число стен:", len(walls))

#Информация о 1 стене
first_wall = walls[0]
print(first_wall)

psets = ifcopenshell.util.element.get_psets(first_wall)

print(psets)

for pset_name, props in psets.items():
    print("Pset:", pset_name)
    for prop_name, value in props.items():
        print("  ", prop_name, "=", value)