import sys
sys.path.append('pypng-main\code')
import png
import argparse

# Read a png file and return its width, height, rows of rgba and red_pixels
def read_png_file(filepath):
    data = png.Reader(filename=filepath).asRGBA8()
    width = data[0]
    height = data[1]
    rows = list(data[2])
    
    red_pixels = []
    for j in rows:
        for red in range (0, len(j), 4):
            red_pixels.append(j[red])
    return width, height, rows , red_pixels 


# Transforme text to binary
def textToBin(text):
    b = []
    b.append([(bin( ord(c) )[2:].rjust(8, '0')) for c in text])
    return b[0]


# Make all red pixels even 
def adjust_to_even(red_list):
    for i in range(len(red_list)):
        if((int(red_list[i]) % 2) != 0):
            red_list[i] = red_list[i] -1
    return red_list


# Encode by adding binary text to red pixels
def encode(redcolor, textbin):
    bi=''
    for i in textbin:
        for k in i:
            bi = bi + k
    for j in range(0 , len(bi)):
        redcolor[j] = redcolor[j] + int(bi[j])
    return redcolor


# Transforme rows to list of tuple
def adapt_rows(rows):
    pixels_adapted = []
    for row in rows:
        rgba_pixels = tuple(row)
        pixels_adapted.append(rgba_pixels)
    return pixels_adapted


# Replace red pixels by the new one which contain binary
def set_red_pixels(red_list, rows, w, h):
    m = 0
    s = 0
    for i in range(0, h):
        n = 0
        l = list(rows[m])   #convert tuple to list in order to edit it
        for j in range(0, w):
            print(l[n] , red_list[s])
            l[n] = red_list[s] # edit the red value
            n += 4 # index of red pixels
            s += 1
        rows[m] = tuple(l) #insert the list as tuple
        m += 1
    return rows


# Create png file from rows
def generat_png(width, high, final_rows, name):
    w = png.Writer(width, high, greyscale=False, alpha=True)
    f = open(name, 'wb')
    w.write(f, adapt_rows(final_rows))
    f.close()


# Decode function from a png it return full text hidden
def decode (path):
    width, high, rows, red_pixels = read_png_file(path)    
    i = 0
    new_list = []
    # insert every 8 value of red color in list of list
    while i < len(red_pixels):
        new_list.append(red_pixels[i:i+8])
        i += 8
    coded_values=[]
    # cheeck end of texte (first 8 value ever)
    for e in new_list:
        if(any(n % 2 == 1 for n in e)):
            coded_values.append(e) # insert 8 value that contain any unever number
        else:
            break # end of message
    bin_string = ''
    full_text = ''
    for x in coded_values:
        bin_string = bin_string + ''.join(map(str,[item % 2 for item in x])) # concatenate binary
    full_text = ''.join(chr(int(bin_string[i*8:i*8+8],2)) for i in range(len(bin_string)//8)) # binary to string
    return full_text



################## Main Function ##################
if __name__ == "__main__":
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help='image path')
    parser.add_argument("-txt", '--text', help='text to encode')
    parser.add_argument("-out", '--output', help='image and text encoded', type=str)
    args = parser.parse_args()
    
    if args.image and args.text:
         # get image infos
        width, high, rows, red_pixels = read_png_file(args.image)

        # Convert text to binary
        textbin = textToBin(args.text)

        # Adjust red_pixels to get even values
        redPixels_adjusted = adjust_to_even(red_pixels)

        # Encode (red_pixels + binary text) 
        redPixels_adjusted = encode(redPixels_adjusted, textbin)

        # Adpat rows to format (list of tuple)
        rows_adapted = adapt_rows(rows) 

        # Repelace red_pixels by the encoded ones
        final_rows =  set_red_pixels(redPixels_adjusted, rows_adapted, width, high)  

        # Generate image
        generat_png(width, high, final_rows, args.output)
    if args.image  and not args.text:
        # encode image
        print(decode(args.image))