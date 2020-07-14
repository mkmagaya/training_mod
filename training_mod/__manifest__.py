# -*- coding: utf-8 -*-

# Telecontract Pvt Ltd (c) 2017. See LICENSE file for full copyright and licensing details.

{
    'name': 'Telco Training (Human Resources)',
    'version': '1.3',
    'category': 'Human Resources',
    'summary': 'Employee Training Module - Human Resource',
    'description': """
        Employee Training Module:

Employee training is part of a long-term investment in our employees. It is an initial process that provides easy access to basic information, programs and services, gives clarification and allows new and existing employees to take an active role in their organization.

            """,
    'author': 'Telecontract Pvt Ltd',
    'website': 'www.telco.co.zw',
    'depends': ['base','hr','mail','survey'],
    'data': [
             'security/employee_orientation_security.xml',
             'security/ir.model.access.csv',
             'data/employee_orientation_data.xml',
             'data/employee_orientation_sequence.xml',
             'views/employee_orientation.xml',
             ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
