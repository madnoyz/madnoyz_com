from flask_table import Table, Col

class results(table):
    id = Col('id')
    item = Col('itemName')
    desc = Col('itemDescription')
    qty = Col('qty')