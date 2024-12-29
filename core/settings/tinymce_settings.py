import os

from .base_settings import BASE_DIR

TINYMCE_URL = "tinystatic/"
TINYMCE_JS_URL = os.path.join(BASE_DIR, TINYMCE_URL, "tinymce/tinymce.min.js")
# TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/qagffr3pkuv17a8on1afax661irst1hbr4e6tbv888sz91jc/tinymce/7.0.1-37/tinymce.min.js'
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    "skin": "oxide-dark",
    "content_css": "dark",
    "image_advtab": True,
    "image_caption": True,
    "toolbar_mode": "sliding",
    # "font_family_formats": 'Andale Mono=andale mono,times; Arial=arial,helvetica,sans-serif; Arial Black=arial
    # black,avant garde; Book Antiqua=book antiqua,palatino; Comic Sans MS=comic sans ms,sans-serif; Courier
    # New=courier new,courier; Georgia=georgia,palatino; Helvetica=helvetica; Impact=impact,chicago; Symbol=symbol;
    # Tahoma=tahoma,arial,helvetica,sans-serif; Terminal=terminal,monaco; Times New Roman=times new roman,
    # times; Trebuchet MS=trebuchet ms,geneva; Verdana=verdana,geneva; Webdings=webdings; Wingdings=wingdings,
    # zapf dingbats',
    # "contextmenu": 'link image table',
    "height": 600,
    "width": 960,
    "menubar": (
        # Free
        "file edit view insert format tools table help"
        # Premium
        # "tc"
    ),
    "plugins": (
        # Free
        "preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars "
        "fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist "
        "lists wordcount help charmap emoticons quickbars accordion print paste spellchecker"
        # Premium
        # "powerpaste casechange tinydrive advcode mediaembed tableofcontents checklist tinymcespellchecker a11ychecker"
        # " editimage formatpainter permanentpen pageembed tinycomments mentions linkchecker advtable footnotes "
        # "mergetags autocorrect typography advtemplate markdown revisionhistory"
    ),
    "toolbar": (
        # Free
        "undo redo | accordion accordionremove | blocks fontfamily fontsizeinput | bold italic underline "
        "strikethrough | align numlist bullist | link image | table media | lineheight outdent indent | forecolor "
        "backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor "
        "codesample | ltr rtl"
        # "fontsize"
        # Premium
        # "revisionhistory | aidialog aishortcuts | footnotes mergetags | addtemplate inserttemplate | addcomment "
        # "showcomments | casechange | spellcheckdialog a11ycheck | pageembed formatpainter checklist"
    ),
    "custom_undo_redo_levels": 10,
    "language": "en_US",
}

# TINYMCE_SPELLCHECKER = True
# TINYMCE_EXTRA_MEDIA = {
#     'css': {
#         'all': [
#             ...
#         ],
#     },
#     'js': [
#         ...
#     ],
# }
