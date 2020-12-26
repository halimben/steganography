import sys
sys.path.append('pypng-main\code')
import png
import argparse


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



def textToBin(text):
    b = []
    b.append([(bin( ord(c) )[2:].rjust(8, '0')) for c in text])
    return b[0]



def adjust_to_even(list):
    adjusted_list = []
    for i in list:
        if((int(i) % 2) != 0):
            adjusted_list.append(i-1)
        else:
            adjusted_list.append(i)
    return adjusted_list



def encode(redcolor, textbin):
    bi=''
    for i in textbin:
        for k in i:
            bi = bi + k
    for j in range(0 , len(bi)):
        redcolor[j] = redcolor[j] + int(bi[j])
    return redcolor



def adapt_rows(rgba_rows):
    rgba_pixels_list = []
    for row in rgba_rows:
        rgba_pixels = tuple(row)
        rgba_pixels_list.append(rgba_pixels)

    return rgba_pixels_list



def set_red_pixels(red_list, rows, w, h):
    print(rows)
    print('----------')
    #w = 20
    #h = 21
    m = 0
    s = 0
    for i in range(0, h):
        n = 0
        l = list(rows[m])   #convert tuple to list in order to edit it
        for j in range(0, w):
            print(l[n] , red_list[s])
            l[n] = red_list[s] # edit the red value
            #print(l[n] ,'=', red_list[s])
            n += 4 # index of red pixels
            s += 1
        #print('**: ',l)
        rows[m] = tuple(l) #insert the list as tuple
        m += 1
    print(rows)
    return rows



def generat_png(width, high, final_rowsn, name):
    w = png.Writer(width, high, greyscale=False, alpha=True)
    f = open(name, 'wb')
    w.write(f, adapt_rows(final_rows))
    f.close()



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
    
    # Parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help='image path')
    parser.add_argument("-txt", '--text', help='text to encode')
    parser.add_argument("-out", '--output', help='image and text encoded', type=str)
    args = parser.parse_args()
    
    if args.image and args.text:
         # get image infos
        width, high, rows, red_pixels = read_png_file(args.image)

        # convert text to binary
        textbin = []
        textbin = textToBin(args.text)

        # adjust red_pixels to get pair values
        redPixels_adjusted = adjust_to_even(red_pixels)

        # encode (red_pixels + binary text) 
        redPixels_adjusted = encode(redPixels_adjusted, textbin)

        # adpat rows to format (list of tuple)
        rows_adapted = adapt_rows(rows) 

        # insert red_pixels encoded in rows
        final_rows =  set_red_pixels(redPixels_adjusted, rows_adapted, width, high)  

        # generate image
        generat_png(width, high, final_rows, args.output)
    if args.image  and not args.text:
        print(decode(args.image))
    '''

    # get image infos
    width, high, rows, red_pixels = read_png_file('tst.png')

    # convert text to binary
    textbin = []
    textbin = textToBin('halim')

    # adjust red_pixels to get pair values
    redPixels_adjusted = adjust_to_even(red_pixels)
    print('-----')
    print(redPixels_adjusted)
    print(textbin)
    # encode (red_pixels + binary text) 
    redPixels_adjusted = encode(redPixels_adjusted, textbin)
    print('---red + bin--')
    print(redPixels_adjusted)

    # adpat rows to format (list of tuple)
    rows_adapted = adapt_rows(rows) 
    print('---adapted--')
    print(rows_adapted)

    # insert red_pixels encoded in rows
    final_rows =  set_red_pixels(redPixels_adjusted, rows_adapted, width, high)  
    print('---insert red coded--')
    print(rows_adapted)
    # generate image
    generat_png(width, high, final_rows, 'png_message.png')

    print(decode('png_message.png'))
    '''


