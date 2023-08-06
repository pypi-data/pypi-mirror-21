Implements server environment behavior
for connector Salesforce authentication.

 To use it you have to add a section named as:

    salesforce_auth_ + Name of the backend

 Default available section options are:

 - authentication_method
 - callback_url
 - sandbox
 - url

Module can easily be extended to add any other field.
By default they are not provided in order not have security issues.


