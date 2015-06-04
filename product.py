# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


__all__ = ['Product']
__metaclass__ = PoolMeta
STATES = {
    'readonly': ~Eval('active', True),
    'invisible': Eval('_parent_template', {}).get('unique_variant', False),
    'required': ~(Eval('_parent_template', {}).get('unique_variant', False)),
    }


class Product:
    __name__ = 'product.product'
    name = fields.Function(
            fields.Char('Name', states=STATES, depends=['active']),
        'get_name', setter='set_name', searcher='search_name', )
    variant_name = fields.Char("Variant Name", select=True)

    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        for d in domain:
            if d and d[0] == 'name':
                domain = ['OR', domain[:], ('template.name', 'ilike', d[2])]
                break
        return super(Product, cls).search(domain, offset=offset, limit=limit,
            order=order, count=count, query=query)

    @classmethod
    def search_rec_name(cls, name, clause):
        res = super(Product, cls).search_rec_name(name, clause)
        return ['OR',
            res,
            [('variant_name', ) + tuple(clause[1:])]
            ]

    def get_name(self, name):
        if self.variant_name:
            return self.variant_name
        return self.template.name

    @classmethod
    def set_name(cls, products, name, value):
        cls.write(products, {'variant_name': value})

    @classmethod
    def search_name(cls, name, clause):
        return [('variant_name',) + tuple(clause[1:])]
