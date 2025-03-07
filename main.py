from xml_tags import tags
import re


def cut_tag(tag):
    """
    Принимаем тег и его содержимое, удалям тег, возвращаем содержимое
    :param tag:
    :return: содержимое тега (без тега)
    """
    return re.sub(r"<.*?>", "", tag)

def cut_date_birth(date_birth):
    """
    Принимаем тег CPBirthday и его содержимое в виде ДД.ММ.ГГГГ или ДД-ММ-ГГГГ, удалям тег, возвращаем только ГГГГ
    :param tag:
    :return: содержимое тега в виде ГГГГ
    """

    search_date = re.search(r'\d{4}$', date_birth)
    if search_date:
        return search_date.group(0)
    else:
        print(search_date)
        raise SyntaxError("Ошибка. Неверный формат даты?")


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
                 type_request=None,     # Тип обращений на сайт Гос. услуг (МФЦ | ЕПГУ | Физ лицо)
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
            self.CPLSurname = list(CPLSurname)
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
        if type_request is None:
            self.type_request = []
        else:
            self.type_request = list(type_request)

        self.flag_old_data = flag_old_data

    def check_old_data(self):
        """
        Если есть старые ФИО - то флаг ставится в True
        """
        if (len(self.CPLSurname) or len(self.CPLName) or len(self.CPLPatronymic)) > 0:
            self.flag_old_data = True

    def set_CPSurname(self, first_surname):
        """
        Установить фамилию
        """
        self.CPSurname.append(cut_tag(first_surname))

    def set_CPName(self, first_name):
        """
        Установить имя
        """
        self.CPName.append(cut_tag(first_name))

    def set_CPPatronymic(self, first_patronymic):
        """
        Установить отчество
        """
        self.CPPatronymic.append(cut_tag(first_patronymic))

    def set_CPLSurname(self, last_surname):
        """
        Установить старые фамилии (возможно несколько)
        """
        self.CPLSurname.append(cut_tag(last_surname))

    def set_CPLName(self, last_name):
        """
        Установить старые имена (возможно несколько)
        """
        self.CPLName.append(cut_tag(last_name))

    def set_CPLPatronymic(self, last_patronymic):
        """
        Установить старые отчества (возможно несколько)
        """
        self.CPLPatronymic.append(cut_tag(last_patronymic))

    def set_CPBirthday(self, first_birthday):
        """
        Установить дату рождения в формате ГГГГ
        """
        self.CPBirthday.append(cut_date_birth(cut_tag(first_birthday)))

    def set_type_request(self, type_req):
        """
        Установить старые фамилии (возможно несколько)
        """
        self.type_request.append(type_req)


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
    print('xml_after_open_and_strip: ', xml_after_open_and_strip)

    # Проверяем XML-файл
    check_xml(xml_after_open_and_strip)

    # Обрезаем XML-файл
    xml_after_cut = cut_xml(xml_after_open_and_strip, tags)
    print('xml_cut: ', xml_after_cut)

    # Создаем список с индексами по обрезанному XML-файл по тегу <Applicant type=>
    xml_after_index: list[int] = index_xml(xml_after_cut)
    print('xml_after_index: ', xml_after_index)

    # Создаем список списков, в каждом из которых уникальные лица со всем тегами, отфильтрованными до этого этапа
    xml_after_decomposing_by_indexes_into_lists = decomposing_xml_by_indexes_into_lists(xml_after_cut, xml_after_index)
    #print('xml_after_decomposing_by_indexes_into_lists: ', xml_after_decomposing_by_indexes_into_lists)

    for el in xml_after_decomposing_by_indexes_into_lists:
        print(el)

    #print('\n', '* ' * 50, '\n', 'Список [xml_after_cut] должен стать пустым: (НУЖЕН ТЕСТ?)', xml_after_cut, '\n', '* ' * 50)

    # Группируем лиц в словарь по видам заявлений (ЕПГУ, МФЦ, Физ лицо)
    #groups_persons: dict[str, list] = distribution_of_persons_by_groups(xml_after_decomposing_by_indexes_into_lists)

    #for k, v in groups_persons.items():
    #    print(k, v)

    for line in xml_after_decomposing_by_indexes_into_lists:
        print('----------------------')
        person = Person()
        for el in line:
            # print(person.flag_old_data)
            if el.startswith('<Applicant type="Единый портал гос.услуг"'):
                # print(el)
                person.set_type_request('ЕПГУ')
            if el.startswith('<CPSurname'):
                # print(el)
                person.set_CPSurname(el)
            if el.startswith('<CPName'):
                # print(el)
                person.set_CPName(el)
            if el.startswith('<CPPatronymic'):
                # print(el)
                person.set_CPPatronymic(el)
            if el.startswith('<CPLSurname'):
                # print(el)
                person.set_CPLSurname(el)
            if el.startswith('<CPLName'):
                # print(el)
                person.set_CPLName(el)
            if el.startswith('<CPLPatronymic'):
                # print(el)
                person.set_CPLPatronymic(el)
            if el.startswith('<CPBirthday'):
                # print(el)
                person.set_CPBirthday(el)

        print('person.type_request: ', person.type_request)
        print('person.CPSurname: ', person.CPSurname)
        print('person.CPName: ', person.CPName)
        print('person.CPPatronymic: ', person.CPPatronymic)
        print('person.CPLSurname: ', person.CPLSurname)
        print('person.CPLName: ', person.CPLName)
        print('person.CPLPatronymic: ', person.CPLPatronymic)
        print('person.CPBirthday: ', person.CPBirthday)

    """
    for keys_types, values_list in groups_persons.items():
        for values in values_list:
            person = Person()
            #print(person.flag_old_data)
            print('----------------------')
            for el in values:
                if el.startswith('<CPSurname'):
                    #print(el)
                    person.set_CPSurname(el)
                if el.startswith('<CPName'):
                    #print(el)
                    person.set_CPName(el)
                if el.startswith('<CPPatronymic'):
                    #print(el)
                    person.set_CPPatronymic(el)
                if el.startswith('<CPLSurname'):
                    #print(el)
                    person.set_CPLSurname(el)
                if el.startswith('<CPLName'):
                    #print(el)
                    person.set_CPLName(el)
                if el.startswith('<CPLPatronymic'):
                    #print(el)
                    person.set_CPLPatronymic(el)
                if el.startswith('<CPBirthday'):
                    #print(el)
                    person.set_CPBirthday(el)

            print('person.CPSurname: ',      person.CPSurname)
            print('person.CPName: ',         person.CPName)
            print('person.CPPatronymic: ',   person.CPPatronymic)
            print('person.CPLSurname: ',     person.CPLSurname)
            print('person.CPLName: ',        person.CPLName)
            print('person.CPLPatronymic: ',  person.CPLPatronymic)
            print('person.CPBirthday: ',     person.CPBirthday)
    """
            #person.check_old_data()
            #print(person.flag_old_data)
    # Если ТЕГ SPL, ты выводим пытемся сновы вывести на экра предыдущую строку, но сравнивая тэги...,
    # КАКие у нас старые данные?
    #Новая фамиля = Старая фамилия?
    # новая имя = новоия ? имя