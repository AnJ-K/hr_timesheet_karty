# -*- coding: utf-8 -*-
{
    "name": "Time sheet report",
    "version": "0.1",
    "author": "author",
    "description": "Time sheet report",
    "website": "website",
    "category": "Test",
    "depends": ["base", "web", "hr", "hr_timesheet"],
    "data": [
        'security/ir.model.access.csv',
        'reports/report_karty.xml',
        'wizard/wizard_karty.xml',
    ],
    "installable": True
}
