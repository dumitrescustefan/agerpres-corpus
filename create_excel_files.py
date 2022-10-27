import os, sys, json
import xlsxwriter

DOMAINS = ['politica', 'social', 'cultura', 'regionale', 'economic-intern', 'justitie', 'educatie-stiinta', 'eveniment', 'sanatate', 'mediu', 'politica-externa', 'romania-in-lume', 'stiintatehnica', 'economic-extern', 'mondorama', 'life', 'planeta']
NUMBER_OF_NEWS_PER_CATEGORY = 100


def write_excel(domain, data):
    filename = f"data/{domain}.xlsx"
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    row_format = cell_format = workbook.add_format()
    row_format.set_bottom(1)
    row_format.set_bottom_color('#aaaaaa')
    row_format.set_bg_color('#ffffff')
    row_format.set_align('vcenter')
    row_format.set_text_wrap()

    header_row_format = cell_format = workbook.add_format()
    header_row_format.set_bottom(1)
    header_row_format.set_bottom_color('#666666')
    header_row_format.set_bg_color('#CCCCCC')
    header_row_format.set_bold(True)
    header_row_format.set_align('vcenter')
    header_row_format.set_text_wrap()

    alt_row_format = cell_format = workbook.add_format()
    alt_row_format.set_bottom(1)
    alt_row_format.set_bottom_color('#aaaaaa')
    alt_row_format.set_bg_color('#f0faff')
    alt_row_format.set_align('vcenter')
    alt_row_format.set_text_wrap()

    bold = workbook.add_format({'bold': True})
    not_bold = workbook.add_format({'bold': False})
    wrap_1 = workbook.add_format({'text_wrap': True, 'bg_color': '#FFFFFF', 'align': 'top'})
    wrap_2 = workbook.add_format({'text_wrap': True, 'bg_color': '#e3ffd5', 'align': 'top'})

    cell_format = workbook.add_format()
    cell_format.set_right(1)
    cell_format.set_right_color('#dddddd')
    cell_format.set_bottom(1)
    cell_format.set_bottom_color('#aaaaaa')
    cell_format.set_align('vcenter')
    cell_format.set_text_wrap()

    alt_cell_format = workbook.add_format()
    alt_cell_format.set_right(1)
    alt_cell_format.set_right_color('#dddddd')
    alt_cell_format.set_bg_color('#f0faff')
    alt_cell_format.set_bottom(1)
    alt_cell_format.set_bottom_color('#aaaaaa')
    alt_cell_format.set_align('vcenter')
    alt_cell_format.set_text_wrap()

    alt_cell_format_bold = alt_cell_format
    alt_cell_format_bold.set_bold()

    data_format1 = workbook.add_format({'bg_color': '#FFFFFF'})
    data_format2 = workbook.add_format({'bg_color': '#e3ffd5'})

    #worksheet.set_default_row(20)
    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 100)
    worksheet.set_column('C:C', 80)


    worksheet.write(0, 0, "#")
    worksheet.write(0, 1, "ARTICOL")
    worksheet.write(0, 2, "REZUMAT")
    worksheet.set_row(0, cell_format=header_row_format)
    #worksheet.set_row(0, bold)

    row = 1
    # data is a list of dicts
    for index, article in enumerate(data):
        title = article['title'].strip()+"\n\n"
        text = article['content']
        text = text[:text.find("AGERPRES")]
        text = text.replace("\n\n\n", "\n\n")



        if index % 2 != 0:
            worksheet.set_row(row, cell_format=data_format1)
            worksheet.write(row, 0, str(index + 1), wrap_1)
            worksheet.write_rich_string(row, 1, bold, title, not_bold, text, wrap_1)
            worksheet.write(row, 2, "", wrap_1)
        else:
            worksheet.set_row(row, cell_format=data_format2)
            worksheet.write(row, 0, str(index + 1), wrap_2)
            worksheet.write_rich_string(row, 1, bold, title, not_bold, text, wrap_2)
            worksheet.write(row, 2, "", wrap_2)

        row += 1

    workbook.close()
    print(f"*** Domain {domain} done. ***")

# load data
os.makedirs("data",exist_ok=True)
data = {}
for domain in DOMAINS:
    file = f'selected_{domain}.json'
    if os.path.exists(file):
        with open(file, 'r', encoding="utf8") as f:
            data[domain] = json.load(f)
        write_excel(domain, data[domain])
    else:
        print(f"\tDomain {domain} does not exist!")

