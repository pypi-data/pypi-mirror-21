

apis = {
    #'auth': {
    #    'base-path': '/alfresco/api/-default-/public/authentication/versions/1',
    #    'operations': {
    #        'create-ticket': {
    #            'path': '/tickets',
    #            #'post-params': {'userId', 'password'}
    #        }
    #    }
    #},
    'nodes': {
        'base-path': '/alfresco/api/-default-/public/alfresco/versions/1',
        'operations': {
            'get-node': {
                'path': '/nodes/{nodeId}'
            },
            'delete-node': {
                'path': '/nodes/{nodeId}'
            },
            'create-node': {
                'path': '/nodes/{nodeId}/children',
                'properties': ['name', 'nodeType'],
                'optional-properties': ['relativePath']
            },
            'update-node': {
                'path': '/nodes/{nodeId}',
                'properties': [],
                'optional-properties': ['name', 'nodeType'],
            },
            'list-node-children': {
                'path': '/nodes/{nodeId}/children'
            },
        }
    },
    'people': {
        'base-path': '/alfresco/api/-default-/public/alfresco/versions/1',
        'operations': {
            'get-person': {
                'path': '/people/{personId}'
            },
            'create-person': {
                'path': '/people',
                'properties': ['id', 'password', 'email', 'firstName']
            },
            'list-people': {
                'path': '/people'
            },
        }
    },
    'sites': {
        'base-path': '/alfresco/api/-default-/public/alfresco/versions/1',
        'operations': {
            'create-site': {
                'path': '/sites',
                'properties': ['id', 'title', 'description', 'visibility']
            },
            'update-site': {
                'path': '/sites/{siteId}',
                'properties': [],
                'optional-properties': ['title', 'description', 'visibility']
            },
            'delete-site': {
                'path': '/sites/{siteId}'
            },
            'get-site': {
                'path': '/sites/{siteId}'
            },
            'get-site-membership': {
                'path': '/people/{personId}/sites/{siteId}'
            },
            'list-sites': {
                'path': '/sites'
            },
            'list-site-memberships': {
                'path': '/people/{personId}/sites'
            }
        }
    }
}