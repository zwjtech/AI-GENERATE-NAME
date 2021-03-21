#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
from matplotlib import pyplot as plt
import matplotlib
print(12.23//6)
print("你好，世界")

#保留小数位
a = 1
b = 3
print(a/b)
#方法一：
print(round(a/b,2))
#方法二：
print(format(float(a)/float(b),'.2f'))
#方法三：
print ('%.2f' %(a/b))

def divide_calclate(x1,y1,x2,y2,m,n):
   "x1,y1表示左上坐标，x2,y2表示右下坐标，m表示横切数，n表示竖切数"
   xLen = abs(x1-x2)
   yLen = abs(y1-y2)

   result = {
       "points":[]
   }

   # 传入同一个点
   if xLen == 0 and yLen == 0 :
       result["points"].append({
           "position": "1",
           "x": x1,
           "y": y2
             })
       return result
   elif xLen == 0 and yLen > 0:
      # 横坐标相同，分割众坐标
      y_dult = round(yLen/m,8)

      if y1 < y2 :
          result["points"].append({
              "position": 0,
              "x": x1,
              "y": y1
          })
          for i in range(1, m):
              y_i = i * y_dult + y1
              result["points"].append({
               "position": i,
               "x": x1,
               "y": y_i
             })
          result["points"].append({
              "position": m,
              "x": x1,
              "y": y2
          })
      else :
          result["points"].append({
              "position": 0,
              "x": x1,
              "y": y2
          })
          for i in range(1, m):
              y_i = i * y_dult + y2
              result["points"].append({
                  "position": i,
                  "x": x1,
                  "y": y_i
              })
          result["points"].append({
              "position": m,
              "x": x1,
              "y": y1
          })
      return result
   elif xLen > 0 and yLen == 0:
       # 纵坐标相同，分割横坐标
       x_dult = round(xLen / n, 8)

       if x1 < x2:
           result["points"].append({
               "position": 0,
               "x": x1,
               "y": y1
           })
           for i in range(1, n):
               x_i = i * x_dult + x1
               result["points"].append({
                   "position": i,
                   "x": x_i,
                   "y": y1
               })
           result["points"].append({
               "position": n,
               "x": x2,
               "y": y2
           })
       else:
           result["points"].append({
               "position": 0,
               "x": x2,
               "y": y2
           })
           for i in range(1, n):
               x_i = i * x_dult + x2
               result["points"].append({
                   "position": i,
                   "x": x_i,
                   "y": y1
               })
           result["points"].append({
               "position": n,
               "x": x1,
               "y": y1
           })
       return result

   else :
       # ，分割众坐标
       y_dult = round(yLen / m, 8)
       # ，分割横坐标
       x_dult = round(xLen / n, 8)
       #先支持这种输入
       if x1 < x2:
           if y1 > y2:
               for i in range(0, m) :
                   for j in range(0, n) :
                        lty = y1 - i * y_dult
                        ltx = j * x_dult + x1
                        ltx1 = (j + 1) * x_dult + x1
                        lty1 = y1 - (i + 1) * y_dult

                        #ltx < x2 and lty >y2 and ltx1 <x2 and lty1 >y2:
                        #第一个点在范围内
                        if ltx < x2 and lty > y2 :
                            # 在右下点范围内
                            if ltx1 < x2 and lty1 > y2 :
                                result["points"].append({
                                    "group_index": str(i)+"*"+str(j),
                                    "position": "left_top",
                                    "x": ltx,
                                    "y": lty
                                   })
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "right_bottom",
                                    "x": ltx1,
                                    "y": lty1
                                })
                            # 第二个点横坐标超过，纵坐标不超
                            elif ltx1 > x2 and lty1 > y2 :
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "left_top",
                                    "x": ltx,
                                    "y": lty
                                })
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "right_bottom",
                                    "x": x2,
                                    "y": lty1
                                })
                            # 第二个点纵坐标超过
                            elif ltx1 < x2 and lty1 < y2:
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "left_top",
                                    "x": ltx,
                                    "y": lty
                                })
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "right_bottom",
                                    "x": ltx1,
                                    "y": y2
                                })
                                # 第二个点坐标超过
                            elif ltx1 > x2 and lty1 < y2:
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "left_top",
                                    "x": ltx,
                                    "y": lty
                                })
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "right_bottom",
                                    "x": x2,
                                    "y": y2
                                })
                        #第一个点横坐标超出
                        elif ltx > x2 and lty > y2 :
                            result["points"].append({
                                "group_index": str(i) + "*" + str(j+1),
                                "position": "left_top",
                                "x": (j-1) * x_dult + x1,
                                "y": lty
                            })
                            if lty1 > y2:
                               result["points"].append({
                                "group_index": str(i) + "*" + str(j+1),
                                "position": "right_bottom",
                                "x": x2,
                                "y": lty1
                              })
                            else:
                                result["points"].append({
                                    "group_index": str(i) + "*" + str(j),
                                    "position": "right_bottom",
                                    "x": x2,
                                    "y": y2
                                })
                        elif ltx < x2 and lty < y2 :
                            {}
               return result
           else :
                return {}
       else :
           return {}



re = divide_calclate(0,10,11,0,20,20)
print(str(re))
print(json.dumps(re))



font = {'family':"Microsoft Yahei",'size':'10'}

matplotlib.rc("font",**font)
_y=[]
_x=[]
for i in re["points"]:
    _y.append(i["y"])
    _x.append(i["x"])

#设置图形大小
plt.figure(figsize=(20,8),dpi=80)

#使用scatter方法绘制散点图,和之前绘制折线图的唯一区别
plt.scatter(_x , _y)

#添加图例
plt.legend(loc="upper left")
#添加描述信息
plt.xlabel("y")
plt.ylabel("x")
plt.title("标题")

#展示
plt.show()