'''
Created on Sep 7, 2013

@author: mlukasik
'''
def ellipse(x, y):
    q = (x-10)**2 + ((y-20)/1.3)**2 
    if q >= 7**2 and q <= 9**2:
        return True
    #print "BAD"
    return False

def H(x, y):
    if y == 30 or y == 31 or y == 10 or y == 11: 
        return True
    elif (x == 5 or x == 4) and (y >= 10 or y <= 30):
        return True
    else:
        return False

def two_circles(x, y):
    if ((x-5)**2 + (y-30)**2 < 11) or( (x-5)**2 + (y-10)**2 < 11): 
        return True
    return False


freq = 100
munsell_fname = "../wcs_input_data/330WCS.xml"
clab_fname = "../wcs_input_data/c-lab-330.txt"
chip_fname = "../wcs_input_data/chip.txt"
out_fname = "../wcs_input_data/330WCS_two_circles.xml"
out_picname = "../wcs_input_data/330WCS_two_circles.png"
cat = "../../../steels/simulations_two_circles"
res_cat = "pictures_two_circles"
#This function returns boolean if a given point in 2d should be multiplied or not.
is_to_be_multiplied = two_circles
