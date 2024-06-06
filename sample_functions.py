import random
import time

BARCODE_XML_PATH = 'Metadata/AttachmentInfos[0]/Label/Barcodes[0]/Content'
BARCODE_DUMMY_CHARS = 'abcdefghkmnpqrstuvwzABCDEFGHJKLMNPQRSTUVWXYZ1234567890'
BARCODE_DUMMY_LENGTH = 9

def get_barcode(zen_image):
    ###
    #
    # Get and format barcode from the ZenImage metadata.
    #
    # Parameters
    # ==========
    # zen_image: Zeiss.Micro.Scripting.ZenImage
    #   A ZenImage acquired with the CD7.
    #
    # Returns
    # =======
    # barcode: string
    #   The formatted barcode.
    #
    ###

    # Get barcode text from metadata element.
    # Note: returns an empty string if barcode element missing from metadata.
    try:
        barcode_text = zen_image.Metadata.GetMetadataStringWithPath(BARCODE_XML_PATH)
    except:
        barcode_text = ''

    # Extract barcode string from element text (e.g. "left barcode: the_barcode").
    # Note: doesn't work if there are spaces within the barcode.
    barcode = barcode_text.split(' ')[-1]

    # If barcode is missing (empty string), replace it with a dummy string.
    if barcode == '':
        barcode = ''.join(random.choice(BARCODE_DUMMY_CHARS) for _ in range(BARCODE_DUMMY_LENGTH))

    return barcode

def get_timestamp():
    ###
    #
    # Get a timestamp in a YYYYMMDDHHMM format.
    #
    # Returns
    # =======
    # string
    #   The formatted timestamp.
    #
    ###
    return time.strftime("%Y%m%d%H%M")
