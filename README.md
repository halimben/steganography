# steganography
Python program that hides text in png file.<br />

**1. Steps:**<br />

  Get the rgba chanels from a png file and make them evens values.<br />
  Convert message into binary and add it to rgba values.<br />
  Generate a png file from the new rows which contain (rgba + binary).<br />
  To decode we check the rgba values until we find the first series of 8 even values (end of message).<br />
  From the significant pixels we extract the binary value added before and convert it to string.<br />
  
 

 **2. Execution and options:**
 
 - Mode write:
 
```console
$  python main.py -w encoded_png.png                             
``` 
  
      Enter your PNG path:
      test.png
      Enter your text:
      hello word_

or

```console 
$  python main.py -w -f png.png -t "Your_text" encoded_png.png
``` 

<br />

- Mode read:

```console 
$  python main.py encoded_png.png   # Decode text hidden in encoded_png.png                                       
```
 
 
 
  
