import numpy as np
import cv2
import matplotlib.pyplot as plt


# init subplot
def get_subplots(row, col, title=''):
    fig, ax = plt.subplots(row, col, figsize=(10, 6))
    
    plt.suptitle(title)
    
    # flatten the ax array and map to turn off axis
    [axi.axis('off') for axi in ax.ravel()]

    return fig, ax

# show image
def imshow(img, axis, title=''):
    axis.imshow(img)
    axis.set_title(title)
    
    
# read and crop  image
def imread(path, axis=None, shape=(), title='', display=True):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if shape:
        # crop image
        img = cv2.resize(img, (shape[1], shape[0]))
    
    if axis:
        axis.imshow(img)
        axis.set_title(title)
    elif display == True:
        plt.imshow(img)
        plt.title(title)
        
    return img


def create_mask(img, lower_bound, upper_bound, axis, title=''):
    lower_bound = np.array(lower_bound)
    upper_bound = np.array(upper_bound)
    
    mask = cv2.inRange(img, lower_bound, upper_bound)

    axis.imshow(mask, cmap='gray')
    axis.set_title(title)
    
    return mask


# mask image
def mask_image(img, mask, axis, flag=0, title=''):    
    if flag == 0:
        img[mask == 0] = [0, 0, 0]
    else:
        img[mask != 0] = [0, 0, 0]

    axis.imshow(img)
    axis.set_title(title)
    
    return img


# return sum of all images added 
def add_images(images, axis, title='Image with new background'):
    complete_image = np.sum(images, axis=0)
    
    axis.imshow(complete_image)
    axis.set_title(title)
    
    return complete_image

# change bg
def background_change(ori_path, bg_path, lower_bound, upper_bound, save_as=''):
    fig, ax = get_subplots(2, 3, title="Background change using basic image processing")

    # show original image
    img = imread(ori_path, ax[0, 0], title='Original Image')
    img = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=1)


    # create mask
    mask = create_mask(img, lower_bound, upper_bound, ax[0, 1], title='Background mask')

    # segregate out background from original image
    masked_image = mask_image(img, mask, ax[0, 2], flag=1, title='Image w/o background')

    # read and process background image
    crop_background = imread(bg_path, ax[1, 0], shape=img.shape, title='Background Image')
    background_masked = mask_image(crop_background, mask, ax[1, 1], flag=0, title='BG w/o foreground region')

    completed_image = add_images([masked_image, crop_background], ax[1, 2], title='Image with new background')

    # plt.tight_layout()
    if save_as != '':
        fig.savefig(save_as)


from argparse import ArgumentParser



# have to make changes to account for accepting bounds as string through terminal
# def main():

#     parser = ArgumentParser()
#     parser.add_argument("-i", "--input", required=True, help="Input image path")
#     parser.add_argument("-o", "--output", required=True, help="Output image path")
#     parser.add_argument("-l", "--lower", required=True, help="Lower bound for mask")
#     parser.add_argument("-u", "--upper", required=True, help="Lower bound for mask")
#     parser.add_argument("-s", "--saveas", help="Save output path")

#     args = parser.parse_args()

#     background_change(args['input'], args['output'], args['lower'], args['upper'], args['saveas'])


# if __name__ == "__main__":
#     main()