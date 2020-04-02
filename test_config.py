options = {'test': False,
           'apiKey': '*** confidential ***',
           'secret': '*** confidential ***'}

if options['test']:
    endpoint = "*** confidential ***"  # test
else:
    endpoint = "https://api-adapter.backend.currency.com/api/v1"  # prod
