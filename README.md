# Задание №3 (Вариант 15)

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на языке json принимается из файла, путь к которому задан
ключом командной строки. Выходной текст на учебном конфигурационном
языке попадает в файл, путь к которому задан ключом командной строки.
Однострочные комментарии:
% Это однострочный комментарий
Многострочные комментарии:
/#
Это многострочный
комментарий
#/
Массивы:
[ значение, значение, значение, ... ]
Словари:
{
 имя => значение,
 имя => значение,
 имя => значение,
 ...
}
Имена:
76
[a-zA-Z][a-zA-Z0-9]*
Значения:
• Числа.
• Строки.
• Массивы.
• Словари.
Строки:
'Это строка'
Объявление константы на этапе трансляции:
def имя := значение
Вычисление константы на этапе трансляции:
!(имя)
Результатом вычисления константного выражения является значение.
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2
примера описания конфигураций из разных предметных областей

<table>
  <tr>
    <td>
      <img src="Image/конф_3_image1.png" alt="Json-файл" width="300">
    </td>
    <td>
      <img src="Image/Конф_3_image2.png" alt="test.conf" width="300">
    </td>
  </tr>
</table>

Тесты:

![image](https://github.com/user-attachments/assets/6f3c7ce5-74dc-40e1-a7fc-3cfff3361eb9)
