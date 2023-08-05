# geoql

Library for performing queries and transformations on GeoJSON data (with emphasis on support for abstract graph representations).

Package Installation and Usage
------------------------------

The package is available on PyPI:

    python -m pip install geoql

The library can be imported in the usual way:

    import geoql

An example of usage is provided  below:

    import geojson
    import geoql
    import geoleaflet
    import requests

    url = 'https://raw.githubusercontent.com/Data-Mechanics/geoql/master/examples/'
    
    # Boston ZIP Codes regions.
    z = geojson.loads(requests.get(url + 'example_zips.geojson').text, encoding="latin-1")
    
    # Extract of street data.
    g = geojson.loads(requests.get(url + 'example_extract.geojson').text, encoding="latin-1")
    
    g = geoql.features_properties_null_remove(g)
    g = geoql.features_tags_parse_str_to_dict(g)
    g = geoql.features_keep_by_property(g, {"highway": {"$in": ["residential", "secondary", "tertiary"]}})
    g = geoql.features_keep_within_radius(g, (42.3551, -71.0656), 0.75, 'miles') # Within 0.75 of Boston Common.
    g = geoql.features_keep_intersecting_features(g, z) # Only those entries found in a Boston ZIP Code regions.
    g = geoql.features_node_edge_graph(g) # Converted into a graph with nodes and edges.
    open('example_extract.geojson', 'w').write(geojson.dumps(g))
    open('leaflet.html', 'w').write(geoleaflet.html(g)) # Create visualization.
