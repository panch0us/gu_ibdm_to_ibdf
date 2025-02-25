from tag_filter import tag_filter

# в списке хранится номер элемента списка с тегом <Applicant type=
xml_epgu_elem = []
# в списке каждое лицо хранится в отдельном списке
xml_epgu = []


def open_and_strip_xml():
    """
    Открывает xml-файл. Удаляет лишние пробелы слева и справа в каждой строке.
    :return: Список с тегами без лишних пробелов.
    """
    # список для обработки исходного xml-файла (без пробелов слева и справа)
    _xml_after_strip = []
    # открываем xml-файл в формате utf-8
    with open("Запросы от 20250113155643.xml", "r", encoding="utf-8") as xml_input:
        # читаем xml-файл построчно
        for line in xml_input:
            # берем каждую строку исходного xml-файла и удаляем лишние пробелы слева и справа
            # после чего добавляем каждую стоку в список
            _xml_after_strip.append(line.strip())
    return _xml_after_strip

def check_xml(bind_xml_after_open):
    """
    Проверяем XML-файл на соответствие стандартному. Пока встречался один вариант. Если не совпадает - исключение.
    :param bind_xml_after_open:
    :return: 0
    """
    match bind_xml_after_open:
        case ['<?xml version="1.0" encoding="UTF-8"?>', '<List>', _, _, _, '<Document>', _,
              '<Procedure>issue</Procedure>', *_, '</Document>', '</List>']:
            print("Стандартный XML")
        case _:
            raise SyntaxError("Ошибка. Формат файла XML не стандартный")
    return 0

def cut_xml(bind_xml_after_strip, bind_tag_filter):
    """
    Обрезаем XML-файл по фильтру
    :param bind_xml_after_strip:
    :param bind_tag_filter:
    :return: Списковое включение
    """
    return [item for item in bind_xml_after_strip if item not in bind_tag_filter]


if __name__ == '__main__':
    # Открываем XML-файл
    xml_after_open_and_strip = open_and_strip_xml()
    print("xml_after_open_and_strip: ", xml_after_open_and_strip)

    # Обрезаем XML-файл
    xml_cut = cut_xml(xml_after_open_and_strip, tag_filter)
    print('xml_cut: ', xml_cut)

    xml_new = [item for item in xml_after_open_and_strip if item not in tag_filter]
    print('xml_new: ', xml_new)

    # Находим все вхождения новых лиц по типам подачи заявлений (тэг <Applicant type=)
    for index, el in enumerate(xml_cut):
        if '<Applicant type=' in el:
            xml_epgu_elem.append(index)
            # print(xml_after_match[index:])
        # if el == '<ConvictionPerson>':
        #    print(1)

    xml_epgu_elem = xml_epgu_elem[::-1]
    print(xml_epgu_elem)

    # Добавляем в список отдельно списки по лицам
    for el in xml_epgu_elem:
        xml_epgu.append(xml_cut[el:])
        del xml_cut[el:]

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
