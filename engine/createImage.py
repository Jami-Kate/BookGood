import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

def create_image(fig, img):
    # Convert the pie chart to an image
    plt.savefig(img, format="png") # temporarily store the image in byte stream 
    img.seek(0)
    plt.close('all')  # close to free memory
    img64 = base64.b64encode(img.getvalue()).decode('utf-8') # encode the imagine in base64; allows it to be enbedded in HTML without creating a separate file for it
    return img64