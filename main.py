_filter = {'<?xml version="1.0" encoding="UTF-8"?>', '<NaturalPerson>', '<ListID>', '<ListTime>', '<ListItem>',
           '<Document>', '<DocumentID>', '<Procedure>', '<NaturalPerson>', '<Surname>'}
# в списке хранится номер элемента списка с тегом <Applicant type=
xml_epgu_elem = []
# в списке каждое лицо хранится в отдельном списке
xml_epgu = []

def open_and_strip_xml() -> list[str]:
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


def check_and_match_xml(bind_xml_after_strip: list[str]) -> list[str]:
    """
    Переименовать, не только проверка, но и урезание. Возмножно переработать, с учетом блока <ConvictionPerson>? (внизу)
    :param bind_xml_after_strip:
    :return:
    """
    match bind_xml_after_strip:
        case ['<?xml version="1.0" encoding="UTF-8"?>', '<List>', _, _, _,
              '<Document>', _,
              '<Procedure>issue</Procedure>',
              *_xml_after_check_and_match, '</Document>',
              '</List>']:
            print("xml_after_check_and_match: ", _xml_after_check_and_match)
        case _:
            raise SyntaxError("Формат файла XML не стандартный")
    return _xml_after_check_and_match


def cut_xml(bind_xml_after_check_and_match: list[str]) -> list[str]:
    """НЕ РАБОТАЕТ - НУЖНО УБРАТЬ ВСЕ ЛИШНИЕ ТЕГИ"""
    _xml_after_cut = []

    for el in _filter:
        for line in xml_after_check_and_match:
            if el in line:
                pass
            else:
                _xml_after_cut.append(line)

    return _xml_after_cut


if __name__ == '__main__':

    xml_after_open_and_strip: list[str] = open_and_strip_xml()
    print("xml_after_open_and_strip: ", xml_after_open_and_strip)

    # список для обработки xml-файла - удаления из него всё до тега <Document> и проверка его на небольшое соответствие
    xml_after_check_and_match: list[str] = check_and_match_xml(xml_after_open_and_strip)

    xml_after_cut : list[str] = cut_xml(xml_after_check_and_match)
    print('xml_after_cut: ', xml_after_cut)

    # Находим все вхождения новых лиц по типам подачи заявлений (тэг <Applicant type=)
    for index, el in enumerate(xml_after_check_and_match):
        if '<Applicant type=' in el:
            xml_epgu_elem.append(index)
            # print(xml_after_match[index:])
        # if el == '<ConvictionPerson>':
        #    print(1)

    xml_epgu_elem = xml_epgu_elem[::-1]
    print(xml_epgu_elem)

    # Добавляем в список отдельно списки по лицам
    for el in xml_epgu_elem:
        xml_epgu.append(xml_after_check_and_match[el:])
        del xml_after_check_and_match[el:]

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
