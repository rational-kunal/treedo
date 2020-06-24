class UIKit(object):
    ADD_ICON = '<span uk-icon="icon: plus"></span>'
    CHECK_ICON = '<span uk-icon="icon: check"></span>'
    UNCHECK_ICON = '<span uk-icon="icon: close"></span>'
    TRASH_ICON = '<span uk-icon="icon: trash"></span>'
    STAR_ICON = '<span uk-icon="icon: star"></span>'
    BRANCH_ICON = '<span uk-icon="icon: git-branch"></span>'
    MORE_ICON = '<span uk-icon="icon: more"></span>'

    @staticmethod
    def button_group(btn_list):
        return '<div class="uk-button-group"> {} </div>'.format(
            ' '.join(btn_list)
        )

    @staticmethod
    def link_black_hover(href, text, css_class_list):
        return '<a href="{}" class="uk-button uk-button-secondary uk-button-small {}"> {} </a>'.format(
            href, ' '.join(css_class_list), text
        )

    @staticmethod
    def drop_down(parent_text, drop_down_links):
        return '''
                    <a href="#" class="uk-button uk-button-secondary uk-button-small"> {} </a>
                    <div uk-dropdown="mode: click">
                    <div>
                        <ul class="uk-nav uk-dropdown-nav">
                            {}
                        </ul>
                    </div>
                '''.format(parent_text,
                           ' '.join(map(lambda x: '<li><a href="{}">{}</a></li>'.format(x['link'], x['text']),
                                        drop_down_links)))