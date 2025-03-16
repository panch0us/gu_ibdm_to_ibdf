from xml_tags import tags
import re

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

def split_tag_into_parts(bind_xml_after_cut):
    """
    Проверяем XML-файл на наличие тега: <CP*> Иванов ,  Петров </CPL*>
    Если такой тег есть, то разделяем его на два таких тега:
    <CP*>Иванов</CP*>
    <CP*>Петров</CP*>
    :return: list тегами
    """
    # Регулярное выражение для поиска тегов, начинающихся на <CP и заканчивающихся на </CP
    pattern = r"(<CP[^>]+>)(.*?)(</CP[^>]+>)"

    _new_list = bind_xml_after_cut

    for num, line in enumerate(_new_list):
        if line.startswith('<CP') and ',' in line:
            my_match = re.search(pattern, line)

            if my_match:
                # Извлекаем открывающий тег, содержимое и закрывающий тег
                open_tag, content, close_tag = my_match.groups()
                # Разделяем содержимое по запятой
                parts = [part.strip() for part in content.split(",")]
                # Формируем новые строки
                output_strings = [f"{open_tag}{part}{close_tag}" for part in parts]

                _new_list[num:num+1] = output_strings
            else:
                print("Теги не найдены.")
    return _new_list

def index_xml(bind_xml_after_cut) -> list[int]:
    """
    По обрезанному XML-файлу находим тег <Applicant type=> и в отдельном списке проставляем по этому тегу индексы.
    Инверсируем этот список.
    :param bind_xml_after_cut:
    :return: Инверсированный список индексов по тегу <Applicant type=> из обрезанного XML-файла
    """
    return [index for index, tag in enumerate(bind_xml_after_cut) if tag.startswith('<Applicant type=')][::-1]

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

def add_person_to_dict(bind_xml_after_decomposing_by_indexes_into_lists):
    """
    Добавляем всех лиц в словарь
    :param bind_xml_after_decomposing_by_indexes_into_lists:
    :return: словарь вида {'ЕПГУ': [], 'МФЦ': [], 'ФЛ': []}
    """
    _persons_dict = {'ЕПГУ': [], 'МФЦ': [], 'ФЛ': []}

    for line in bind_xml_after_decomposing_by_indexes_into_lists:
        person = Person()
        for el in line:
            if el.startswith('<Applicant type="Единый портал гос.услуг"'):
                person.set_type_request('ЕПГУ')
            if el.startswith('<Applicant type="МФЦ"'):
                person.set_type_request('МФЦ')
            if el.startswith('<Applicant type="Физическое лицо"'):
                person.set_type_request('ФЛ')
            if el.startswith('<CPSurname'):
                person.set_CPSurname(el)
            if el.startswith('<CPName'):
                person.set_CPName(el)
            if el.startswith('<CPPatronymic'):
                person.set_CPPatronymic(el)
            if el.startswith('<CPLSurname'):
                person.set_CPLSurname(el)
            if el.startswith('<CPLName'):
                person.set_CPLName(el)
            if el.startswith('<CPLPatronymic'):
                person.set_CPLPatronymic(el)
            if el.startswith('<CPBirthday'):
                person.set_CPBirthday(el)
        if person.type_request == ['ЕПГУ']:
            _persons_dict['ЕПГУ'].append(person)
        if person.type_request == ['МФЦ']:
            _persons_dict['МФЦ'].append(person)
        if person.type_request == ['ФЛ']:
            _persons_dict['ФЛ'].append(person)

    return _persons_dict

def classify_text_by_query_type():
    """
    Распределение итогового текста на 3 группы (ЕПГУ | Физ лицо | МФЦ)
    :return:
    """
    text_epgu = ''
    text_fl = ''
    text_mfc = ''

    for key, value in persons_dict.items():
        if key == 'ЕПГУ' and len(value) > 0:
            text_epgu = create_text(persons_dict['ЕПГУ'])
        if key == 'МФЦ' and len(value) > 0:
            text_mfc = create_text(persons_dict['МФЦ'])
        if key == 'ФЛ' and len(value) > 0:
            text_fl = create_text(persons_dict['ФЛ'])

    print('text_epgu: \n', text_epgu, sep='')
    print('text_mfc: \n', text_mfc, sep='')
    print('text_fl: \n', text_fl, sep='')

######## Вспомогательные функции и классы ########

def cut_tag_and_lower_text(tag):
    """
    Принимаем тег и его содержимое, удалям тег, переводим содержимое в нижний регистр, возвращаем содержимое
    :param tag:
    :return: содержимое тега в нижнем регистре (без тега)
    """
    return re.sub(r"<.*?>", "", tag).strip().lower()

def cut_date_birth(date_birth):
    """
    Принимаем тег CPBirthday и его содержимое в виде ДД.ММ.ГГГГ или ДД-ММ-ГГГГ, удалям тег, возвращаем только ГГГГ
    :param date_birth:
    :return: содержимое тега в виде ГГГГ
    """

    search_date = re.search(r'\d{4}$', date_birth)
    if search_date:
        return search_date.group(0)
    else:
        print(search_date)
        raise SyntaxError("Ошибка. Неверный формат даты?")

