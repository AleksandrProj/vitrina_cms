from django.utils.html import format_html, escape

from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtail.images.formats import (
    Format, 
    register_image_format, 
    unregister_image_format, 
    get_image_formats)


class UserImageFormat(Format):
    def __init__(self, name, label, classnames, filter_spec):
        self.name = name
        self.label = label
        self.classname = classnames
        self.filter_spec = filter_spec

    def image_to_html(self, image, alt_text, extra_attributes=None):

        self.filter_spec_desktop = "original"
        self.filter_spec_tablet = "height-680"
        self.filter_spec_mobile = "height-280"

        if extra_attributes is None:
            extra_attributes = {}

        rendition_desktop = get_rendition_or_not_found(image, self.filter_spec_desktop)
        rendition_mobile = get_rendition_or_not_found(image, self.filter_spec_mobile)
        rendition_tablet = get_rendition_or_not_found(image, self.filter_spec_tablet)

        extra_attributes["alt"] = escape(alt_text)
        if self.classname:
            extra_attributes["class"] = "%s" % escape(self.classname)

        original_html = rendition_desktop.img_tag(extra_attributes)
        original_html_retina = rendition_desktop.full_url
        mobile_html = rendition_mobile.full_url
        tablet_html = rendition_tablet.full_url

        return format_html("<picture>\
                                <source srcset='{1} 2x' media='(max-width: 767px) and (-webkit-min-device-pixel-ratio: 1.5), \
                                                               (max-width: 767px) and (min-resolution: 1.5dppx), \
                                                               (max-width: 767px) and (min--moz-device-pixel-ratio: 1.5), \
                                                               (max-width: 767px) and (-o-min-device-pixel-ratio: 3/2), \
                                                               (max-width: 767px) and (min-resolution: 120dpi)'>\
                                <source srcset='{0}' media='(max-width: 767px)'>\
                                <source srcset='{1}' media='(max-width: 1023px)'>\
                                <source srcset='{3} 2x' media='(min-width: 1024px) and (-webkit-min-device-pixel-ratio: 1.5), \
                                                               (min-width: 1024px) and (min-resolution: 1.5dppx), \
                                                               (min-width: 1024px) and (min--moz-device-pixel-ratio: 1.5), \
                                                               (min-width: 1024px) and (-o-min-device-pixel-ratio: 3/2), \
                                                               (min-width: 1024px) and (min-resolution: 120dpi)'>{2}\
                           </picture>", mobile_html, tablet_html, original_html, original_html_retina)


for format in get_image_formats():
    unregister_image_format(format.name)

register_image_format(UserImageFormat('left-image-page', 'Выравнивание по левому краю', 'left-image-page', 'original'))
register_image_format(UserImageFormat('right', 'Выравнивание по правому краю', 'right-image-page', 'original'))
register_image_format(UserImageFormat('center', 'Выравнивание по центру', 'center-image-page', 'original'))
register_image_format(UserImageFormat('full_width', 'Выравнивание по ширине', 'fullwidth-image-page', 'original'))