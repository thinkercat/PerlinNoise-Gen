import noise, random, os, json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

# Perlin noise settings
scale = 18.0
octaves = 2
persistence = 2.5
lacunarity = 1.5

seed = random.randint(0,10000*10000)
def get_noise(x,y):
    value = noise.pnoise3(x / scale,
        y / scale,
        seed,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=x,
        repeaty=y,
        base=0)
    
    return value

def color_scale(type:str,value):
    c = int((value+1) * 128)
    c = max(0,min(255,c))
    if type == 'world':
        if c < 10:
            color = (29, 53, 87)
        elif c < 100:
            color = (69, 123, 157)
        elif c < 110:
            color = (168, 218, 220)
        elif c < 120:
            color = (254, 250, 224)
        elif c < 150:
            color = (96, 108, 56)
        elif c < 170:
            color = (40, 54, 24)
        elif c < 200:
            color = (188, 184, 177)
        elif c < 230:
            color = (70, 63, 58)
        else:
            color = (244, 243, 238)     
    else:
        color = (c,c,c)

    return color

def save(w=100, h=100):
    # Create images
    img = Image.new('RGB', (w,h), 255)
    img2 = Image.new('RGB',(w,h), 255)
    for x in range(w):
        for y in range(h):
            value = get_noise(x,y)

            img.putpixel((x, y),color_scale('world',value))
            img2.putpixel((x, y),color_scale('',value))
    
    # Save files
    dt_save = datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")
    path = f'renders/{dt_save}/'

    os.makedirs(os.path.dirname(path), exist_ok=True)

    img.save(f'{path}world.png')
    img2.save(f'{path}grey.png')

    data = {"seed":seed,
            "scale":18.0,
            "octaves": 2,
            "persistence":2.5,
            "lacunarity":1.5 }
    
    js_data = json.dumps(data)
    with open(f'{path}properties.json','w') as f:
        f.write(js_data)
        print(f"file save as in {path}")



class App():
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("2D Perlin Noise")

        self.content = ttk.Frame(self.root)
        self.content.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.S))

        self.seed = tk.IntVar()
        self.seed.set(56)
        self.seed_entry = ttk.Entry(self.content,textvariable=self.seed)
        self.seed_entry.grid(column=0,row=1)
        self.seed_newbtn = ttk.Button(self.content,text="New Seed",command=self.newseed)
        self.seed_newbtn.grid(column=1,row=1)


        self.scale = tk.DoubleVar()
        self.scale.set(18.0)
        self.scale_bar = ttk.Scale(self.content,orient='horizontal',length=200,variable=self.scale,from_=0.0, to=100.0)
        self.scale_bar.grid(column=0,row=2)
        self.scale_entry = ttk.Entry(self.content,textvariable=self.scale)
        self.scale_entry.grid(column=1,row=2)
        
        self.octaves = tk.IntVar()
        self.octaves.set(2)
        self.octaves_bar = ttk.Scale(self.content,orient='horizontal',length=200,variable=self.octaves,from_=0, to=10)
        self.octaves_bar.grid(column=0,row=3)
        self.octaves_entry = ttk.Entry(self.content,textvariable=self.octaves)
        self.octaves_entry.grid(column=1,row=3)

        self.persistence = tk.DoubleVar()
        self.persistence.set(2.5)
        self.persistence_bar = ttk.Scale(self.content,orient='horizontal',length=200,variable=self.persistence,from_=0.0, to=10.0)
        self.persistence_bar.grid(column=0,row=4)
        self.persistence_entry = ttk.Entry(self.content,textvariable=self.persistence)
        self.persistence_entry.grid(column=1,row=4)

        self.lacunarity = tk.DoubleVar()
        self.lacunarity.set(1.5)
        self.lacunarity_bar = ttk.Scale(self.content,orient='horizontal',length=200,variable=self.lacunarity,from_=0.0, to=10.0)
        self.lacunarity_bar.grid(column=0,row=5)
        self.lacunarity_entry = ttk.Entry(self.content,textvariable=self.lacunarity)
        self.lacunarity_entry.grid(column=1,row=5)


        self.render_btn = ttk.Button(self.content,text="render",command=self.makerender)
        self.render_btn.grid(column=3,row=8)

        self.render_canvas = tk.Canvas(self.content,width=500,height=500)
        self.render_canvas.grid(column=3,row=1,columnspan=6,rowspan=6)
        


    def makerender(self):
        canvas = self.render_canvas
        for x in range(canvas.winfo_width()):
            for y in range(canvas.winfo_height()):
                value = self.get_noise(x,y)
                canvas.create_line(x, y,x+1,y,fill=self.color_scale('world',value))
            canvas.update()

    def color_scale(self,type:str,value):
        c = int((value+1) * 128)
        c = max(0,min(255,c))
        if type == 'world':
            if c < 10:
                color = '#1d3557'
            elif c < 100:
                color = '#457b9d'
            elif c < 110:
                color = '#a8dadc'
            elif c < 120:
                color = '#fefae0'
            elif c < 150:
                color = '#606c38'
            elif c < 170:
                color = '#283618'
            elif c < 200:
                color = '#bcb8b1'
            elif c < 230:
                color = '#463f3a'
            else:
                color = '#fef3ee'     
        else:
            color = f'#{hex(c)}{hex(c)}{hex(c)}'

        return color
    def get_noise(self,x,y):
        value = noise.pnoise3(x / self.scale.get(),
                            y / self.scale.get(),
                            self.seed.get(),
                            octaves=self.octaves.get(),
                            persistence=self.persistence.get(),
                            lacunarity=self.lacunarity.get(),
                            repeatx=x,
                            repeaty=y,
                            base=0)
    
        return value
    
    def newseed(self):
        self.seed.set(random.randint(0,10000))
        
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
