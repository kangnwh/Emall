from webapp.Models.db_basic import Session
from webapp.Models.user import User
from webapp.Models.user_feedback import User_feedback
from webapp.Models.prod_profit_rate import Prod_profit_rate
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.prod_info import Prod_info
from webapp.Models.advertise_info import Advertise_info
from webapp.Models.prod_price_range import Prod_price_range
from webapp.common import generate_md5

from webapp.Models.db_init import recreate_all

# recreate all tables accroding to py classes
# recreate_all()

# unit testing for individual tables
# below is an example for table User
u = User()
u.user_name = 'abcd'
u.email = 'mail@126.com'
u.password = generate_md5('passw0rd')


uf=User_feedback()
uf.user_id=1
uf.user_name='abcd'
uf.user_comment='fsfdsfdsfdsfdsfd'


prr=Prod_profit_rate()
prr.profit_rate=2.50

pcat=Prod_cat()
pcat.prod_cat_name='Rush item'
pcat.prod_cat_desc='used for Rush items'


psubcat=Prod_sub_cat()
psubcat.prod_cat_sub_name='paper'
psubcat.prod_cat_sub_desc='homeuse paper'
psubcat.prod_cat_id=1

prodinfo=Prod_info()
prodinfo.prod_name='prod1'
prodinfo.prod_desc='this is prod1'
prodinfo.prod_cat_sub_id=1

adv=Advertise_info()
adv.prod_id=1

pprange=Prod_price_range()
pprange.prod_id=1
pprange.quantity_from1=1
pprange.quantity_to1=1000
pprange.unit_price1=12

pprange.quantity_from2=1001
pprange.quantity_to2=10000
pprange.unit_price2=10


s = Session()
s.add(u)
s.add(uf)
s.add(pcat)
s.add(psubcat)
s.add(prr)
s.add(prodinfo)
s.add(adv)
s.add(pprange)

s.commit()

