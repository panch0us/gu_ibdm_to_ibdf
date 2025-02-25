"""
Фильтр тегов XML-файла, которые не должны попасть в файл перед итоговой обработкой
"""

tag_filter = {
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<NaturalPerson>',
    '<List>',
    '<ListID>',
    '<ListTime>',
    '<ListItem>',
    '<Document>',
    '<DocumentID>',
    '<Procedure>',
    '<NaturalPerson>',
    '<Surname>',
}