CustomLogin
===========

A way to customise the login behaviour by using content rules. Content rules
can now be triggered by a Unauhtorised trigger and new Redirect action allows
adminstrators to send users to a custom form or another site. Rules can be
created to redirect unauthorised users based on the content location, current
groups or permissions or any other content rule criteria. Because the redirect action uses 
a tal expression you can include any additional information you need for you 
custom login process.

Examples
--------
Filling out a form to download a pdf. This can be achieved via creating a rule 
that redirects to a PloneFormGen form and then applying the content rule to the 
private content objects you want to protect. Using a PFT script adapter you
can use something like tokenrole to give permission to original object once
the user has filled out the form correctly. 

Technical
---------

A PAS challenge that raises an event so that a custom event handler can 
issue a redirect, allowing for custom login pages.

Provides a ContentRule and a ContentAction so that redirects can be managed via
content rules.
