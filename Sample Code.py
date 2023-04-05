from PIL import Image

# def compress_quadtree(image):
#     data = []
#     width, height = image.size
#     stack = [(0, 0, width, height)]
#     while stack:
#         x, y, w, h = stack.pop()
#         print("{} {} {} {}".format(x, y, w, h))
#         subimage = image.crop((x, y, x + w, y + h))
#         if all(subimage.getpixel((i, j)) == subimage.getpixel((0, 0)) for i in range(w) for j in range(h)):
#             data.append(subimage.getpixel((0, 0)))
#         else:
#             w2 = w // 2
#             h2 = h // 2
#             stack.append((x, y, w2, h2))
#             stack.append((x + w2, y, w - w2, h2))
#             stack.append((x, y + h2, w2, h - h2))
#             stack.append((x + w2, y + h2, w - w2, h - h2))
#             data.extend([None, len(data) - 4, len(data) - 3, len(data) - 2, len(data) - 1])
#     return data

def compress_quadtree(original_image):
    # Initialize the quadtree stack
    stack = []
    stack.append((original_image, (0, 0, original_image.size[0]//1000, original_image.size[1]//1000)))

    # Initialize the compressed data list
    data = []

    # Traverse the quadtree
    while len(stack) > 0:
        # Pop the next subimage and region from the stack
        subimage, region = stack.pop()

        # Add the top-left pixel of the subimage to the data list
        if subimage.size[0] > 0 and subimage.size[1] > 0:
            data.append(subimage.getpixel((0, 0)))
        else:
            data.append((0, 0, 0))

        # Check if the subimage can be further divided
        if subimage.size[0] > 1 and subimage.size[1] > 1:
            # Calculate the dimensions of the four quadrants
            x, y, w, h = region
            w2 = w // 2
            h2 = h // 2

            # Divide the subimage into four quadrants
            subimages = [
                subimage.crop((x, y, x + w2, y + h2)),
                subimage.crop((x + w2, y, x + w, y + h2)),
                subimage.crop((x, y + h2, x + w2, y + h)),
                subimage.crop((x + w2, y + h2, x + w, y + h))
            ]

            # Calculate the regions of the four quadrants
            regions = [
                (x, y, w2, h2),
                (x + w2, y, w2, h2),
                (x, y + h2, w2, h2),
                (x + w2, y + h2, w2, h2)
            ]

            # Push the four quadrants onto the stack
            for i in range(4):
                stack.append((subimages[i], regions[i]))

    # Return the compressed data
    return data



def decompress_quadtree(data, width, height):
    image = Image.new('RGB', (width, height))
    index = 0
    stack = [(image, data[index], 0, 0, width, height)]
    while stack:
        image, color, x, y, w, h = stack.pop()
        if color is not None:
            image.paste(Image.new('RGB', (w, h), tuple(color)), (x, y))
        else:
            w //= 2
            h //= 2
            stack.append((image, data[index + 3], x + w, y + h, w, h))
            stack.append((image, data[index + 2], x, y + h, w, h))
            stack.append((image, data[index + 1], x + w, y, w, h))
            stack.append((image, data[index], x, y, w, h))
            index += 4
    return image

# Load the original image
original_image = Image.open("Sample.png")

# Compress the image using a quadtree
compressed_data = compress_quadtree(original_image)

# Decompress the compressed data into a new image
# decompressed_image = decompress_quadtree(compressed_data, original_image.width, original_image.height)

# Display the original and decompressed images
original_image.show()
# decompressed_image.show()
# original_image.save(f'C:/Users/Swastik/Desktop/OS LAB/LAB 8/myimage.png')