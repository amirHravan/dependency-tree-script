CLASS_NAME_REGEX = '((\\w+)\\s+)?class\\s*((\\w+)(<[\\w\\s]*>)?)\\s*'
INTERFACE_NAME_REGEX = 'interface\\s*([\\w<>]+)\\s*[^(]'
INJECT_VIEWMODEL_REGEX = '(\\w+)\\s*:\\s*(\\w+)\\s+by\\s+((viewModel)|(inject)|(sharedViewModel))'