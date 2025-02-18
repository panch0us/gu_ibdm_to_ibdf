# список для обработки исходного xml-файла (без пробелов слева и справа)
xml_after_strip = []
# список для обработки xml-файла - удаления из него всё до тега <Document> и проверка его на небольшое соответствие
xml_after_match = []
# в списке хранится номер элемента списка с тегом <Applicant type=
xml_epgu_elem = []
# в списке каждое лицо хранится в отдельном списке
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
    xml_epgu.append(xml_after_match[el:])
    del xml_after_match[el:]

xml_epgu = xml_epgu[::-1]

# получаем список с лицом, из общего списка всех лиц
for el_list in xml_epgu:
    # перебираем все теги
    for el in el_list:
        if '<CPSurname>' in el:
            print(el, end='')
        if '<CPName>' in el:
            print(el, end='')
        if '<CPPatronymic>' in el:
            print(el, end='')
        if '<CPBirthday>' in el:
            print(el)
        # Продумать блок со старыми ФИО???
        if '<CPLastFIO>' in el:
            print('(', end='')
        if '<CPLSurname>' in el:
            print(el + ')')

for el in xml_epgu:
    print(el)

# попробовать match/case уменьшить список и оставить блок <ConvictionPerson>?
# ИЛИ лучше оставить ТЕГ <Applicant type=" и блок <ConvictionPerson>?