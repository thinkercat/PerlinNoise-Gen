import noise, random, os, json
from PIL import Image
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

def save(w, h):
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




if __name__ == '__main__':
    save(200,200)