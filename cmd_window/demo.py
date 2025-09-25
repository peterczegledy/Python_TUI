import cmd_window as cmd

cars = []

def add_car():
    cars.append([t1.text, t2.value, t3.text])

window = cmd.AdvancedWindow([["Cars", "Cars table"]],[21, 60], [20])
l1 = cmd.Label("Brand:",2,2)
t1 = cmd.Textbox(1,10,8,2,False)
l2 = cmd.Label("Color:",2,3)
t2 = cmd.Listbox(2,["red","yellow","blue","green"],9,3)
l3 = cmd.Label("Price:",2,4)
t3 = cmd.Textbox(3,10,8,4,False)
b0 = cmd.Button(4, "Add", add_car,3,8)
l4 = cmd.Label("password", 2, 10)
p1 = cmd.Textbox(7,10,2,11,True)
l5 = cmd.Label("Checkbox", 2, 13)
c1 = cmd.Checkbox(8,"Checkbox1", 2, 14)
s1 = cmd.Slider(9, 10, 0, 10, 1, 2, 16)
table1 = cmd.Table(6,cars,["Brand", "Color", "Price"], [10,6,10], 10,41,2)
mtb1 = cmd.MultilineTextbox(5, 16,10,24,2)

objects = [window,l1,l2,l3,t1,t2,t3,b0, mtb1,l4,l5,p1,c1,s1, table1]

cmd.run(objects)