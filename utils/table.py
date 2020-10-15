from django.db.models import Q

def _build_path(queries):
    string = '?'
    for q in queries:
        string += q + '=' + queries[q] + '&'
    return string[:-1]

'''
modifies the past queryset object, with the given columns (properties and annotations)
with the desired order and search parameters. 
'''
def get_queryset_table(queryset, columns, queries, default_order=None, search_columns=None, search_type='__icontains'):
    if default_order is None:
        default_order = columns[0]

    if 'order' in queries and queries['order'] in columns:
        if 'dir' in queries and queries['dir'] == 'asc':
            table = queryset.order_by(queries['order'])
        else:
            table = queryset.order_by('-' + queries['order'])
    else:
        table = queryset.order_by(default_order)

    if 'search' in queries and queries['search'] and search_columns is not None:
        query = Q()
        for col in search_columns:
            col += search_type
            query = query | Q(**{col: queries['search']})
        table = table.filter(query)

    return table

'''
returns an iterable of strings that represent query parameters
for adding to the heads of columns in a searchable table
so that they can easily be sorted in asc and desc order
'''
def get_col_urls(queries, columns):

    col_urls = []

    for col in columns:
        q = queries.copy()
        q['order'] = col
        if 'order' in queries and queries['order'] == col:
            if 'dir' in q and q['dir'] == 'desc':
                q['dir'] = 'asc'
            else:
                q['dir'] = 'desc'
        else:
            q['dir'] = 'desc'
        col_urls.append(_build_path(q))

    return col_urls
