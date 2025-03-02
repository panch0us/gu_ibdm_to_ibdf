from xml_tags import tags


class Person:
    """
    Лицо с ФИО и Датой рождения, а также со старыми ФИО
    """
    def __init__(self,
                 CPSurname=None,        # Имя
                 CPName=None,           # Фамилия
                 CPPatronymic=None,     # Отчество
                 CPLSurname=None,       # Старая фамилия
                 CPLName=None,          # Старое имя
                 CPLPatronymic=None,    # Старое отчество
                 CPBirthday=None,       # Дата рождения (ДД.ММ.ГГГГ)
                 flag_old_data=False,   # Есть ли у лица старые ФИО? (по умолчанию нет)
                 ):

        if CPSurname is None:
            self.CPSurname = []
        else:
            self.CPSurname = list(CPSurname)
        if CPName is None:
            self.CPName = []
        else:
            self.CPName = list(CPName)
        if CPPatronymic is None:
            self.CPPatronymic = []
        else:
            self.CPPatronymic = list(CPPatronymic)
        if CPLSurname is None:
            self.CPLSurname = []
        else:
            self.CPLSurname = list(CPSurname)
        if CPLName is None:
            self.CPLName = []
        else:
            self.CPLName = list(CPLName)
        if CPLPatronymic is None:
            self.CPLPatronymic = []
        else:
            self.CPLPatronymic = list(CPLPatronymic)
        if CPBirthday is None:
            self.CPBirthday = []
        else:
            self.CPBirthday = list(CPBirthday)

        self.flag_old_data = flag_old_data

    def check_old_data(self):
        """
        Если есть старые ФИО - то флаг ставится в True
        """
        if (len(self.CPLSurname) or len(self.CPLName) or len(self.CPLPatronymic)) > 0:
            self.flag_old_data = True


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

def index_xml(bind_xml_cut) -> list[int]:
    """
    По обрезанному XML-файлу находим тег <Applicant type=> и в отдельном списке проставляем по этому тегу индексы.
    Инверсируем этот список.
    :param bind_xml_cut:
    :return: Инверсированный список индексов по тегу <Applicant type=> из обрезанного XML-файла
    """
    return [index for index, tag in enumerate(bind_xml_cut) if tag.startswith('<Applicant type=')][::-1]

def decomposing_xml_by_indexes_into_lists(bind_xml_after_cut, bind_xml_after_index):
    """
    Создает список списков по индексам, полученных их функции index_xml, через аргумент bind_xml_after_index.
    В каждый отдельный список помещается уникальное лицо.
    :param bind_xml_after_cut:
    :param bind_xml_after_index:
    :return: Список списков с отдельными лицами.
    """
    # xml после разбивки по индексам на списки
    _xml_after_decomposing_by_indexes_into_lists = []
    # Добавляем в список отдельно списки по лицам
    for el in bind_xml_after_index:
        _xml_after_decomposing_by_indexes_into_lists.append(bind_xml_after_cut[el:])
        del bind_xml_after_cut[el:]

    _xml_after_decomposing_by_indexes_into_lists = _xml_after_decomposing_by_indexes_into_lists[::-1]
    return _xml_after_decomposing_by_indexes_into_lists

def distribution_of_persons_by_groups(bind_xml_after_decomposing_by_indexes_into_lists) -> dict[str, list]:
    """
    Группируем лиц по видам подачи заявлений (ЕПГУ, Физ лицо, МФЦ)
    :param bind_xml_after_decomposing_by_indexes_into_lists:
    :return: словарь с ключами по видам заявлений и по значениям - спискам лиц
    """
    _groups_persons = {
        'epgu': [],
        'mfc': [],
        'fiz_lico': [],
    }

    for line in bind_xml_after_decomposing_by_indexes_into_lists:
        if 'Единый портал гос.услуг' in line[0]:
            _groups_persons['epgu'].append(line[1:])
        if 'МФЦ' in line[0]:
            _groups_persons['mfc'].append(line[1:])
        if 'Физическое лицо' in line[0]:
            _groups_persons['fiz_lico'].append(line[1:])

    return _groups_persons


if __name__ == '__main__':
    # Открываем XML-файл
    xml_after_open_and_strip = open_and_strip_xml()
    #print('xml_after_open_and_strip: ', xml_after_open_and_strip)

    # Проверяем XML-файл
    check_xml(xml_after_open_and_strip)

    # Обрезаем XML-файл
    xml_after_cut = cut_xml(xml_after_open_and_strip, tags)
    #print('xml_cut: ', xml_after_cut)

    # Создаем список с индексами по обрезанному XML-файл по тегу <Applicant type=>
    xml_after_index: list[int] = index_xml(xml_after_cut)
    #print('xml_after_index: ', xml_after_index)

    # Создаем список списков, в каждом из которых уникальные лица со всем тегами, отфильтрованными до этого этапа
    xml_after_decomposing_by_indexes_into_lists = decomposing_xml_by_indexes_into_lists(xml_after_cut, xml_after_index)

    #for el in xml_after_decomposing_by_indexes_into_lists:
    #    print(el)

    #print('\n', '* ' * 50, '\n', 'Список [xml_after_cut] должен стать пустым: (НУЖЕН ТЕСТ?)', xml_after_cut, '\n', '* ' * 50)

    # Группируем лиц в словарь по видам заявлений (ЕПГУ, МФЦ, Физ лицо)
    groups_persons: dict[str, list] = distribution_of_persons_by_groups(xml_after_decomposing_by_indexes_into_lists)

    for k, v in groups_persons.items():
        print(k, v)

    person = Person()
    print(person.flag_old_data)

    for keys_types, values_list in groups_persons.items():
        for values in values_list:
            for el in values:
                # Если есть только старая фамилия
                if el.startswith('<CPLSurname'):
                    print(el)
                    person.CPLSurname.append([el])
                if el.startswith('<CPLName'):
                    print(el)
                    person.CPLName.append([el])
                if el.startswith('<CPLPatronymic'):
                    print(el)


    print('person.CPSurname: ', person.CPSurname)
    print('person.CPSurname: ', person.CPName)
    print('person.CPLSurname: ', person.CPLSurname)
    print('person.CPLSurname: ', person.CPLName)

    person.check_old_data()
    print(person.flag_old_data)
    # Если ТЕГ SPL, ты выводим пытемся сновы вывести на экра предыдущую строку, но сравнивая тэги...,
    # КАКие у нас старые данные?
    #Новая фамиля = Старая фамилия?
    # новая имя = новоия ? имя