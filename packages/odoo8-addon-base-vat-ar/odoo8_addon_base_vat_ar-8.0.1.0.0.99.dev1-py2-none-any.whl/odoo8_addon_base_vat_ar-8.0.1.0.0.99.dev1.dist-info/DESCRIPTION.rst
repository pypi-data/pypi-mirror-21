This module provide :
* VAT Check for Argentina.
* Modification of check_vat_routine:
    The original routine, got the VAT Number an extract the first two letters
    and used them to as Country ISO Code to know the country of the partner and to call
    the routine related to this country.
    This module modify this, getting the country from the partner itself (the ISO Code has
    to be well defined) and if this is not defined, the original routine is executed.


