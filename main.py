import cv2
import os
import numpy as np

def make_folder(folders):
    for folder in folders:
        os.makedirs(folder,exist_ok=True)

def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)


def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def add_border(in_img,border_size=3):
    row, col = in_img.shape[:2]
    bottom = in_img[row-2:row, 0:col]
    #mean = cv2.mean(bottom)[0]
    mean = [255,255,255]
    in_img = cv2.copyMakeBorder(
        in_img,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=mean
    )
    return in_img

def create_output_img_form(imgs_list):
    
    out_img_np =[]

    #create merge form
    if len(imgs_list)== 1:
        merge_form = [1]
    elif len(imgs_list)== 2:
        merge_form = [2]
    elif len(imgs_list)== 3:
        merge_form = [1,2]
    elif len(imgs_list)== 4:
        merge_form = [2,2]
    elif len(imgs_list)== 5:
        merge_form = [2,3]
    elif len(imgs_list)== 6:
        merge_form = [3,3]
    elif len(imgs_list)== 7:
        merge_form = [3,3,1]
    elif len(imgs_list)== 8:
        merge_form = [4,4]
    elif len(imgs_list)== 9:
        merge_form = [3,3,3]
    elif len(imgs_list)== 10:
        merge_form = [4,4,2]
    else:
        merge_form =[]

    #generate out_img_array
    row_id = 0
    for row in range(0,len(merge_form)):
        row_np =[]
        for idx in range(0,merge_form[row]):
            row_np.append(imgs_list[row_id])
            row_id+=1
        out_img_np.append(row_np)
    
    return out_img_np

if __name__ == '__main__':
    global base_path, input_path, output_path
    base_path = os.getcwd()
    input_path = os.path.join(base_path,'input')
    output_path = os.path.join(base_path,'output')

    #for each folder in input dir
    for folder in os.listdir(input_path):
        print(os.path.join(input_path,folder))

        #get files list then read img
        file_list = os.listdir(os.path.join(input_path,folder))
        imgs_list =[]
        for idx,img in enumerate(file_list):
            sub_img = cv2.imread(os.path.join(input_path,folder,file_list[idx]))
            sub_img = add_border(sub_img) #add boder to img
            imgs_list.append(sub_img)     
        
        """
        #get way to merge img 
        if len(imgs_list) ==5:
            img_form_array =[[imgs_list[0]],[imgs_list[1], imgs_list[2]],[imgs_list[3], imgs_list[4]]]
        elif len(imgs_list) ==9:
            img_form_array =[[imgs_list[0],imgs_list[1],imgs_list[2]],[imgs_list[3], imgs_list[4], imgs_list[5]],[imgs_list[6], imgs_list[7], imgs_list[8]]]
        """

        img_form_array = create_output_img_form(imgs_list)

        #resize + concat img
        im_tile_resize = concat_tile_resize(img_form_array)
        
        #write to output file
        cv2.imwrite(os.path.join(output_path,'{}.jpg'.format(folder)), im_tile_resize)