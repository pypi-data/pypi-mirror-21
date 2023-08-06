Swiss bank electronic payment (DTA) - Transaction ID Compatibility
==================================================================

Link module between the Swiss Payment File (DTA) module
(l10n_ch_dta) and the module adding a transaction ID
field (base_transaction_id).

When an invoice has a transaction ID, the DTA is exported with this ID
as reference. This is used by the bank-statement-reconcile project
in the banking addons (https://launchpad.net/banking-addons).



