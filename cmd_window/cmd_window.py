from pynput.keyboard import Key, Listener
import threading
from .window import CursesDrawer

current_textbox = 0
drawer = CursesDrawer()

class Window:
    def __init__(self, title: str, sizex: int, sizey: int, boxes: int):
        self.title = title
        self.sizex = sizex
        self.sizey = sizey
        self.boxes = boxes
        self.boxsize = int((sizex - 2) / self.boxes)

    def draw(self):
        if self.boxes == 1:
            output = ("┌" + self.title + "─" * (self.sizex - (len(self.title) + 2)) + "┐\n")
            for i in range(self.sizey - 2): output += ("│" + " " * (self.sizex - 2) + "│\n")
            output += ("└" + "─" * (self.sizex - 2) + "┘")
        else:
            if not self.boxes < self.sizex / 2: raise ValueError("Can't have more boxes than the x size of the window.")
            elif self.boxsize < len(self.title): raise ValueError("Title is too long to fit on a box.")
            else:
                output = ("┌" +
                          ((self.title + "─" * (self.boxsize - len(self.title))) + "┬" + (("─" * self.boxsize) + "┬") * (self.boxes - 2) + ("─" * self.boxsize)) +
                          "┐\n")
                for i in range(self.sizey - 2): output += (("│" + " " * (self.boxsize)) * (self.boxes) + "│\n")
                output += ("└" +
                           (("─" * (self.boxsize) + "┴") * (self.boxes - 1)) +
                           ("─" * (self.boxsize)) +
                           "┘")
        return output
    
class AdvancedWindow:
    def __init__(self, titles:list, sizesx:list[int], sizesy:list[int]):
        self.titles = titles
        self.sizesx = sizesx
        self.sizesy = sizesy
        self.boxesx = len(sizesx)
        self.boxesy = len(sizesy)

    def draw(self):
        for y in range(self.boxesy):
            if y == 0:output = "┌"
            if y != 0:output+="├"
            
            for x in range(self.boxesx):
                if y == 0:
                    if x!=self.boxesx-1:
                        output+=self.titles[y][x]+"─"*(self.sizesx[x]-len(self.titles[y][x]))+"┬"
                    else:
                        output+=self.titles[y][x]+"─"*(self.sizesx[x]-len(self.titles[y][x]))+"┐\n"
                elif y!=0:
                    if x!=self.boxesx-1:
                        output+=self.titles[y][x]+"─"*(self.sizesx[x]-len(self.titles[y][x]))+"┼"
                    else:
                        output+=self.titles[y][x]+"─"*(self.sizesx[x]-len(self.titles[y][x]))+"┤\n"
            for j in range(self.sizesy[y]):
                for i in range(self.boxesx):
                    output +=("│"+(" "*self.sizesx[i]))
                output+="│\n"
            
        output+="└"
        for i in range(self.boxesx-1):
            output +=(("─"*self.sizesx[i])+"┴")
        output+="─"*(self.sizesx[x])+"┘\n"

        return output
    
class Label:
    def __init__(self, text: str, posx: int, posy: int):
        self.text = text
        self.posx = posx
        self.posy = posy

    def draw(self):
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(self.text)+self.posx-1)) + "\n"
        output += ("¤" * (self.posx - 1)) + self.text+ "\n"
        return output

class Textbox:
    def __init__(self, id: int, width: int, posx: int, posy: int, ispassword:bool):
        self.id = id
        self.width = width
        self.text = ""
        self.posx = posx
        self.posy = posy
        self.active = False
        self.ispassword = ispassword

    def keypress(self, key):
        if len(self.text) < self.width:
            if len(str(key)[1:-1]) == 1:
                self.text += str(key)[1:-1]
            elif (str(key)) == "Key.space":
                self.text += " "
        if (str(key)) == "Key.backspace":
            self.text = self.text[:-1]

    def draw(self):
        output = ""
        if self.ispassword:text = (len(self.text)*"*") + "_" * (self.width - len(self.text))   
        else:text = self.text + "_" * (self.width - len(self.text))
        for i in range(self.posy - 1):
            output += ("¤" * (len(text)+self.posx-1)) + "\n"
        if self.active:
            output += ("¤" * (self.posx - 1))+text+"*"+"\n"
        else:
            output += ("¤" * (self.posx - 1))+text+"\n"
        return output

