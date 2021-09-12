import re
import sys
import xml.etree.ElementTree as ET

# with open("Output/AldiSued2/20210905_annotation/20210905131534_haushalt.xml") as f:
#    xml = f.read()

pattern_rating = r"(\d.\d)( *\s+ *Sternen?)"
pattern_rating_count = r"(Keine|\d?)( *)(\n?)( *)(Bewertungen)"
pattern_quantity_price_relation = r"(\d* *\n?)(kg|g|ml|l)( *\n? *= *\n?)(€ *\n? *\d,\d*)"
pattern_quantity = r"(\d x )?(\d+,?\d*)( ?|-?)(g|kg|Kg|ml|l|Stück)(;|-)"
pattern_price = r"(€ \d+,?\d*)( |\n)"
pattern_name = r"(Bewertungen; )(\D*)( *|\n?)( <claim_p_quantity)"


tree = ET.parse('Output/AldiSued2/20210912_2/20210912144752_haushalt.xml')
root = tree.getroot()

idx = 0
for product in root.findall('Product'):
    # print(product)
    if idx >= 0:
        p_info = product.find('p_info').text
        # print(p_info)
        print()
        try:
            result = re.findall(pattern_rating, p_info)
            # print(str(result))
            for entry in result:
                p_info = p_info.replace("".join(entry),
                                        "<claim_p_rating>" + str(entry[0]) + "</claim_p_rating>" +
                                        str(entry[1]))

            result = re.findall(pattern_rating_count, p_info)
            for entry in result:
                p_info = p_info.replace("".join(entry), "<claim_p_rating_count>" + str(entry[0]) + "</claim_p_rating_count>" +
                                        str(entry[1]) + str(entry[2]) + str(entry[3]) + str(entry[4]))

            result = re.findall(pattern_quantity_price_relation, p_info)
            for entry in result:
                p_info = p_info.replace("".join(entry), "<claim_p_quantity_price_relation>" +
                                        str(entry[0]) + str(entry[1]) + str(entry[2]) + str(entry[3]) +
                                        "</claim_p_quantity_price_relation>")

            result = re.findall(pattern_quantity, p_info)
            for entry in result:
                p_info = p_info.replace("".join(entry), "<claim_p_quantity>" + str(entry[0]) +
                                        str(entry[1]) + str(entry[2]) + str(entry[3]) + "</claim_p_quantity>" + entry[4])

            result = re.findall(pattern_price, p_info)
            for entry in result:
                p_info = p_info.replace("".join(entry), "<claim_p_price>" + str(entry[0]) + "</claim_p_price>" + entry[1])

            result = re.search(pattern_name, p_info)
            # print(result.groups())
            #for entry in result:
            #    print(entry)
            p_info = p_info.replace(result.groups()[1], "<claim_p_name>" + str(result.groups()[1]) + "</claim_p_name>")
            # print(p_info)


        except:
            print(p_info)
            print("Exception " + str(sys.exc_info()[0]) + " Occured")
            print("Details: " + str(sys.exc_info()[1]))
    idx = idx + 1

    # print(xml)

# test_string = "0.0 Sternen"
# test_pattern = "p_info"
# print(m)
# print(xml)
