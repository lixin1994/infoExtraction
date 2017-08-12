from party_name_extraction import process_html, download_file, get_party_names, get_list_of_party_names


print(get_list_of_party_names('COL.txt', 2000))

# import xlsxwriter


# result = open('result.txt')
# data_lines = result.readlines()
# workbook = xlsxwriter.Workbook('data.xlsx')
# worksheet = workbook.add_worksheet()
# row = 0
# for line in data_lines:
# 	content = line.split(',')
# 	col = 0
# 	for i in content:
# 	    worksheet.write(row, col, i)
# 	    col+=1
# 	row += 1