# a small script for Leica optical microscope (based on leica m125 c data)
import warnings

from tqdm import tqdm #pip install tqdm
import cv2, os #pip install opencv-python
from xml.dom.minidom import parse, Node

def find_id_attribute(parent, attribute_name="XMetresPerPixel"):
    """"""
    global some_mcm  # a workaround to extract the value from recursive function (it should be easier)
    # inspired https://realpython.com/python-xml-parser/
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.tagName == attribute_name:
            some_mcm = parent.firstChild.data  # parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        find_id_attribute(child, attribute_name)

if __name__ == '__main__':
    ignore_folders = ["venv", ".idea"]
    extentions = [".jpg"]
    workdir = ""  # path in a format 'F:/somepath/orig' where all data stored with images and xml files together
    mode = "px"  # px - for fixed px length of a scale
                 # mcm - for fixed scale in mcm
    line_px_length = 500  # length for all scales in px
    line_mcm_length = 100  # length for all scales in μm
    for path, dirs, files in tqdm(os.walk(workdir)):
        if any([each in path for each in ignore_folders]):
            continue
        print(path, dirs, files)
        work_files = list(filter(lambda x: x if list(set(extentions).intersection(
            set(os.path.splitext(x)))) != []
            else None, files))
        if work_files:
            for file in work_files:
                name, ext = os.path.splitext(file)
                cal_name = name+".jpg.cal.xml"
                full_path_cal = os.path.join(path, cal_name)
                full_path_im = os.path.join(path, file)
                global some_mcm
                some_mcm = 0
                if os.path.exists(full_path_cal):
                    document = parse(full_path_cal)
                    find_id_attribute(document)
                    text_um = round(float(some_mcm) * 10 ** 6, 3)
                    im = cv2.imread(full_path_im)
                    if mode == "px":
                        fin_length_px = str(int(line_px_length * text_um))
                    else:
                        line_px_length = int(line_mcm_length/text_um)
                        fin_length_px = str(line_mcm_length)
                    line_px_width = 20
                    h, w = im.shape[:2]
                    from_right = 50
                    from_bottom = 10
                    line_start_w = w-from_right-line_px_length
                    text_start_w = line_start_w
                    line_start_h = h-from_bottom-line_px_width
                    cv2.line(im, (line_start_w,line_start_h), (line_start_w+line_px_length, line_start_h),
                             (0, 0, 255), line_px_width)

                    font = cv2.FONT_HERSHEY_COMPLEX
                    text_size, baseline = cv2.getTextSize(fin_length_px+"mcm", font,
                                                3, 3)
                    if text_size[0]+text_start_w-from_right > w:
                        text_start_w = w-text_size[0]
                    cv2.putText(im, fin_length_px+"mcm", (text_start_w-from_right,
                                                       line_start_h-from_bottom-line_px_width), font, 3,
                                (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.imwrite(os.path.join(path, name+"_scale_"+mode+ext), im)
                else:
                    if "_scale_" in full_path_cal:
                        continue
                    else:
                        warnings.warn("Doesn't have scale file:%s"%full_path_cal)
    print("Done!")

    # cv2.imshow("", cv2.resize(im, (800, 600)))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




    # def list_recursevly(node, name='XMetresPerPixel'):
    #     for child in node:
    #         if child.tag != name:
    #             print(child.tag)
    #         else:
    #             print("yay!", name)
    #             return
    # list_recursevly(root)
    # # print("done")
    # for child in root:
    #     print(child.tag, ", ", child.attrib, child.text )
    #     for each_child in child:
    #         print("2", each_child.tag, ", ", each_child.attrib, each_child.text )
    #         for each_child_2 in each_child:
    #             print("3", each_child_2.tag, ", ", each_child_2.attrib, each_child_2.text )
    #             for each_child_3 in each_child_2:
    #                 print("4", each_child_3.tag, ", ", each_child_3.attrib, each_child_3.text )
    #                 for each_child_4 in each_child_3:
    #                     print("5", each_child_4.tag, ", ", each_child_4.attrib, each_child_4.text )
    #                     for each_child_5 in each_child_4:
    #                         print("6", each_child_5.tag, ", ", each_child_5.attrib, each_child_5.text )
    #                         for each_child_6 in each_child_5:
    #                             print("7", each_child_6.tag, ", ", each_child_6.attrib, each_child_6.text)
    #                             for each_child_7 in each_child_6:
    #                                 print("8", each_child_7.tag, ", ", each_child_7.attrib, each_child_7.text)
    #                                 for each_child_8 in each_child_7:
    #                                     print("9", each_child_8.tag, ", ", each_child_8.attrib, each_child_8.text)
    #                                     for each_child_9 in each_child_8:
    #                                         print("10", each_child_9.tag, ", ", each_child_9.attrib, each_child_9.text)
    #                                         for each_child_10 in each_child_8:
    #                                             print("11", each_child_10.tag, ", ", each_child_10.attrib, each_child_10.text)
    #                                             for each_child_11 in each_child_10:
    #                                                 print("12", each_child_11.tag, ", ", each_child_11.attrib, each_child_11.text)
    #                                                 for each_child_12 in each_child_11:
    #                                                     print("13", each_child_12.tag, ", ", each_child_12.attrib, each_child_12.text)
    #                                                     for each_child_13 in each_child_12:
    #                                                         print("14", each_child_13.tag, ", ", each_child_13.attrib, each_child_13.text)
    #                                                         for each_child_14 in each_child_13:
    #                                                             print("15", each_child_14.tag, ", ", each_child_14.attrib, each_child_14.text)
    #                                                             for each_child_15 in each_child_14:
    #                                                                 print("16", each_child_15.tag, ", ", each_child_15.attrib, each_child_15.text)
    #
    #
    #
    #
    #     # See PyCharm help at https://www.jetbrains.com/help/pycharm/
