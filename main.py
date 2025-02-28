from xml_tags import tags


def open_and_strip_xml():
    """
    Открывает xml-файл. Удаляет лишние пробелы слева и справа в каждой строке.
    :return: Список с тегами без лишних пробелов.
    """
    # список для обработки исходного xml-файла (без пробелов слева и справа)
    _xml_after_strip = []
    # открываем xml-файл в формате utf-8
    with open('Запросы от 20250113155643.xml', 'r', encoding='utf-8') as xml_input:
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
            print("Проверка XML: Стандартный!")
        case _:
            raise SyntaxError("Ошибка. Формат файла XML не стандартный")
    return 0

def cut_xml(bind_xml_after_strip, bind_tags):
    """
    Сокращает XML-файл, сопоставляя исходный XML со списком тегов, которые должны остаться
    :param bind_xml_after_strip:
    :param bind_tags:
    :return: список лиц с Видом заявления, ФИО и Датой рождения
    """
    return [el
            for el in bind_xml_after_strip
                for tag in bind_tags
                    if el.startswith(tag)]

def index_xml(bind_xml_cut):
    """
    По обрезанному XML-файлу находим тег <Applicant type=> и в отдельном списке проставляем по этому тегу индексы.
    Инверсируем этот список.
    :param bind_xml_cut:
    :return: Инверсированный список индексов по тегу <Applicant type=> из обрезанного XML-файла
    """
    return [index for index, tag in enumerate(bind_xml_cut) if tag.startswith('<Applicant type=')][::-1]

def build_list_by_tag_from_xml(bind_xml_after_cut, bind_xml_after_index):
    """
    Создает список списков по списку индексов, отобранных в функции index_xml, через аргумент bind_xml_after_index.
    В каждый отдельный список помещается уникальное лицо.
    :param bind_xml_after_cut:
    :param bind_xml_after_index:
    :return: Список списков с отдельными лицами.
    """
    xml_epgu = []
    # Добавляем в список отдельно списки по лицам
    for el in bind_xml_after_index:
        xml_epgu.append(bind_xml_after_cut[el:])
        del bind_xml_after_cut[el:]

    xml_epgu = xml_epgu[::-1]
    return xml_epgu


if __name__ == '__main__':
    # Открываем XML-файл
    xml_after_open_and_strip = open_and_strip_xml()
    print("xml_after_open_and_strip: ", xml_after_open_and_strip)

    # Проверяем XML-файла
    check_xml(xml_after_open_and_strip)

    # Обрезаем XML-файл
    xml_after_cut = cut_xml(xml_after_open_and_strip, tags)
    print('xml_cut: ', xml_after_cut)

    # Создаем список с индексами по обрезанному XML-файл по тегу <Applicant type=>
    xml_after_index = index_xml(xml_after_cut)
    print('xml_after_index: ', xml_after_index)

    xml_epgu = build_list_by_tag_from_xml(xml_after_cut, xml_after_index)

    for el in xml_epgu:
        print(el)

    print(xml_after_cut)
