
from constants import html_entities
from pijnu.library.node import Nil, Nodes, Node
from mediawiki_parser import wikitextParser
import apostrophes

try: 
    import pygments
except ImportError:
    pygments = None

def toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes, interwiki, namespaces, use_pygments=False):
    tags_stack = []

    external_autonumber = []
    """ This is for the autonumbering of external links.
    e.g.: "[http://www.mozilla.org] [http://fr.wikipedia.org]"
    is rendered as: "<a href="...">[1]</a> <a href="...">[2]</a>
    """

    category_links = []
    """ This will contain the links to the categories of the article. """
    interwiki_links = []
    """ This will contain the links to the foreign versions of the article. """

    if use_pygments and not pygments:
        raise RuntimeError("use_pygment=True, but pygment could not be imported")

    pygment_options = {'lang': "text"}

    for namespace, value in namespaces.iteritems():
        assert value in range(16), "Incorrect value for namespaces"
    """
    Predefined namespaces; source: includes/Defines.php of MediaWiki-1.17.0
    'NS_MAIN', 0
    'NS_TALK', 1
    'NS_USER', 2
    'NS_USER_TALK', 3
    'NS_PROJECT', 4
    'NS_PROJECT_TALK', 5
    'NS_FILE', 6
    'NS_FILE_TALK', 7
    'NS_MEDIAWIKI', 8
    'NS_MEDIAWIKI_TALK', 9
    'NS_TEMPLATE', 10
    'NS_TEMPLATE_TALK', 11
    'NS_HELP', 12
    'NS_HELP_TALK', 13
    'NS_CATEGORY', 14
    'NS_CATEGORY_TALK', 15 
    """

    def balance_tags(tag=None):
        i = 0
        if tag is not None:
            try:
                i = tags_stack.index(tag, -1)
            except ValueError:
                return ''
        result = ''
        while len(tags_stack) > i:
            result += '</%s>' % tags_stack.pop()
        return result

    def content(node):
        return apostrophes.parse('%s' % node.leaf() + balance_tags())

    def render_title1(node):
        node.value = '<h1>' + content(node) +  '</h1>\n'

    def render_title2(node):
        node.value = '<h2>' + content(node) +  '</h2>\n'

    def render_title3(node):
        node.value = '<h3>' + content(node) +  '</h3>\n'

    def render_title4(node):
        node.value = '<h4>' + content(node) +  '</h4>\n'

    def render_title5(node):
        node.value = '<h5>' + content(node) +  '</h5>\n'

    def render_title6(node):
        node.value = '<h6>' + content(node) +  '</h6>\n'

    def render_raw_text(node):
        node.value = "%s" % node.leaf()

    def render_paragraph(node):
        value = content(node)
        if value != '':
            node.value = '<p>' + value +  '</p>\n'

    def render_wikitext(node):
        node.value = content(node)

    def render_body(node):
        metadata = ''
        if category_links != []:
            metadata += '<p>Categories: ' + ', '.join(category_links) + '</p>\n'
        if interwiki_links != []:
            metadata += '<p>Interwiki: ' + ', '.join(interwiki_links) + '</p>\n'
        node.value = '<body>\n' + content(node) + metadata + '</body>'

    def render_entity(node):
        value = '%s' % node.leaf()
        if value in html_entities:
            node.value = '%s' % unichr(html_entities[value])
        else:
            node.value = '&amp;%s;' % value

    def render_lt(node):
        node.value = '&lt;'

    def render_gt(node):
        node.value = '&gt;'

    def process_attribute(node, allowed_tag):
        assert len(node.value) in [1,2], "Bad AST shape!"
        if len(node.value) == 1:
            attribute_name = node.value[0].value
            if attribute_name in allowed_attributes or not allowed_tag:
                return '%s' % attribute_name
            return ''
        elif len(node.value) == 2:
            attribute_name = node.value[0].value
            attribute_value = node.value[1].value
            if attribute_name in allowed_attributes or not allowed_tag:
                return '%s="%s"' % (attribute_name, attribute_value)
            return ''

    def process_attributes(node, allowed_tag):
        result = ''
        if len(node.value) == 1:
            pass
        elif len(node.value) == 2:
            attributes = node.value[1].value
            for i in range(len(attributes)):
                attribute = process_attribute(attributes[i], allowed_tag)
                if attribute is not '':
                    result += ' ' + attribute 
        else:
            raise Exception("Bad AST shape!")
        return result

    def render_attribute(node):
        node.value = process_attribute(node, True)

    def render_tag_open(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tags_stack.append(tag_name)
            node.value = '<%s%s>' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s&gt;' % (tag_name, attributes)

    def render_tag_close(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            node.value = balance_tags(tag_name)
        else:
            node.value = "&lt;/%s&gt;" % tag_name

    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            attributes = process_attributes(node, True)
            node.value = '<%s%s />' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s /&gt;' % (tag_name, attributes)

    def render_table(node):
        table_parameters = ''
        table_content = ''
        if isinstance(node.value, Nodes) and node.value[0].tag == 'table_begin':
            attributes = node.value[0].value[0]
            for attribute in attributes:
                if attribute.tag == 'HTML_attribute' and attribute.value != '':
                    table_parameters += ' ' + attribute.value
            contents = node.value[1].value
            for item in contents:
                table_content += content(item)
        else:
            table_content = content(node)
        node.value = '<table%s>\n<tr>\n%s</tr>\n</table>\n' % (table_parameters, table_content)

    def render_cell_content(node):
        if isinstance(node.value, Nil):
            return None
        cell_parameters = ''
        cell_content = ''
        if len(node.value) > 1:
            values = node.value[0].value
            for value in values:
                if isinstance(value, Node):
                    if value.tag == 'HTML_attribute' and value.value != '':
                        cell_parameters += ' ' + value.value
                    else:
                        cell_content += value.leaf()
                else:
                    cell_content += value
            cell_content += content(node.value[1])
        else:
            cell_content = content(node)
        return (cell_parameters, cell_content)

    def render_table_header_cell(node):
        result = ''
        if isinstance(node.value, Nodes):
            for i in range(len(node.value)):
                content = render_cell_content(node.value[i])
                result += '\t<th%s>%s</th>\n' % content
        else:
            content = render_cell_content(node)
            result = '\t<th%s>%s</th>\n' % content            
        if result != '':
            node.value = result

    def render_table_normal_cell(node):
        result = ''
        if isinstance(node.value, Nodes):
            for i in range(len(node.value)):
                content = render_cell_content(node.value[i])
                result += '\t<td%s>%s</td>\n' % content
        else:
            content = render_cell_content(node)
            result = '\t<td%s>%s</td>\n' % content            
        if result != '':
            node.value = result

    def render_table_empty_cell(node):
        node.value = '\t<td></td>\n'

    def render_table_caption(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<caption%s>%s</caption>\n' % content

    def render_table_line_break(node):
        line_parameters = ''
        if node.value != '':
            assert len(node.value) == 1, "Bad AST shape!"
            parameters = node.value[0].value
            for value in parameters:
                if value.tag == 'HTML_attribute' and value.value != '':
                    line_parameters += ' ' + value.value
        node.value = '</tr>\n<tr%s>\n' % line_parameters

    def render_preformatted(node):
        node.value = u'<pre>' + content(node) +  u'</pre>\n'

    def render_source(node):
        if use_pygments:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter
            source = content(node)
            source_lang = pygment_options["lang"]
            linenos = pygment_options['linenos']
            rendered = highlight(source, get_lexer_by_name(source_lang, stripnl=False, stripall=False, tabsize=8), HtmlFormatter(linenos=linenos))
            node.value =rendered
            pygment_options['lang'] = "text"
            return
        else:
            node.value = content(node) + u'</code></pre>\n'

    def render_source_open(node):
        if use_pygments:
            if node.kind == node.BRANCH:
                source_lang = ([n.value for n in node[0] if getattr(n, 'tag', None) == "SOURCE_LANG_NAME"] or ["text"])[0]
                source_lang, source_linenos = (source_lang.split(" ") + [""])[0:2]
                source_linenos = source_linenos != "nonumber"
            else:
                source_lang = "text"
                source_linenos = True
            pygment_options['lang'] = source_lang
            pygment_options['linenos'] = source_linenos
            node.value = ""
        else:
            if node.value != node.NIL:
                attribs = " %s"%(node.leaves(),)
            else: 
                attribs = ""
            node.value = u"<pre><code%s>"%attribs

    def render_source_text(node):
        if not use_pygments:
            node.value = content(node).replace('<', '&lt;').replace('>', '&gt;') 
        else:
            node.value = content(node)

    def render_hr(node):
        node.value = '<hr />\n'

    def render_ul(list, level):
        indent = level * '\t'
        result = '<ul>\n'
        for i in range(len(list)):
            result += indent + '<li>' + content(list[i]) +  '</li>\n'
        result += '</ul>\n'
        return result

    def render_ol(list, level):
        indent = level * '\t'
        result = '<ol>\n'
        for i in range(len(list)):
            result += indent + '<li>' + content(list[i]) +  '</li>\n'
        result += '</ol>\n'
        return result

    def render_dd(list, level):
        indent = level * '\t'
        result = '<dl>\n'
        for i in range(len(list)):
            result += indent + '<dd>' + content(list[i]) +  '</dd>\n'
        result += '</dl>\n'
        return result

    def render_dt(list, level):
        indent = level * '\t'
        result = '<dl>\n'
        for i in range(len(list)):
            result += indent + '<dt>' + content(list[i]) +  '</dt>\n'
        result += '</dl>\n'
        return result

    def render_dl(list, level):
        indent = level * '\t'
        result = '<dl>\n'
        #import pdb; pdb.set_trace()
        def tagtype(value):
            if value.tag in ['semi_colon_list_leaf', '@semi_colon_sub_list@']: 
                return 'dt'
            else:
                return 'dd'
        for i in range(len(list)):
            tagname = tagtype(list[i])
            result += indent + '<%s>'%tagname + content(list[i]) +  '</%s>\n'%tagname
        result += '</dl>\n'
        return result

    def collapse_list(list):
        def _equiv( l1, l2 ):
            equivs = [ ('bullet_list_leaf', '@bullet_sub_list@')
                     , ('number_list_leaf', '@number_sub_list@')
                     , ('colon_list_leaf', '@colon_sub_list@')
                     , ('semi_colon_list_leaf', '@semi_colon_sub_list@')
                     ]
            for t1, t2 in equivs:
                if l1.tag == t1 and l2.tag == t2:
                    return True
            return False
        i = 0
        while i+1 < len(list):
            if _equiv(list[i], list[i+1]):
                list[i].value.append(list[i+1].value[0])
                list.pop(i+1)
            else:
                i += 1
        for i in range(len(list)):
            if isinstance(list[i].value, Nodes):
                collapse_list(list[i].value)

    def select_items(nodes, i, value, level):
        list_tags = ['bullet_list_leaf', 'number_list_leaf', 'colon_list_leaf', 'semi_colon_list_leaf']
        if isinstance(value, list):
            for v in value:
                list_tags.remove(v)
        else:
            list_tags.remove(value)
        if isinstance(nodes[i].value, Nodes):
            render_lists(nodes[i].value, level + 1)
        items = [nodes[i]]
        while i + 1 < len(nodes) and nodes[i+1].tag not in list_tags:
            if isinstance(nodes[i+1].value, Nodes):
                render_lists(nodes[i+1].value, level + 1)
            items.append(nodes.pop(i+1))
        return items

    def render_lists(list, level):
        i = 0
        while i < len(list):
            if list[i].tag == 'bullet_list_leaf' or list[i].tag == '@bullet_sub_list@':
                list[i].value = render_ul(select_items(list, i, 'bullet_list_leaf', level), level)
            elif list[i].tag == 'number_list_leaf' or list[i].tag == '@number_sub_list@':
                list[i].value = render_ol(select_items(list, i, 'number_list_leaf', level), level)
            elif list[i].tag == 'colon_list_leaf' or list[i].tag == '@colon_sub_list@' \
                 or list[i].tag == 'semi_colon_list_leaf' or list[i].tag == '@semi_colon_sub_list@':
                list[i].value = render_dl(select_items(list, i, ['semi_colon_list_leaf', 'colon_list_leaf'], level), level)
            i += 1

    def render_list(node):
        assert isinstance(node.value, Nodes), "Bad AST shape!"
        collapse_list(node.value)
        render_lists(node.value, 1)

    def render_url(node):
        node.value = '<a href="%s">%s</a>' % (node.leaf(), node.leaf())

    def render_external_link(node):
        if len(node.value) == 1:
            external_autonumber.append(node.leaf())
            node.value = '<a href="%s">[%s]</a>' % (node.leaf(), len(external_autonumber))
        else:
            text = node.value[1].leaf()
            node.value = '<a href="%s">%s</a>' % (node.value[0].leaf(), text)

    def render_interwiki(prefix, page):
        link = '<a href="%s">%s</a>' % (interwiki[prefix] + page, page)
        if link not in interwiki_links:
            interwiki_links.append(link)

    def render_category(category_name):
        link = '<a href="%s">%s</a>' % (category_name, category_name)
        if link not in category_links:
            category_links.append(link)

    def render_file(file_name, arguments):
        """ This implements a basic handling of images.
        MediaWiki supports much more parameters (see includes/Parser.php).
        """
        style = ''
        thumbnail = False
        legend = ''
        if arguments != []:
            parameters = arguments[0].value
            for parameter in parameters:
                parameter = '%s' % parameter.leaf()
                if parameter[-2:] == 'px':
                    size = parameter[0:-2]
                    if 'x' in size:
                        size_x, size_y = size.split('x', 1)
                        try:
                            size_x = int(size_x)
                            size_y = int(size_y)
                            style += 'width:%spx;height:%spx' % (size_x, size_y)
                        except:
                            legend = parameter
                    else:
                        try:
                            size_x = int(size)
                            style += 'width:%spx;' % size_x
                        except:
                            legend = parameter
                elif parameter in ['left', 'right', 'center']:
                    style += 'float:%s;' % parameter
                elif parameter in ['thumb', 'thumbnail']:
                    thumbnail = True
                elif parameter == 'border':
                    style += 'border:1px solid grey'
                else:
                    legend = parameter
        result = '<img src="%s" style="%s" alt="" />' % (file_name, style)
        if thumbnail:
            result = '<div class="thumbnail">%s<p>%s</p></div>\n' % (result, legend)
        return result

    def render_internal_link(node):
        force_link = False
        url = ''
        page_name = node.value.pop(0).value
        if page_name[0] == ':':
            force_link = True
            page_name = page_name[1:]
        if ':' in page_name:
            namespace, page_name = page_name.split(':', 1)
            if namespace in interwiki.keys() and not force_link:
                render_interwiki(namespace, page_name)
                node.value = ''
                return
            elif namespace in interwiki.keys():
                url = interwiki[namespace]
                namespace = ''
            if namespace in namespaces.keys():
                if namespaces[namespace] == 6 and not force_link:  # File
                    node.value = render_file(page_name, node.value)
                    return
                elif namespaces[namespace] == 14 and not force_link:  # Category
                    render_category(page_name)
                    node.value = ''
                    return
            if namespace:
                page_name = namespace + ':' + page_name
        if len(node.value) == 0:
            text = page_name
        else:
            text = '|'.join('%s' % item.leaf() for item in node.value[0])
        node.value = '<a href="%s%s">%s</a>' % (url, page_name, text)

    def render_invalid(node):
        node.value = '<span style="color:red">Invalid line: %s</span>' % node.leaf()

    return locals()

def make_parser(allowed_tags=[], allowed_autoclose_tags=[], allowed_attributes=[], interwiki={}, namespaces={}, use_pygments=False):
    """Constructs the parser for the HTML backend.
    
    :arg allowed_tags: List of the HTML tags that should be allowed in the parsed wikitext.
            Opening tags will be closed. Closing tags with no opening tag will be removed.
            All the tags that are not in the list will be output as &lt;tag&gt;.
    :arg allowed_autoclose_tags: List of the self-closing tags that should be allowed in the
            parsed wikitext. All the other self-closing tags will be output as &lt;tag /&gt;
    :arg allowed_attributes: List of the HTML attributes that should be allowed in the parsed
            tags (e.g.: class="", style=""). All the other attributes (e.g.: onclick="") will
            be removed.
    :arg interwiki: Dict of the allowed interwiki prefixes (en, fr, es, commons, etc.)
    :arg namespaces: Dict of the namespaces of the wiki (File, Category, Template, etc.),
            including the localized version of those strings (Modele, Categorie, etc.),
            associated to the corresponding namespace code.
    """
    tools = toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes, interwiki, namespaces, use_pygments)
    return wikitextParser.make_parser(tools)
