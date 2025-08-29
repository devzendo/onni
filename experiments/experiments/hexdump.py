def hexdump(buf, length):
    """
    Display a hexadecimal and printable ASCII dump of a memory area.
    
    Args:
        buf: bytearray containing the data to dump
        length: number of bytes to dump from the buffer
    """
    hexdigs = "0123456789abcdef"
    offset = 0
    left = length
    
    while left > 0:
        # Initialize line with spaces
        line = [' '] * 78
        
        # Set the separator characters
        line[9] = '|'
        line[59] = '|'
        
        # Format the offset (8 hex digits)
        offset_str = f"{offset:08X}"
        for i, c in enumerate(offset_str):
            line[i] = c
        line[8] = ' '
        
        # Determine how many bytes to process (up to 16)
        upto16 = min(16, left)
        
        # Process each byte in this line
        for x in range(upto16):
            b = buf[offset + x]
            
            # Convert byte to hex digits
            line[11 + (3 * x)] = hexdigs[(b & 0xf0) >> 4]
            line[12 + (3 * x)] = hexdigs[b & 0x0f]
            
            # Add printable ASCII character or dot
            if 32 <= b <= 126:  # printable ASCII range
                line[61 + x] = chr(b)
            else:
                line[61 + x] = '.'
        
        # Convert line list to string and print
        print(''.join(line))
        
        offset += upto16
        left -= upto16

