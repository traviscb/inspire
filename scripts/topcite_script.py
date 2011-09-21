list = intbitset(list)
list2 - list
list3 = _i
list3
list3 = list2 - list
len(list)
len(list2)
len(list3)
list[0]
list
list.tolist()[0]
list.tolist().pop
list.pop 
list.pop()
list.tolist().pop()
_ip.magic("run topcites.py")
_ip.magic("run topcites.py")
list = generate_topcite_list(d,"year:'2005->2009' -year:'0->2004'",50,"980:CORE year:2009",num=100)
_ip.magic("run topcites.py")
list = generate_topcite_list(d,"year:'2005->2009' -year:'0->2004'",50,"980:CORE year:2009",num=100)
_ip.magic("run topcites.py")
list = generate_topcite_list(d,"year:'2005->2009' -year:'0->2004'",50,"980:CORE year:2009",num=100)
list
[(BibFormatObject(a).fields("773__y")) for a in list]
[(BibFormatObject(a[0]).fields("245__a"),a[1]) for a in list]

generate_topcite_list(d,"year:2005->2009 -year:0->2004",100,"980:CORE",of='hb',num=100,outfile='lastfive.html')
generate_topcite_list(d,"cited:100->9999999",100,"980:CORE",of='hb',num=100,outfile='alltime.html')
generate_topcite_list(d,"cited:50->999999",50,"980:CORE year:'2009'",of='hb',num=100,outfile='core09.html')
generate_topcite_list(d,"cited:50->999999 year'2005->2009' -year:'0->2004'",50,"980:CORE year:'2009'",of='hb',num=100,outfile='last5_core09.html')
generate_topcite_list(d,"cited:50->999999 year'2005->2009' -year:'0->2004'",50,"980:CORE year:'2009'",num=100)
generate_topcite_list(d,'cited:50->999999 year:"2005->2009" -year:"0->2004"',50,"980:CORE year:'2009'",num=100)
generate_topcite_list(d,'cited:50->999999 year:"2005->2009" -year:"0->2004"',50,"980:CORE year:'2009'",num=100,of='hb',outfile='last5_core09.html')
_ip.magic("save topcite_script 200-233")
