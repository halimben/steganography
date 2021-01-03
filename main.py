"""
Name : main.py
Author : Halim BENIKHLEF
Time    : 03/01/2021 20:12
Desc: encode text in png file
"""
import sys
import os
sys.path.append(os.path.join('pypng-main','code'))
import png
import argparse

# Read a png file and return its width, height, rows and lis of rgba values
def read_png_file(filepath):
    '''
    read a png file
            Parameters:
                    filepath (path): a png path
            Returns:
                    width (int): width of the png file
                    height (int): height of the png file
                    list_rgba (list): list of rgba values
    '''
    data = png.Reader(filename=filepath).asRGBA8()
    width = data[0]
    height = data[1]
    rows = list(data[2])
    
    list_rgba = []
    for j in rows:
        for color in range (0, len(j)):
            list_rgba.append(j[color])
    return width, height , list_rgba 


def textToBin(text):
    '''
    convert text to binary
            Parameters:
                    text (str): text to convert
            Returns:
                    b (str): string of binary, each char in one byte
    '''
    b = ''
    b = b.join([(bin( ord(c) )[2:].rjust(8, '0')) for c in text])
    return b


def adjust_to_even(list_rgba):
    '''
    make all values even
            Parameters:
                    list_rgba (list): rgba values
            Returns:
                    list_rgba (list): rgba even values
    '''
    for i in range(len(list_rgba)):
        if((int(list_rgba[i]) % 2) != 0):
            list_rgba[i] = list_rgba[i] -1
    return list_rgba


# Encode by adding binary text to  lowest-weight bits of each channel
def encode(list_rgba, message_bin):
    '''
    encode a message by adding each bit in color value
            Parameters:
                    list_rgba (list): rgba values
                    message_bin (str): string of binary
            Returns:
                    rgba_encoded (list): rgba values + binary string
    '''
    if(len(list_rgba) - 8 < len(message_bin)):
        raise Exception('text too long to encode in png file')
    rgba_encoded = []
    rgba_encoded = adjust_to_even(rgba_list)

    for j in range(0 , len(message_bin)):
        rgba_encoded[j] = rgba_encoded[j] + int(message_bin[j])
    return rgba_encoded

    
def adapt_rows(rgba_encoded, width):
    '''
    adapt rows to reconstitute a png file
            Parameters:
                    rgba_encoded (list): rgba values list
                    width (int): png width
            Returns:
                    tuple_list (list of tuples): format adpated to write
    '''
    tmp = []
    tuple_list = []
    for j in range(0, len(rgba_encoded)):
        tmp.append(rgba_encoded[j])
        if(len(tmp) == width*4 and j != 0):
            tuple_list.append(tuple(tmp))
            tmp.clear()
    return tuple_list


def generat_png(width, height, rgba_encoded, name):
    '''
    Create a png file form the rgba_encoded
            Parameters:
                    width (int): png width
                    height (int): height width
                    rgba_encoded (list): rgba values list                 
            Returns:
                    none
    '''
    w = png.Writer(width, height, greyscale=False, alpha=True)
    f = open(name, 'wb')
    w.write(f, adapt_rows(rgba_encoded, width))
    f.close()


# Decode function from a PNG it return full text hidden
def decode (path):
    '''
    Decode the png file and get cleartext
            Parameters:
                    path (path): png width                 
            Returns:
                    full_text (str): cleartext message
    '''
    width, height, list_rgba = read_png_file(path)    
    i = 0
    new_list = []
    # insert every 8 value of colors in list of list
    while i < len(list_rgba):
        new_list.append(list_rgba[i:i+8])
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
        width, height, rgba_list = read_png_file(image)

        # Convert text to binary
        message_bin = textToBin(text)
        
        # Encode (rgba_pixels + binary text) 
        rgba_encoded = encode(rgba_list, message_bin)
        
        # Generat new PNG file
        generat_png(width, height, rgba_encoded, args.output)

    if not args.write:
        # encode png
        print(decode(args.output))