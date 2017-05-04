__author__ = 'pepOS'


def bytehl(number, nbits):
    val = (number + (1 << nbits)) % (1 << nbits)
    temp = bin(val)[-len(bin(val))+2:]
    hg = temp[:-nbits/2]
    if hg == '':
        hg = '0b0'
    lw = '0b' + temp[-nbits/2:]
    return int(hex(int(hg, 2)), 16), int(hex(int(lw, 2)), 16)


def stdlen8(number):
    
    binR = bin(number)
    if len(binR) < 10:
        binR = (10 - len(binR))*'0' + binR[-len(binR)+2:]
    
    return binR