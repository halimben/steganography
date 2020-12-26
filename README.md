# steganography
Python program that hide text in png file.<br />

**1. Steps:**<br />

  Get the red pixels from a png file and make them evens values.<br />
  Convert message into binary and add it to red pixels.<br />
  Generate a png file from the new rows how contain red pixels and binary text.<br />
  To decode we cheeck the red values until we find the first serie of 8 even values (end of message).<br />
  From the significant pixels we extract the binary value added before and convert it to string.<br />
  
 

 **2. Execution and options:**
 
 - Mode write:
 > Prgram wil ask for arguments if they are not specified
```console
$  python main.py -w encoded_png.png                                    
``` 
  
    $  Enter your PNG path:
      test.png
    $  Enter your text:
      hello word

> Encode Your_text in png.png, output= encoded_png.png
```console 
$  python main.py png.png -w -f pnp.png -t "Your_text" encoded_png.png  
``` 


- Mode read:
> Decode text hidden in encoded_png.png
```console 
$  python main.py encoded_png.png                                       
```
 
 
 
  
