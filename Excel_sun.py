import xlrd
from xlutils.copy import copy

exel1 = "D:/software/QQ/Record/457361577/FileRecv/阳光一小班级花名册2018.9 - 副本.xls"
exel2 = "D:/software/QQ/Record/457361577/FileRecv/双十贫困数据库 - 副本 (2).xls"

exel_out_name = "D:/software/QQ/Record/457361577/FileRecv/阳光_贫困_比较结果.xls"

# 所有贫困人
pools = []
workbook = xlrd.open_workbook(exel2)
pool_sheet = workbook.sheet_by_name('贫困户信息_1')
pool_id = pool_sheet.col_values(0)
pool_id = pool_id[3:]
pool_id = [str(_) for _ in pool_id]
pool_id = [_.replace(".0", '') for _ in pool_id]
pool_shenfen = pool_sheet.col_values(8)
pool_shenfen = pool_shenfen[3:]
pool_shenfen = [_.replace("'", '') for _ in pool_shenfen]
pool_shenfen = [_.replace("\n", '') for _ in pool_shenfen]
pool_shenfen = [_.replace("\t", '') for _ in pool_shenfen]
pool_shenfen = [_.replace(" ", '') for _ in pool_shenfen]
pool_shenfen = [_.upper() for _ in pool_shenfen]

pool_name = pool_sheet.col_values(7)
pool_name = pool_name[3:]

for i in range(len(pool_id)):
    pools.append((pool_id[i], pool_name[i], pool_shenfen[i]))

# 读取阳光，并且准备结果文件
sun_workbook = xlrd.open_workbook(exel1)
sun_out = copy(sun_workbook)
sheet_out = sun_out.get_sheet('班级花名册')
sun_sheet = sun_workbook.sheet_by_name('班级花名册')
sun_name = sun_sheet.col_values(4)
sun_name = sun_name[1:]
sun_shenfen = sun_sheet.col_values(9)
sun_shenfen = sun_shenfen[1:]

sun_shenfen = [_.replace("'", '') for _ in sun_shenfen]
sun_shenfen = [_.replace("\n", '') for _ in sun_shenfen]
sun_shenfen = [_.replace("\t", '') for _ in sun_shenfen]
sun_shenfen = [_.replace(" ", '') for _ in sun_shenfen]
sun_shenfen = [_.upper() for _ in sun_shenfen]

assert (len(sun_shenfen) == len(sun_name))
for i in range(len(sun_shenfen)):
    print(i)
    name = sun_name[i]
    shenfen = sun_shenfen[i]

    # 是否匹配
    isMatch = False

    # 查找是否有身份证号和名字都相同的
    for (pid, pname, pshenfen) in pools:
        # 如果身份证号码和名字都相等
        if (pname == name and pshenfen == shenfen):
            # 身份证号码和姓名是否都相同
            sheet_out.write(i + 1, 29, '是')
            # 都一致匹配行
            sheet_out.write(i + 1, 30, pid)
            # 姓名匹配行
            sheet_out.write(i + 1, 31, pid)
            # 身份证号匹配行
            sheet_out.write(i + 1, 32, pid)

            isMatch = True
            break

    # 如果没有匹配，统计姓名和身份证号单独匹配的个数
    if (not isMatch):
        sheet_out.write(i + 1, 29, '否')
        same_name_ids = []
        same_shenfe_ids = []
        for (pid2, pname2, pshenfen2) in pools:
            if (pname2 == name):
                same_name_ids.append(pid2)
            if (pshenfen2 == shenfen):
                same_shenfe_ids.append(pid2)

        # 都一致匹配行
        sheet_out.write(i + 1, 30, '无')
        # 姓名匹配行
        if (len(same_name_ids) > 0):
            sheet_out.write(i + 1, 31, str(','.join(same_name_ids)))
        else:
            sheet_out.write(i + 1, 31, '无')
        # 身份证号匹配行
        if (len(same_shenfe_ids) > 0):
            sheet_out.write(i + 1, 32, str(','.join(same_shenfe_ids)))
        else:
            sheet_out.write(i + 1, 32, '无')

sun_out.save(exel_out_name)
