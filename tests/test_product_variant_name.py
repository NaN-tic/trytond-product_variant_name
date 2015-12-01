# This file is part of the product_variant_name module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductVariantNameTestCase(ModuleTestCase):
    'Test Product Variant Name module'
    module = 'product_variant_name'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductVariantNameTestCase))
    return suite