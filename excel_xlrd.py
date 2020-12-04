import json

import xlrd
import xlsxwriter as xlsxwriter
import xlwt


def readexcel(FileName):
    allData = {}

    workbook = xlrd.open_workbook(FileName)

    sheets = workbook.sheets()

    names = workbook.sheet_names()

    for i in range(len(sheets)):

        sheet_name = names[i]

        sheet = sheets[i]

        nrows = sheet.nrows

        # 正常数据title
        normal_title = sheet.row_values(0)
        # 异常数据title
        err_title = sheet.row_values(nrows - 2)
        # 最终的数据列表
        data = []
        # 从第1行开始遍历循环所有行，获取每行的数据
        for i in range(1, nrows):

            # 异常数据
            if i >= nrows - 1:
                row_data = sheet.row_values(i)
                # 组建每一行数据的字典
                row_data_dict = {}

                # 遍历行数据的每一项，赋值进行数据字典
                for j in range(len(row_data)):
                    item = row_data[j]
                    row_data_dict[err_title[j]] = item
            else:
                row_data = sheet.row_values(i)
                # 组建每一行数据的字典
                row_data_dict = {}

                # 遍历行数据的每一项，赋值进行数据字典
                for j in range(len(row_data)):
                    item = row_data[j]
                    row_data_dict[normal_title[j]] = item

            # 将行数据字典加入到data列表中
            data.append(row_data_dict)

        first = data[0]
        item = data[len(data) - 1]
        itemTitle = data[len(data) - 2]
        # 删除异常数据
        data.remove(item)
        # 删除异常title
        data.remove(itemTitle)

        new_row_data_dict = {}

        # 重新组装异常数据
        for key in first.keys():

            value = item.get(key)

            if value:
                new_row_data_dict[key] = value
                item.pop(key)
            else:
                # 数据未空也添加
                new_row_data_dict[key] = "null"

        # 未获取到的数据添加到尾部
        for key in item.keys():
            new_row_data_dict[key] = item.get(key)

        data.append(new_row_data_dict)

        allData[sheet_name] = data

    book = xlsxwriter.Workbook('111111.xls')  # 创建一个工作簿

    for allkey in allData.keys():
        value = allData[allkey]
        sheet = book.add_worksheet(allkey)

        for i in range(len(value)):
            row_data = value[i]
            a = 0

            for key in row_data.keys():
                sheet.write(0, a, key)

                if i == len(value) - 1:
                    # 添加一行title
                    sheet.write(i+1, a, key)
                    sheet.write(i+2, a, row_data.get(key))
                else:
                    sheet.write(i+1, a, row_data.get(key))
                a += 1

    book.close()


if __name__ == '__main__':
    readexcel(r'HUAWEI.xlsx')
