Check that the Customer has a VAT number on invoice validation
==============================================================

This module adds an option **Customer must have VAT** on fiscal positions.
When a user tries to validate a customer invoice or refund
with a fiscal position that have this option, OpenERP will check that
the customer has a VAT number.

If it doesn't, OpenERP will block the validation of the invoice
and display an error message.

In the European Union (EU), when an EU company sends an invoice to
another EU company in another country, it can invoice without VAT
(most of the time) but the VAT number of the customer must be displayed
on the invoice.

This module also displays a warning when a user sets
a fiscal position with the option **Customer must have VAT** on a customer
and this customer doesn't have a VAT number in OpenERP yet.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com>
for any help or question about this module.


