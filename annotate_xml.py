import re
import sys
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring


def getFileNameWithoutExt(filename):
    return filename[:-4]


def throwException():
    print("Exception " + str(sys.exc_info()[0]) + " Occured")
    print("Details: " + str(sys.exc_info()[1]))


pattern_rating = r"(\d.\d)( *\s+ *Sternen?)"
pattern_rating_count = r"(Keine|\d?)( *)(\n?)( *)(Bewertungen)"
pattern_quantity_price_relation = r"(\d* *\n?)(kg|g|ml|l)( *\n? *= *\n?)(€ *\n? *\d,\d*)"
pattern_quantity = r"(\d x )?(\d+,?\d*)( ?|-?)(g|kg|Kg|ml|l|Stück)(;|-)"
pattern_price = r"(€ \d+,?\d*)( |\n)"
pattern_name = r"(Bewertungen;)( *\n?)(\D*|\d*)( *|\n?|;?)(\D*|\d*)( <claim_p_quantity>| <claim_p_price>)"

# pattern_name = r"(Bewertungen;)( *|\n?)(\D*|\d*|\n?|-*)( *|\n?)(\D*|\d*|\n?|-*)(;?)( <claim_p_quantity>| " \
#               r"<claim_p_price>) "

input_dir = 'Output/AldiSued2/20210912/'
output_dir = 'Output/AldiSued2/20210912_annotation/'

try:
    os.mkdir(output_dir)
except:
    throwException()

xml_files = os.listdir(input_dir)
# xml_f = ["20210912134019_neu-im-sortiment.xml"]
# xml_f = ["20210912140222_kuehlung-und-tiefkuehlkost.xml"]
# print(xml_f)
for file in xml_files:
    input_file = input_dir + file
    tree = ET.parse(input_file)
    root = tree.getroot()

    new_root = Element('Products')
    new_tree = ElementTree(new_root)

    idx = 0
    write_idx = 0
    for product in root.findall('Product'):
        if idx >= 0:
            new_product = SubElement(new_root, 'Product')
            new_product.set('processed', 'false')
            new_p_info = SubElement(new_product, 'p_info')

            p_info = product.find('p_info').text
            try:
                result = re.findall(pattern_rating, p_info)
                for entry in result:
                    p_info = p_info.replace("".join(entry),
                                            "<claim_p_rating>" + str(entry[0]) + "</claim_p_rating>" +
                                            str(entry[1]))

                result = re.findall(pattern_rating_count, p_info)
                for entry in result:
                    p_info = p_info.replace("".join(entry),
                                            "<claim_p_rating_count>" + str(entry[0]) + "</claim_p_rating_count>" +
                                            str(entry[1]) + str(entry[2]) + str(entry[3]) + str(entry[4]))

                result = re.findall(pattern_quantity_price_relation, p_info)
                for entry in result:
                    p_info = p_info.replace("".join(entry), "<claim_p_quantity_price_relation>" +
                                            str(entry[0]) + str(entry[1]) + str(entry[2]) + str(entry[3]) +
                                            "</claim_p_quantity_price_relation>")

                result = re.findall(pattern_quantity, p_info)
                for entry in result:
                    p_info = p_info.replace("".join(entry), "<claim_p_quantity>" + str(entry[0]) +
                                            str(entry[1]) + str(entry[2]) + str(entry[3]) + "</claim_p_quantity>" +
                                            entry[4])

                result = re.findall(pattern_price, p_info)
                for entry in result:
                    p_info = p_info.replace("".join(entry),
                                            "<claim_p_price>" + str(entry[0]) + "</claim_p_price>" + entry[1])

                result = re.search(pattern_name, p_info)
                # print(result.groups())
                # print(p_info)
                if result is not None:
                    result_str = result.groups()[2].replace(";", "") + result.groups()[3].replace(";", "") + result.groups()[4].replace(";", "")
                    # print(result_str.strip())
                    p_info = p_info.replace(result_str.strip(),
                                            "<claim_p_name>" + result_str.strip() + "</claim_p_name>")

                product.find('p_info').text = p_info
                new_p_info.text = p_info
            except:
                throwException()
                # print(p_info)

        idx = idx + 1
        if(idx % 25 == 0):
            write_idx += 1
            filename = getFileNameWithoutExt(file)
            output_file = output_dir + filename + "_annotation_" + str(write_idx) + ".xml"
            with open(output_file, 'wb') as f:
                new_tree.write(f, encoding='UTF-8', xml_declaration=True)
            new_root = Element('Products')
            new_tree = ElementTree(new_root)
            print("Saved: " + output_file + "\n")

    write_idx += 1
    filename = getFileNameWithoutExt(file)
    output_file = output_dir + filename + "_annotation_" + str(write_idx) +  ".xml"
    with open(output_file, 'wb') as f:
        new_tree.write(f, encoding='UTF-8', xml_declaration=True)
    print("Saved: " + output_file + "\n")
    new_tree = None
