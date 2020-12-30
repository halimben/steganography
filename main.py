import sys
import os
sys.path.append(os.path.join('pypng-main','code'))
import png
import argparse

# Read a png file and return its width, height, rows and lis of rgba values
def read_png_file(filepath):
    data = png.Reader(filename=filepath).asRGBA8()
    width = data[0]
    height = data[1]
    rows = list(data[2])
    
    list_rgba = []
    for j in rows:
        for color in range (0, len(j)):
            list_rgba.append(j[color])
    return width, height, rows , list_rgba 


# Transforme text to binary
def textToBin(text):
    b = []
    b.append([(bin( ord(c) )[2:].rjust(8, '0')) for c in text])
    return b[0]


# rgba odd values to even 
def adjust_to_even(list_rgba):
    for i in range(len(list_rgba)):
        if((int(list_rgba[i]) % 2) != 0):
            list_rgba[i] = list_rgba[i] -1
    return list_rgba


# Encode by adding binary text to  lowest-weight bits of each channel
def encode(list_rgba, textbin):
    # Adjust rgba_pixels to get even values
    rgba_encoded = []
    rgba_encoded = adjust_to_even(rgba_list)
    binary=''
    # binary concatenate
    for byte in textbin:
        for bit in byte:
            binary = binary + bit
    # Add chanel value with bits
    for j in range(0 , len(binary)):
        rgba_encoded[j] = rgba_encoded[j] + int(binary[j])
    return rgba_encoded

    
# Transforme rows to list of tuple
def adapt_rows(rows, width):
    tmp = []
    tuple_list = []
    for j in range(0, len(rows)):
        tmp.append(rows[j])
        if(len(tmp) == width*4 and j != 0):
            tuple_list.append(tuple(tmp))
            tmp.clear()
    return tuple_list


# Create png file from rows adapted
def generat_png(width, high, final_rows, name):
    w = png.Writer(width, high, greyscale=False, alpha=True)
    f = open(name, 'wb')
    w.write(f, adapt_rows(final_rows, width))
    f.close()


# Decode function from a PNG it return full text hidden
def decode (path):
    width, height, rows, red_pixels = read_png_file(path)    
    i = 0
    new_list = []
    # insert every 8 value of colors in list of list
    while i < len(red_pixels):
        new_list.append(red_pixels[i:i+8])
        i += 8
    coded_values=[]
    # Check end of message (first 8 value all even)
    for e in new_list:
        if(any(n % 2 == 1 for n in e)):
            coded_values.append(e) # insert 8 value that contain any odd number
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
    parser.add_argument("-w", '--write', action='store_true', help='mode write')
    parser.add_argument("-f", '--image', help='image path')
    parser.add_argument("-t", '--text', help='text to encode')
    parser.add_argument('output', help='image and text encoded')
    args = parser.parse_args()
    
    if args.write:
        if args.image and args.text:
            image = args.image
            text = args.text
        else:
            image = input("Enter your PNG path: ") 
            text = input("Enter your text: ") 

        # get PNG infos
        width, height, rows, rgba_list = read_png_file(image)

        # Convert text to binary
        textbin = textToBin(text)
        
        # Encode (red_pixels + binary text) 
        rgba_encoded = encode(rgba_list, textbin)
        
        # Generat new PNG file
        generat_png(width, height, rgba_encoded, args.output)

    if not args.write:
        # encode image
        print(decode(args.output))