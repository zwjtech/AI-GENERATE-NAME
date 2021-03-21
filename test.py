from name import Name


temp=Name("王","卧槽","男")
temp2=Name("王","卧操","男")
temp3=Name("王","卧擦","男")

print(temp==temp2)
print(temp==temp3)


a = 123.123121
b = 13
print(a/b)
#方法一：
print(round(a/b,6))
#方法二：
print(format(float(a)/float(b),'.6f'))
#方法三：
print ('%.6f' %(a/b))