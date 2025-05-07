from datetime import datetime

# 判断两个时间段是否重合
def checkIsOverlap(start1, end1, start2, end2):
    """
    判断两个时间段是否重合
    :param start1: 第一个时间段的开始时间，datetime 类型
    :param end1: 第一个时间段的结束时间，datetime 类型
    :param start2: 第二个时间段的开始时间，datetime 类型
    :param end2: 第二个时间段的结束时间，datetime 类型
    :return: 如果两个时间段重合返回 True，否则返回 False
    """
    return not (end1 < start2 or end2 < start1)