# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 22:55:39 2024

@author: Shen
@name: Image Metadata adder
@description:
    
    Adds metadata to an image and can also read it as well.
    
"""

from exif import Image
import webbrowser

import reverse_geocoder as rg
import pycountry

#%%

def format_dms_coordinates(coordinates):
    return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""

def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref):        
    decimal_latitude = dms_coordinates_to_dd_coordinates(latitude, latitude_ref)
    decimal_longitude = dms_coordinates_to_dd_coordinates(longitude, longitude_ref)
    url = f"https://www.google.com/maps?q={decimal_latitude},{decimal_longitude}"
    webbrowser.open_new_tab(url)

    


def runtest():
    '''Do a test run on 2 images comparing them    
    Source:
        https://auth0.com/blog/read-edit-exif-metadata-in-photos-with-python/
    '''    
    
    ### EXIF image objects
    with open("images/palm-tree-1.jpg", "rb") as palm_1_file:
        palm_1_image = Image(palm_1_file)
        
    with open("images/palm-tree-2.jpg", "rb") as palm_2_file:
        palm_2_image = Image(palm_2_file)
        
    images = [palm_1_image, palm_2_image]

    ### acquire metadata
    for index, image in enumerate(images):
        if image.has_exif:
            status = f"contains EXIF (version {image.exif_version}) information."
        else:
            status = "does not contain any EXIF information."
        print(f"Image {index} {status}")
        
        print(f"Device information - Image {index}")
        print("----------------------------")
        print(f"Make: {image.make}")
        print(f"Model: {image.model}\n")
        
        print(f"Lens and OS - Image {index}")
        print("---------------------")
        print(f"Lens make: {image.get('lens_make', 'Unknown')}")
        print(f"Lens model: {image.get('lens_model', 'Unknown')}")
        print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
        print(f"OS version: {image.get('software', 'Unknown')}\n")
        
        # We can find out by looking at each photo’s datetime_original property, which specifies 
        # the date and time when the photo was taken. The processor in a smartphone is fast enough 
        # to record the exact fraction of a second when it takes a photo, and that fraction is stored
        # in the subsec_time_original property.
        print(f"Date/time taken - Image {index}")
        print("-------------------------")
        print(f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n")
        
        
        # You may have noticed the slight difference between the coordinates reported in the photos. 
        # This is expected; even the same device, located at the same spot, will report slightly different coordinates 
        # at different times. The discrepancy in coordinates reported by the phones is on the order of a fraction of a second, 
        # which translates to about 8 meters or about 25 feet.
        print(f"Coordinates - Image {index}")
        print("---------------------")
        # print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
        # print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n")
        print(f"Latitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}")
        print(f"Longitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n")
        
        decimal_latitude = dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)
        decimal_longitude = dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)
        print(f"Latitude (DD): {decimal_latitude}")
        print(f"Longitude (DD): {decimal_longitude}\n")
                
        coordinates = (decimal_latitude, decimal_longitude)
                
        print('=======================')
        
    image_members = []
    for image in images:
        image_members.append(dir(image))
    
    for index, image_member_list in enumerate(image_members):
        print(f"Image {index} contains {len(image_member_list)} members")
        # print(f"{image_member_list}\n")

    common_members = set(image_members[0]).intersection(set(image_members[1]))
    print(f"Image 0 and Image 1 have {len(common_members)} members in common")
    common_members_sorted = sorted(list(common_members))
    # print(f"{common_members_sorted}")

    return common_members_sorted, image_members, images, coordinates

#%%
if __name__ == '__main__':
    common_members_sorted, image_members, images, coordinates = runtest()

    # reverse search address and plot on maps
    for index, image in enumerate(images):
        # REVERSE SEARCH FOR ADDRESS
        location_info = rg.search(coordinates)[0]
        location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
        print(f"{location_info}\n")
        
        # DRAW MAP ON GOOGLE
        draw_map_for_location(image.gps_latitude, 
                              image.gps_latitude_ref, 
                              image.gps_longitude,
                              image.gps_longitude_ref)