class MultilineTextbox:
    def __init__(self, id: int, width: int, height: int, posx: int, posy: int):
        self.id = id
        self.width = width
        self.height = height
        self.text = ""
        self.posx = posx
        self.posy = posy
        self.active = False
    
    def keypress(self, key):
        if len(self.text) < (self.width*self.height):
            if len(str(key)[1:-1]) == 1:
                self.text += str(key)[1:-1]
            elif (str(key)) == "Key.space":
                self.text += " "
            elif str(key) == "Key.end":
                self.text+=(((int(len(self.text)/self.width)+1)*self.width)-len(self.text))*"¤"

        if (str(key)) == "Key.backspace":
            if self.text[-1] != "¤":
                self.text = self.text[:-1]
            else:
                while self.text[-1] == "¤":
                    self.text = self.text[:-1]

    def draw(self):
        text = self.text+("_"*((self.width*self.height)-len(self.text)))
        output = ""
        for i in range(self.posy - 1): #lines before y position
            output += ("¤" * (self.width+self.posx-1)) + "\n"
        for i in range(0, len(text), self.width): #text assembling
            if i == 0 and self.active: #First line if self.active *
                output += ("¤" * (self.posx-1)) +text[i:i+self.width]+"*"+"\n"
            else:
                output += ("¤" * (self.posx-1)) +text[i:i+self.width]+"\n"
        return output
    
class Button:
    def __init__(self,id, text, command, posx, posy):
        self.id = id
        self.text = text
        self.command = command
        self.posx = posx
        self.posy = posy
        self.active = False

    def press(self):
        if self.command:
            self.command()

    def draw(self):
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(self.text)+self.posx-1)) + "\n"
        if self.active:
            output += ("¤" * (self.posx - 2))+"*"+self.text+"*"+"\n"
        else:
            output += ("¤" * (self.posx - 1)) +self.text+"\n"
        return output

class Checkbox:
    def __init__(self,id:int, text:str, posx:int, posy:int):
        self.id = id
        self.text = text
        self.posx = posx
        self.posy = posy
        self.value = False
        self.active = False
        self.val = " "

    def press(self):
        self.value = not self.value
    
    def draw(self):
        if self.value:text = "[*] "+self.text
        else:text = "[ ] "+self.text
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(text)+self.posx-1)) + "\n"
        if self.active:
            output += ("¤" * (self.posx - 1)) + text + "*"+"\n"
        else:
            output += ("¤" * (self.posx - 1)) + text + "\n"
        return output

class Progressbar:
    def __init__(self, width:int, value:int, minvalue:int, maxvalue:int, showValue:bool, posx:int, posy:int):
        self.width = width
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.value = value
        self.percentage = ((self.value - self.minvalue) / (self.maxvalue - self.minvalue)) * 100
        self.showValue = showValue
        self.posx = posx
        self.posy = posy
    
    def update(self):
        self.percentage = ((self.value - self.minvalue) / (self.maxvalue - self.minvalue)) * 100
        self.draw()
    
    def draw(self):
        filled = int((self.percentage / 100) * self.width)
        empty = self.width - filled
        if self.showValue:
            text = "["+("=" * filled + "." * empty)+"]" + str(self.percentage)+"%"
        else:
            text = "["+("=" * filled + "." * empty)+"]"
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(text)+self.posx-1)) + "\n"
        output += ("¤" * (self.posx - 1)) + text + "\n"
        return output

class Listbox:
    def __init__(self, id:int, data:list, posx:int, posy:int):
        self.id = id
        self.data = data
        self.posx = posx
        self.posy = posy
        self.current = 0
        self.width=0
        self.value=self.data[self.current]
        self.active=False
        for i in range(len(self.data)):
            if len(self.data[i]) > self.width:self.width = len(self.data[i])
        
    def press(self, key):
        if key == Key.right:
            if self.current+1 < len(self.data):
                self.current += 1
        elif key == Key.left:
            if self.current-1 >= 0:
                self.current -= 1
        self.value = self.data[self.current]

    def draw(self):
        if self.active:
            text = "<"+self.data[self.current]+"."*(self.width-len(self.data[self.current]))+">*"
        else:
            text = "<"+self.data[self.current]+"."*(self.width-len(self.data[self.current]))+">"
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(text)+self.posx)) + "\n"
        output += ("¤" * (self.posx - 1)) + text + "\n"
        return output
    
class Slider:
    def __init__(self, id:int, width:int, minvalue:int, maxvalue:int, step:int, posx:int, posy:int):
        self.id = id
        self.width = width
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.step = step
        self.posx = posx
        self.posy = posy
        self.value = self.minvalue
        self.active = False
    
    def press(self,key):
        if key == Key.right:
            self.value += self.step
            if self.value > self.maxvalue: self.value=self.maxvalue
        elif key == Key.left:
            self.value -= self.step
            if self.value < self.minvalue: self.value=self.minvalue

    def draw(self):
        percentage = (self.value - self.minvalue) / (self.maxvalue - self.minvalue)
        filled = int(self.width * percentage)
        empty = self.width - filled
        if self.active:
            text = "[" + "=" * filled + "-" * empty + "]*"
        else:
            text = "[" + "=" * filled + "-" * empty + "]"
        output = ""
        for i in range(self.posy - 1):
            output += ("¤" * (len(text)+self.posx-1)) + "\n"
        output += ("¤" * (self.posx - 1)) + text + "\n"
        return output

