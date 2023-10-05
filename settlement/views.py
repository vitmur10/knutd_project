from .models import Hostel
from django.shortcuts import render, redirect
from .forms import StudentForm, StudentParentsForm
from django.http import Http404
from docx import Document
from datetime import datetime

from docx.shared import Pt, Cm

current_date = datetime.now()
formatted_month = current_date.strftime("%m")


def fill_order_document(template_path, output_path, data_to_fill, size, data):
    doc = Document(template_path)

    # Заповнення даними текстових параграфів
    for paragraph in doc.paragraphs:
        for key, value in data_to_fill.items():
            if key in paragraph.text:
                new_text = paragraph.text.replace(key, value)
                paragraph.text = new_text  # Замінюємо текст параграфу без використання run
                if paragraph.runs:
                    font = paragraph.runs[0].font
                    font.name = 'Times New Roman'
                    font.size = Pt(size)

    # Заповнення даними комірок таблиць

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data_to_fill.items():
                    if key in cell.text:
                        new_text = cell.text.replace(key, value)
                        cell.text = new_text  # Замінюємо текст комірки таблиці без використання run
                        if cell.paragraphs and cell.paragraphs[0].runs:
                            font = cell.paragraphs[0].runs[0].font
                            font.name = 'Times New Roman'
                            font.size = Pt(size)
                            # Виправлення відступів та розмірів комірки
                            cell.paragraphs[0].paragraph_format.left_indent = Cm(0.3)

    doc.save(output_path)


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        parent_form = StudentParentsForm(request.POST)
        if form.is_valid() and parent_form.is_valid():
            parent_form.save()
            form.save()
            data = form.cleaned_data
            print(form.cleaned_data)
            order_data_to_fill = {
                "м. Київ	  						«____»_______________20____р.": f"""м. Київ	  						"{current_date.day} {formatted_month} {current_date.year}" р.""",
                "виданий _____________________________________________________________________,": f"виданий                                            {data['IPI']}",
                "який (яка) навчається у __________________на денній формі навчання,": "який (яка) навчається у КНУТД на денній формі навчання,",
                "факультету _____________________________________,   _____курсу,    група___________,": f"{data['faculty']},   {data['course']} курсу,    група {data['group']},",
                " № ____ по вул. _______________, буд.": f" № {data['hostel']} по вул. {data['street']}, буд. house № room, кімната, блок, № bloc",
                "№ ___, кімната, блок, № _________ .": "",
                "Ордер дійсний протягом ___________ навчального року до ___.______________ 20_____р.": f"Ордер дійсний протягом {data['learning_from']}/{data['training_to']} навчального року до 30.06.{data['training_to']} р.",
                "_______________________________________________________,": f"                                                   {data['IPI']},",
                "який (яка) навчається у _______________ на денній формі навчання,": "який (яка) навчається у КНУТД на денній формі навчання,",
                "факультету __________, __________курсу, група_______________": f"{data['faculty']}, {data['course']} курсу, група {data['course']}",
                "на право займати ліжко-місце в гуртожитку №_____, кімнаті №___,": f"на право займати ліжко-місце в гуртожитку №{data['hostel']}, кімнаті №{'room'},",
                "Термін проживання до __________________20_____ року": f"Термін проживання до 30.06.{data['training_to']} року",
            }
            """            contract_data_to_fill = {
                " на	/	": f" на {[learning_from]}/{[training_to]}",
                "м. Київ	«	»	20	р.": f"м. Київ	«{current_date.day}» {formatted_month} {current_date.year} р.",
                "***********************************************************": f"{[IPI]}",
                "здобувача освіти факультету/інституту	група	курс	(далі — Наймач)": f"здобувача освіти факультету/інституту {[faculty]} група {[group]} курс {[course]} (далі — Наймач)",
                " в кімнаті №	у": f" в кімнаті №{room} у",
                "гуртожитку КНУТД №	, яке розташоване за адресою:	та зобов’язується провести ": f"гуртожитку КНУТД № {[hostel]}, яке розташоване за адресою: вул.{street} {house} та зобов’язується провести ",
                "Сплачувати за проживання. Оплата здійснюється авансовано за навчальний рік в сумі	гривень, без ПДВ.": f"Сплачувати за проживання. Оплата здійснюється авансовано за навчальний рік в сумі 10900 гривень, без ПДВ.",
                "Договір набуває чинності з   «     »	20           р. і діє до «      »	20 р": f"Договір набуває чинності з   «{current_date.day}» {formatted_month}. {current_date.year} р. і діє до «30» 06. {current_date.year + 1} р.",
                f"проживання в гуртожитку №  	": f"проживання в гуртожитку №  {[hostel]}",
                "Паспорт серія	№  	": f"Паспорт серія {[passport_series]} № {[passport_number]} ",
                "виданий «	»	20	р.": f"виданий «10»09 2020р. ",
                "ідентифікаційний код  	": f"ідентифікаційний код {[identification_code]}",
                "index, obl": f"38541 Хмельницька",
                "city": f"Старокостнятинів",
                " вулиця будинок квартира": f"вул. Лейпцезька 16 708",
                "?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????": f"{[IPIF]}",
                "паспорт серія батьки	№ батьки	виданий  батьки	": f"паспорт серія {[passport_series_f]} № {[passport_number_f]} виданий {[passport_issued_f]}",
            }"""
            fill_order_document('ORDER.docx', f"заповнений_ордер{data['IPI']}.docx", order_data_to_fill, 12, data)
            # fill_order_document(contract_template_path, contract_output_path, contract_data_to_fill, 8, data)
    else:
        form = StudentForm()
        parent_form = StudentParentsForm()

    return render(request, 'swttlement/form.html', {'form': form,
                                                    'parent_form': parent_form})


def dormitories(request):
    try:
        h = Hostel.objects.all()
    except:
        raise Http404('Сталася помилка(')
    return render(request, 'swttlement/dormitories.html', {'hostel': h})


def hostel(request):
    return render(request, 'swttlement/hostel.html')
