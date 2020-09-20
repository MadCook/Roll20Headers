import argparse
from PIL import Image, ImageFont, ImageDraw
import textwrap


parser = argparse.ArgumentParser()
parser.add_argument("phrase", help ='Required Text')
parser.add_argument("-f", "--font", help='Overridden font')
parser.add_argument("-fd", "--fontDirectory",
                    help='Directory Location of font')
parser.add_argument("-m", "--max", help='Max width', type=int)
parser.add_argument("-s", "--size", help='Font size', type=int)
parser.add_argument("-c", "--color", help='Font Color')
args = parser.parse_args()


def setDefaults(args):
    defaults = {
        'save-directory': 'created_images/',
        'font-directory' : '/home/madcook/fonts/warenhaus-typenhebel/',#'/home/madcook/fonts/',
        'font' : 'Warenhaus-Standard.ttf',#'Celtica/Celtica-Book.ttf',
        'size' : 40,
        'max_width' : 20,
        'text': args.phrase,
        'color': (255,255,255),
        'line_space': 12,
        'alignment': 'center'
        }
    if args.font:
        defaults['font'] = args.font
    if args.fontDirectory:
        defaults['font-directory'] = args.fontDirectory
    if args.max:
        defaults['max_width'] = args.max
    if args.size:
        defaults['size'] = args.size
    if args.color:
        defaults['color'] = args.color
    if '.txt' in defaults['text']:
        f = open(defaults['text'], "r")
        defaults['wrapped_text'] = f.read()
    else:
        defaults['wrapped_text'] = inputNewlines(defaults.get('text'),
                                             defaults.get('max_width'))

    return defaults

def inputNewlines(txt, max_width):
    brokenLines = textwrap.wrap(txt, max_width)
    return '\n'.join(brokenLines)

defaults = setDefaults(args)

# Base size of image go large then cut down
image = Image.new('RGBA', (500,500), (255, 255, 255, 0))

# Draw object
draw_layer = ImageDraw.Draw(image)

#Font object
font = ImageFont.truetype(defaults.get('font-directory')+defaults.get('font'),
                          defaults.get('size'))


draw_layer.multiline_text((0,0), defaults.get('wrapped_text'),
                          defaults.get('color'), font=font,
                          spacing=defaults.get('line_space'),
                          align=defaults.get('alignment'))
size = draw_layer.multiline_textsize( defaults.get('wrapped_text'), font=font,
                              spacing=defaults.get('line_space'))
print(size)
image = image.crop((0,0,size[0],size[1]+defaults.get('line_space')))
print(image.size)
image.save(defaults.get('save-directory')+defaults.get('wrapped_text')[0:8]+'.png',"PNG")
image.show()
