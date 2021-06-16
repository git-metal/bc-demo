# -*- coding:utf-8 -*-

import csv

# utf-8-sig
with open('test.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["姓名", "年龄", "性别"])
    csv_writer.writerow(['a', '18', '男,1,2,3'])
    csv_writer.writerow(['b', '18', '男'])
    csv_writer.writerow(['c', '19', '女'])

print("end")
