# cmd_window
## Description

This Python module makes it easy to create text-based graphical interfaces for various purposes. It includes text boxes, labels, buttons, list boxes, tables, password fields, checkboxes, progress bars, and two types of windows.

## Usage
First of all, you have to import the modul.  
```python 
import cmd_window as cmd
```
Then you need to define an array for the items. The items in this array will be drawn to the screen.

```python 
objects = []
```

The program can be started with the run(objects) function. You have to pass the array which contains all the objects.

```python
cmd.run(objects)
```

All objects you can interact with have an ID value. You can select them by using the Page Up key to decrease and the Page Down key to increase the current ID. The ID cannot be the same, and it is recommended to use an increasing order. Having two objects with the same ID can cause issues.

For objects that have a value that might be used for something (e.g., Textbox), you should define it as a variable.
Some objects use additional keys. You can use the SPACE key to press a button or check a checkbox.
Also, for Listboxes and Tables, you can use the arrow keys to select an item, or change the value of Sliders.

```python 
textbox1 = Textbox(...)
```

Later you can get the value of the textbox like this:
```python 
text = textbox1.text()
```

## All objects

### Window
A basic window where you can set a title and define how many columns it has. However, the size of the columns cannot be customized.
```python
Window(title: str, sizex: int, sizey: int, boxes: int)
```

```
-title: The title of the window
-sizex: The x size of the window
-sizey: Thy y size of the window
-boxes: The number of vertical boxes the -window will be divided into.
```

### Advanced window
An advanced window where you can define how many rows and columns it has, as well as set custom sizes and individual titles for each section.

```python
AdvancedWindow(titles:list, sizesx:list[int], sizesy:list[int], boxesx:int, boxesy:int)
```

```
-titles: An array —possibly 2D— that contains all the titles.
-sizesx: An array that contains the width of each column.
-sizesy: An array that contains the height of each row.
-boxesx: The number of columns.
-boxesy: The number of rows.
```

### Label
A simple text element used to display static information. It cannot be interacted with.

```python
Label(text: str, posx: int, posy: int)  
```
```
-text: Text of the label  
-posx: The x position of the label  
-posy: The y position of the label  
```
### Button
A clickable element that displays custom text and can be activated using the SPACE key.

```python
Button(id:int, text:str, command, posx:int, posy:int)
```

```
-id: The id of the button.
-text: The text of the button.
-command: The function that should be called when pressed
-posx: The x position of the button.
-posy: The y position of the button.
```
### Textbox
An input field that allows the user to enter text. It can also be a password field, where the entered characters are hidden. The value can be retrieved and used within the program.
```python
Textbox(id:int, width:int, posx:int, posy:int, ispassword:bool)
```

```
-id: The id of the textbox.
-width: The width of the textbox.
-posx: The x position of the textbox.
-posy: The y position of the textbox.
-ispassword: If set to True, the textbox will display "*" characters instead of the entered text, but the value can still be accessed using the .text attribute of the textbox.
```

### Multilinetextbox
An input field that allows the user to enter multiple lines of text. The value can be retrieved and used within the program.  
!Work in progress!
### Listbox
A selectable list of items where the user can choose one option. The selected items can be retrieved and used in the program.  
The value can be retrieved using the .value attribute.

```python
Listbox(id:int, data:list, posx:int, posy:int)
```

```
-id: The id of the listbox.
-data: A list that contains all the options of the listbox.
-posx: The x position of the listbox.
-posy: The y position of the listbox.
```
### Chechbox
A toggleable element that allows the user to select or deselect an option. It has a value of True when checked and False when unchecked.

```python
Checkbox(id:int, text:str, posx:int, posy:int)
```

```
-id: The id of the checkbox.
-text: The text of the checkbox.
-posx: The x position of the checkbox.
-posy: The y position of the checkbox.
```
### Table 
A grid-like structure that displays data in rows and columns. Each cell can contain text or other elements, and values can be retrieved or modified. 
```python
Table(id, data:list[list], columnheaders:list, columnwidths:list, visiblerows:int, posx:int, posy:int, windowx:int, windowy:int)
```

```
-id: The id of the table.
-data: A 2D array that contains the data of the table.
-columnheaders: A list containing the headers of the columns.
-columnwidths: A list containing the widths of the columns.
-visiblerow: The maximum number of visible rows.
-posx: The x position of the table.
-posy: The y position of the table.
-windowx: !!WILL BE REMOVED!!
-windowy: !!WILL BE REMOVED!!
```
### Slider
An input element that allows the user to select a value from a range by sliding a handle. The value can be adjusted using the left and right arrow keys, and it can be retrieved and modified programmatically.

```python
Slider(id:int, width:int, minvalue:int, maxvalue:int, step:int, posx:int, posy:int)
```

```
-id: The id of the slider
-width: The width of the slider that will be drawn.
-minvalue: The minimum value of the slider.
-maxvalue: The maximum value of the slider.
-step: The amount by which the value will increase or decrease.
-posx: The x position of the slider.
-posy: The y position of the slider.
```
## Installation

The module can be downloaded from the github page.
```sh
pip install cmd-window
```
## License
MIT License © 2025 Péter Czeglédy