def create_text(bind_persons_dict):
    """
    Создает итоговый текст с нужным форматом фамилия;имя;отчество;чч;мм;гггг;;
    :param bind_persons_dict: список лиц
    :return: итоговый текст
    """
    _text = ''

    for prs in bind_persons_dict:
        #### Если у лица есть Фамилия или Имя или Отчество (нет старых ФИО)
        for sn in prs.CPSurname:
            _text = _text + sn + ';'
        for nm in prs.CPName:
            _text = _text + nm + ';'
        for pn in prs.CPPatronymic:
            _text = _text + pn + ';'
        for bd in prs.CPBirthday:
            _text = _text + bd + ';;\n'

        #### Если у лица есть старые Фамилия, Имя и Отчество
        if len(prs.CPLSurname) > 0 and len(prs.CPLName) > 0 and len(prs.CPLPatronymic) > 0:
            for ls in prs.CPLSurname:
                for ln in prs.CPLName:
                    for lpn in prs.CPLPatronymic:
                        for bd in prs.CPBirthday:
                            _text = _text + f'{ls};{ln};{lpn};{bd};;\n'

        #### Если у лица есть только старые Фамилия и Имя
        elif len(prs.CPLSurname) > 0 and len(prs.CPLName) > 0:
            for ls in prs.CPLSurname:
                for ln in prs.CPLName:
                    for pn in prs.CPPatronymic:
                        for bd in prs.CPBirthday:
                            _text = _text + f'{ls};{ln};{pn};{bd};;\n'

        #### Если у лица есть только старая Фамилия
        elif len(prs.CPLSurname) > 0:
            for ls in prs.CPLSurname:
                for nm in prs.CPName:
                    for pn in prs.CPPatronymic:
                        for bd in prs.CPBirthday:
                            _text = _text + f'{ls};{nm};{pn};{bd};;\n'
    return _text

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
                 type_request=None,     # Тип обращений на сайт государственных услуг (МФЦ | ЕПГУ | Физ лицо)
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


    def set_CPSurname(self, first_surname):
        """
        Установить фамилию
        """
        self.CPSurname.append(cut_tag_and_lower_text(first_surname))

    def set_CPName(self, first_name):
        """
        Установить имя
        """
        self.CPName.append(cut_tag_and_lower_text(first_name))

    def set_CPPatronymic(self, first_patronymic):
        """
        Установить отчество
        """
        self.CPPatronymic.append(cut_tag_and_lower_text(first_patronymic))

    def set_CPLSurname(self, last_surname):
        """
        Установить старые фамилии (возможно несколько)
        """
        self.CPLSurname.append(cut_tag_and_lower_text(last_surname))

    def set_CPLName(self, last_name):
        """
        Установить старые имена (возможно несколько)
        """
        self.CPLName.append(cut_tag_and_lower_text(last_name))

    def set_CPLPatronymic(self, last_patronymic):
        """
        Установить старые отчества (возможно несколько)
        """
        self.CPLPatronymic.append(cut_tag_and_lower_text(last_patronymic))

    def set_CPBirthday(self, first_birthday):
        """
        Установить дату рождения в формате ГГГГ
        """
        self.CPBirthday.append(cut_date_birth(cut_tag_and_lower_text(first_birthday)))

    def set_type_request(self, type_req):
        """
        Установить тип запроса из сайта (МФЦ | ЕПГУ | Физ лицо)
        """
        self.type_request.append(type_req)



if __name__ == '__main__':
    # Открываем XML-файл
    xml_after_open_and_strip = open_and_strip_xml()
    #print('xml_after_open_and_strip: ', xml_after_open_and_strip)

    # Проверяем XML-файл
    check_xml(xml_after_open_and_strip)

    # Обрезаем XML-файл
    xml_after_cut = cut_xml(xml_after_open_and_strip, tags)
    #print('xml_cut: ', xml_after_cut)

    xml_after_split_tag_into_parts = split_tag_into_parts(xml_after_cut)
    #print('xml_after_split_tag_into_parts: ', xml_after_split_tag_into_parts)

    # Создаем список с индексами по обрезанному XML-файл по тегу <Applicant type=>
    xml_after_index: list[int] = index_xml(xml_after_split_tag_into_parts)
    #print('xml_after_index: ', xml_after_index)

    # Создаем список списков, в каждом из которых уникальные лица со всем тегами, отфильтрованными до этого этапа
    xml_after_decomposing_by_indexes_into_lists = decomposing_xml_by_indexes_into_lists(xml_after_cut, xml_after_index)
    #print('xml_after_decomposing_by_indexes_into_lists: ', xml_after_decomposing_by_indexes_into_lists)

    # Создаем словарь с группами (тип заявления: список лиц)
    persons_dict = add_person_to_dict(xml_after_decomposing_by_indexes_into_lists)

    # Распределение итогового текста на 3 группы (ЕПГУ | Физ лицо | МФЦ)
    classify_text_by_query_type()