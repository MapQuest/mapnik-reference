#!/usr/bin/env python

try:
    # <= python 2.5
    import simplejson as json
except ImportError:
    # >= python 2.6
    import json

def testAttribute(parent, attr):
    assert 'type' in attr[1].keys(), '%s: type not in %s' % (parent[0], attr[0])
    #assert 'doc' in attr[1].keys(), '%s: doc string not in %s' % (parent[0], attr[0])
    assert 'css' in attr[1].keys(), '%s: css not in %s' % (parent[0], attr[0])

def testPsuedo(parent, attr):
    for i in attr[1].items():
        assert 'behavior' in i[1].keys(), '%s: behavior not in %s' % (parent[0], i[0])
        assert 'indexed' in i[1].keys(), '%s: indexed not in %s' % (parent[0], i[0])

def testChildElements(parent, attr, reference):
    for child in attr[1]:
        assert child in reference['elements'].keys(), '%s: %s is not a valid element' % (parent[0], child)

versions = ['2.0.0','2.0.1', '2.0.2', '2.1.0', '2.1.1', '2.3.0', 'latest']

for v in versions:
    print '-- testing %s/reference.json' % v
    reference = json.load(open('%s/reference.json' % v, 'r'))
    assert reference
    assert reference['version'] == v,"%s not eq to %s" % (reference['version'],v)
    for sym in reference['symbolizers'].items():
        assert sym[1]
        for i in sym[1].items():
            if i[0] == 'child-elements':
                testChildElements(sym, i, reference)
            else:
                testAttribute(sym, i)
                if sym[0] not in ['map','*']:
                    group_name = sym[0]
                    if group_name == 'markers':
                        group_name = 'marker'
                    css_name = i[1]['css']
                    assert group_name in css_name, "'%s' not properly prefixed by '%s'" % (css_name,group_name)
    if 'elements' in reference.keys():
        for elem in reference['elements'].items():
            assert elem[1]
            for i in elem[1].items():
                if i[0] == 'child-elements':
                    testChildElements(elem, i, reference)
                elif i[0] == 'pseudo':
                    testPsuedo(elem, i)
                else:
                    testAttribute(elem, i)
