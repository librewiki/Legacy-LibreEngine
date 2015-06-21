from constants import html_entities
from pijnu.library.node import Nil, Nodes, Node
from mediawiki_parser import wikitextParser
import apostrophes

def toolset(interwiki, namespaces):
    tags_stack = []

    external_autonumber = []
    """ This is for the autonumbering of external links.
    e.g.: "[http://www.mozilla.org] [http://fr.wikipedia.org] text"
    is rendered as: "[1] [2] text
    Links:
    [1] http://www.mozilla.org
    [2] http://fr.wikipedia.org
    """

    external_links = []
    """ This will contain the external links of the article. """
    category_links = []
    """ This will contain the links to the categories of the article. """
    interwiki_links = []
    """ This will contain the links to the foreign versions of the article. """

    style_tags = {'bold': '*', 'bold_close': '*', 'italic': '_', 'italic_close': '_'}

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

    def render_tag_p(attributes):
        return '\n'

    def render_tag_br(attributes):
        return '\n'

    allowed_tags = {'p': render_tag_p,
                    'br': render_tag_br}

    def content(node):
        return apostrophes.parse('%s' % node.leaf(), style_tags)

    def render_title1(node):
        node.value = '%s\n' % node.leaf()

    def render_title2(node):
        node.value = '%s\n' % node.leaf()

    def render_title3(node):
        node.value = '%s\n' % node.leaf()

    def render_title4(node):
        node.value = '%s\n' % node.leaf()

    def render_title5(node):
        node.value = '%s\n' % node.leaf()

    def render_title6(node):
        node.value = '%s\n' % node.leaf()

    def render_raw_text(node):
        pass

    def render_paragraph(node):
        node.value = '%s\n' % node.leaf()

    def render_wikitext(node):
        pass

    def render_body(node):
        metadata = ''
        if external_links != []:
            metadata += '\nLinks:\n' + '\n'.join(external_links) + '\n'
        if category_links != []:
            metadata += '\nCategories:\n' + '\n'.join(category_links) + '\n'
        if interwiki_links != []:
            metadata += '\nInterwiki:\n' + '\n'.join(interwiki_links) + '\n'
        node.value = apostrophes.parse('%s' % node.leaves(), style_tags) + metadata

    def render_entity(node):
        value = '%s' % node.leaf()
        if value in html_entities:
            node.value = '%s' % unichr(html_entities[value])
        else:
            node.value = '&amp;%s;' % value

    def render_lt(node):
        node.value = '<'

    def render_gt(node):
        node.value = '>'

    def process_attribute(node, allowed_tag):
        assert len(node.value) in [1,2], "Bad AST shape!"
        if len(node.value) == 1:
            attribute_name = node.value[0].value
            return '%s' % attribute_name
        elif len(node.value) == 2:
            attribute_name = node.value[0].value
            attribute_value = node.value[1].value
            return '%s="%s"' % (attribute_name, attribute_value)

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
        if tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tag_processor = allowed_tags[tag_name]
            node.value = tag_processor(attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '<%s%s>' % (tag_name, attributes)

    def render_tag_close(node):
        node.value = ''

    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tag_processor = allowed_tags[tag_name]
            node.value = tag_processor(attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '<%s%s />' % (tag_name, attributes)

    def render_table(node):
        table_content = ''
        if isinstance(node.value, Nodes) and node.value[0].tag == 'table_begin':
            contents = node.value[1].value
            for item in contents:
                table_content += content(item)
        else:
            table_content = content(node)
        node.value = '----------\n%s\n----------\n' % table_content

    def render_cell_content(node):
        if isinstance(node.value, Nil):
            return None
        cell_content = ''
        if len(node.value) > 1:
            values = node.value[0].value
            for value in values:
                if isinstance(value, Node):
                    if not (value.tag == 'HTML_attribute' and value.value != ''):
                        cell_content += value.leaf()
                else:
                    cell_content += value
            cell_content += content(node.value[1])
        else:
            cell_content = content(node)
        return cell_content

    def render_table_header_cell(node):
        result = ''
        if isinstance(node.value, Nodes):
            for i in range(len(node.value)):
                content = render_cell_content(node.value[i])
                result += '%s\t' % content
        else:
            content = render_cell_content(node)
            result = '%s\t' % content            
        if result != '':
            node.value = result

    def render_table_normal_cell(node):
        result = ''
        if isinstance(node.value, Nodes):
            for i in range(len(node.value)):
                content = render_cell_content(node.value[i])
                result += '%s\t' % content
        else:
            content = render_cell_content(node)
            result = '%s\t' % content            
        if result != '':
            node.value = result

    def render_table_empty_cell(node):
        node.value = '\t'

    def render_table_caption(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t%s\n' % content

    def render_table_line_break(node):
        node.value = '\n'

    def render_preformatted(node):
        node.value = content(node) + '\n'

    def render_source(node):
        node.value = content(node)

    def render_source_open(node):
        node.value = ''

    def render_source_text(node):
        node.value = content(node)

    def render_hr(node):
        node.value = '------'

    def render_ul(list, level):
        indent = level * '\t'
        result = '\n'
        for i in range(len(list)):
            result += indent + '* ' + content(list[i]) + '\n'
        return result

    def render_ol(list, level):
        indent = level * '\t'
        result = '\n'
        for i in range(len(list)):
            result += indent + '%i. %s\n' % (i + 1, content(list[i]))
        return result

    def render_dd(list, level):
        indent = level * '\t'
        result = '\n'
        for i in range(len(list)):
            result += indent + '* ' + content(list[i]) + '\n'
        return result

    def render_dt(list, level):
        indent = level * '\t'
        result = '\n'
        for i in range(len(list)):
            result += indent + '* ' + content(list[i]) + '\n'
        return result

    def collapse_list(list):
        i = 0
        while i+1 < len(list):
            if list[i].tag == 'bullet_list_leaf' and list[i+1].tag == '@bullet_sub_list@' or \
               list[i].tag == 'number_list_leaf' and list[i+1].tag == '@number_sub_list@' or \
               list[i].tag == 'colon_list_leaf' and list[i+1].tag == '@colon_sub_list@' or \
               list[i].tag == 'semi_colon_list_leaf' and list[i+1].tag == '@semi_colon_sub_list@':
                list[i].value.append(list[i+1].value[0])
                list.pop(i+1)
            else:
                i += 1
        for i in range(len(list)):
            if isinstance(list[i].value, Nodes):
                collapse_list(list[i].value)

    def select_items(nodes, i, value, level):
        list_tags = ['bullet_list_leaf', 'number_list_leaf', 'colon_list_leaf', 'semi_colon_list_leaf']
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
            elif list[i].tag == 'colon_list_leaf' or list[i].tag == '@colon_sub_list@':
                list[i].value = render_dd(select_items(list, i, 'colon_list_leaf', level), level)
            elif list[i].tag == 'semi_colon_list_leaf' or list[i].tag == '@semi_colon_sub_list@':
                list[i].value = render_dt(select_items(list, i, 'semi_colon_list_leaf', level), level)
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
            url = node.leaf()
            text = len(external_autonumber)
        else:
            url = node.value[0].leaf()
            text = node.value[1].leaf()
        node.value = '[%s]' % (text)
        external_links.append('[%s] %s' % (text, url))

    def render_interwiki(prefix, page):
        link = '* %s' % (interwiki[prefix] + page)
        if link not in interwiki_links:
            interwiki_links.append(link)

    def render_category(category_name):
        link = '* %s' % (category_name)
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
        result = 'Image: %s, style: %s' % (file_name, style)
        if thumbnail:
            result = '%s, legend:%s\n' % (result, legend)
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
        node.value = '%s (link: %s%s)' % (text, url, page_name)

    def render_invalid(node):
        pass

    return locals()

def make_parser(interwiki={}, namespaces={}):
    """Constructs the parser for the text backend.

    :arg interwiki: Dict of the allowed interwiki prefixes (en, fr, es, commons, etc.)
    :arg namespaces: Dict of the namespaces of the wiki (File, Category, Template, etc.),
            including the localized version of those strings (Modele, Categorie, etc.),
            associated to the corresponding namespace code.
    """
    tools = toolset(interwiki, namespaces)
    return wikitextParser.make_parser(tools)
