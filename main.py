import getcalories
import getname
import getcode

#codes = ["0085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142", "0080244009236"]
codes = getcode.getcode('links.txt')

for code in codes:
    name = getname.getProductName(code)
    cal = getcalories.get_calorie(name)
    print()
    print(name, cal)
    print()