# список для обработки исходного xml-файла (без пробелов слева и справа)
xml_after_strip = []
# список для обработки xml-файла - удаления из него всё до тега <Document> и проверка его на небольшое соответствие
xml_after_match = []
xml_epgu_elem = []
xml_epgu = []

with open("Запросы от 20250113155643.xml", "r", encoding="utf-8") as xml_input:
    for line in xml_input:
        xml_after_strip.append(line.strip())

print(xml_after_strip)

match xml_after_strip:
    case ['<?xml version="1.0" encoding="UTF-8"?>', '<List>', _, _, _,
          '<Document>', _,
          '<Procedure>issue</Procedure>',
          *xml_after_match, '</Document>',
          '</List>']:
        print(xml_after_match)
    case _:
        raise SyntaxError("Формат файла XML не стандартный")

# Находим все вхождения новых лиц по типам подачи заявлений (тэг <Applicant type=)
for index, el in enumerate(xml_after_match):
    if '<Applicant type=' in el:
        xml_epgu_elem.append(index)

        #print(xml_after_match[index:])

    #if el == '<ConvictionPerson>':
    #    print(1)

xml_epgu_elem = xml_epgu_elem[::-1]
print(xml_epgu_elem)

# Добавляем в список отдельно списки по лицам
for el in xml_epgu_elem:
    xml_epgu.append([xml_after_match[el:]])
    del xml_after_match[el:]


for el in xml_epgu:
    print(el)