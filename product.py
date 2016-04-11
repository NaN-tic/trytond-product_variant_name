# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['Product']


class Product:
    __metaclass__ = PoolMeta
    __name__ = 'product.product'
    variant_name = fields.Char("Variant Name", select=True, translate=True)

    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        for d in domain:
            if d and d[0] == 'name':
                if d[1] == 'in':
                    domain = ['OR', domain[:], ('template.name', 'in', d[2])]
                    break
                else:
                    domain = ['OR', domain[:], ('template.name', 'ilike', d[2])]
                    break
        return super(Product, cls).search(domain, offset=offset, limit=limit,
            order=order, count=count, query=query)

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super(Product, cls).search_rec_name(name, clause)
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
            domain,
            ('variant_name', ) + tuple(clause[1:])
            ]
