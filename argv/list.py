list = []                      #definerar listan
print(len(list))               #skriver längden av listan (alltid 0)
list.append("zzz")             #lägger till i lista
list.append("pelle svanslös")  #lägger till i lista
print(list[0])                 #skriver första saken i listan (zzz)
print(list[1])                 #skriver andra saken i listan (pelle svanslös)
list[-1] = "INTE PELLE"        #gör om sista indexen till "INTE PELLE"
print(list)                    #skriver ut hela listan (zzz, INTE PELLE)

list[0] = "inte zzz"           #gör om första indexen till "inte zzz"

foo_bar = ["foo", "bar"]       #definerar lista med "foo" och "bar"
pro_bar = 3*foo_bar            #definerar lista med foo,bar tre gånger, samma som foo,bar,foo,bar,foo,bar
print(list + foo_bar)          #skriver ut lista 1 och lista 2 kombinerat
print(pro_bar)                 #skriver ut foo,bar,foo,bar,foo,bar

empty = []                     #definerar tom list  

if (len(empty)) < 1:           #checkar om listan är tom
    print("man it empty")      #skriver om listan är tom