class Table:
    def __init__(self,id, data:list[list], columnheaders:list, columnwidths:list, visiblerows:int, posx:int, posy:int):
        self.id = id
        self.data = data
        self.columnheaders = columnheaders
        self.columnwidths = columnwidths
        self.visiblerows = visiblerows
        self.posx = posx
        self.posy = posy
        self.active = False
        self.current = 0
        
    def scroll(self, key):
        if key == Key.up:
            if self.current-1 >= 0:
                self.current -= 1
        elif key == Key.down:
            if self.current+1 <= len(self.data)-1:
                self.current += 1
        self.draw()

    def draw(self):
        data = self.data[self.current:self.current+self.visiblerows]
        if len(data)<self.visiblerows: 
            for _ in range(self.visiblerows-len(data)):
                data.append("¤"*len(self.columnwidths))
        output = ""
        for i in range(self.posy - 1):
            output += "¤" + "\n"
        output+=("¤" * (self.posx - 1))
        for i in range(len(self.columnheaders)):
            if i != len(self.columnheaders)-1:
                output+="│"+self.columnheaders[i]+"¤"*(self.columnwidths[i]-len(self.columnheaders[i]))
            else:
                if self.active:
                    output+="│"+self.columnheaders[i]+"¤"*(self.columnwidths[i]-len(self.columnheaders[i]))+"│*\n"
                else:
                    output+="│"+self.columnheaders[i]+"¤"*(self.columnwidths[i]-len(self.columnheaders[i]))+"│\n"
        for i in range(len(self.columnheaders)): # Separator for headers
            if i == 0:
                output+=("¤" * (self.posx - 1))+"├"+"─"*(self.columnwidths[i])
            else:
                output+="┼"+"─"*(self.columnwidths[i])
        
        output+="┤\n"
        for i in range(len(data)): # Data rows
            output+=("¤" * (self.posx - 1))
            for x in range(len(self.columnheaders)):
                if x != len(self.columnheaders)-1:
                    output+="│"+data[i][x]+"¤"*(self.columnwidths[x]-len(data[i][x]))
                else:
                    output+="│"+data[i][x]+"¤"*(self.columnwidths[x]-len(data[i][x]))+"│\n"
        return output


class MessageBox:
    def __init__(self):
        pass

def on_release(key, objects, current_textbox):
    if key == Key.page_down:
        current_textbox += 1
    elif key == Key.page_up:
        if current_textbox > 0:
            current_textbox -= 1

    for obj in objects:
        if isinstance(obj, (Textbox, Button, Checkbox, Listbox, Table, Slider, MultilineTextbox)):
            obj.active = False
            if obj.id == current_textbox:
                obj.active = True

    for obj in objects:
        if isinstance(obj, Textbox) and obj.active:
            obj.keypress(key)
        elif isinstance(obj, Button) and obj.active and key == Key.space:
            obj.press()
        elif isinstance(obj, Checkbox) and obj.active and key == Key.space:
            obj.press()
        elif isinstance(obj, Listbox) and obj.active:
            obj.press(key)
        elif isinstance(obj, Table) and obj.active:
            obj.scroll(key)
        elif isinstance(obj, Slider) and obj.active:
            obj.press(key)
        elif isinstance(obj, MultilineTextbox) and obj.active:
            obj.keypress(key)

    draw(objects)
    return current_textbox

def str_to_matrix(text: str) -> list[list[str]]:
    return [list(line) for line in text.splitlines()]

def matrix_to_str(matrix: list[list[str]]) -> str:
    return '\n'.join(''.join(row) for row in matrix)

def manage_layers(layers: list[str]) -> str:
    base = layers[0]
    base_matrix = str_to_matrix(base)
    height = len(base_matrix)
    width = max(len(row) for row in base_matrix)

    for row in base_matrix:
        while len(row) < width:
            row.append("¤")

    for layer in layers[1:]:
        layer_matrix = str_to_matrix(layer)
        for y in range(height):
            for x in range(width):
                if y < len(layer_matrix) and x < len(layer_matrix[y]):
                    if layer_matrix[y][x] != "¤":
                        base_matrix[y][x] = layer_matrix[y][x]

    return matrix_to_str(base_matrix)

def draw(objects):
    layers = []
    for obj in objects:
        layers.append(obj.draw())
    drawer.draw(manage_layers(layers))

def onrelease(key, objects):
    global current_textbox
    current_textbox = on_release(key, objects, current_textbox)
    if key == Key.esc:
        exit()
        return False

def start_curses():
    drawer.start()

def start_listener(objects):
    with Listener(on_release=lambda key: onrelease(key, objects)) as listener:
        listener.join()

def run(objects):
    global current_textbox
    thread = threading.Thread(target=start_curses, daemon=True)
    thread.start()
    draw(objects)
    listener_thread = threading.Thread(target=start_listener, args=(objects,))
    listener_thread.start()